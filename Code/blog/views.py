from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from registration.decorators import user_is_confirmed
from .models import Post, Comment
from .forms import BlogCreationForm, CommentCreationForm
from django.shortcuts import get_object_or_404, redirect
from registration.models import CustomUser
from .decorators import user_same_as_comment_user_or_admin, user_same_as_dashboard_user
from django.db.models import Q
from .forms import BlogSearchForm


class BlogListView(ListView):
    template_name = "blog/blog-list.html"
    model = Post
    paginate_by = 3
    ordering = '-date'

    def get_queryset(self):
        form = BlogSearchForm(self.request.GET)
        posts = Post.objects.all()
        if 'uid' in self.kwargs.keys():
            user = get_object_or_404(CustomUser, id=self.kwargs['uid'])
            posts = Post.objects.filter(owner=user)
        if 'makan' in self.request.GET:
            if form.is_valid():
                makan = form.cleaned_data.get('makan')
                if makan != '':
                    posts = posts.filter(Q(city=makan) | Q(province=makan))
        if 'keyword' in self.request.GET:
            if form.is_valid():
                keyword = form.cleaned_data.get('keyword')
                if keyword != '':
                    posts = posts.filter(
                        Q(title__contains=keyword) | Q(owner__first_name=keyword) | Q(owner__last_name=keyword)
                        | Q(description__contains=keyword))

        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'uid' in self.kwargs.keys():
            context['blog_user'] = get_object_or_404(CustomUser, id=self.kwargs['uid'])
        return context


@method_decorator([login_required, user_is_confirmed, user_same_as_dashboard_user], name='dispatch')
class BlogCreateView(View):
    template_name = "blog/create_blog.html"

    def get(self, request, *args, **kwargs):
        form = BlogCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = BlogCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            url = '/blog/post/' + str(post.id)
            return redirect(url)
        else:
            return render(request, self.template_name, {'form': form})


class BlogEditView(View):
    template_name = "blog/create_blog.html"

    def get(self, request, uid, blog_id):
        blog = Post.objects.get(pk=int(blog_id))
        initial = {'title': blog.title, 'description': blog.description, 'province': blog.province,
                   'city': blog.city, 'image': blog.image}
        form = BlogCreationForm(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, uid, blog_id):
        blog = Post.objects.get(pk=int(blog_id))
        form = BlogCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            blog.title = post.title
            blog.description = post.description
            blog.province = post.province
            blog.city = post.city
            blog.image = post.image
            blog.save()
            url = '/blog/post/' + str(blog.id)
            return redirect(url)
        else:
            return render(request, self.template_name, {'form': form})


class BlogDetailView(DetailView):
    template_name = "blog/blog_detail.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['flag'] = (CustomUser.objects.get(post__pk=self.kwargs['pk']) == self.request.user)
        context['uid'] = self.request.user.pk
        return context


@method_decorator([login_required, user_is_confirmed], name='dispatch')
class CreateCommentView(View):
    def post(self, request, *args, **kwargs):
        comment_form = CommentCreationForm(request.POST)
        post = get_object_or_404(Post, id=kwargs['pk'])
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            url = '/blog/post/' + str(post.id)
            messages.success(request, 'نظر شما با موفقیت ثبت شد.')
            return redirect(url)
        else:
            messages.error(request, 'ثبت نظر با مشکل مواجه شده است. لطفاً دوباره تلاش کنید.')
            url = '/blog/post/' + str(post.id)
            return redirect(url)


@method_decorator([login_required, user_is_confirmed, user_same_as_comment_user_or_admin], name='dispatch')
class CommentDelete(View):
    def get(self, request, *args, **kwargs):
        comment_id = kwargs['id']
        comment = Comment.objects.get(id=comment_id)
        post = comment.post
        comment.delete()
        messages.warning(request, 'نظر حذف شد.')
        url = '/blog/post/' + str(post.id)
        return redirect(url)
