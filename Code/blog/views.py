from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Post, Comment
from .forms import BlogCreationForm, CommentCreationForm
from django.shortcuts import get_object_or_404, redirect
from registration.models import CustomUser
from .decorators import user_same_as_comment_user_or_admin, user_same_as_dashboard_user


class BlogListView(ListView):
    template_name = "blog/blog-list.html"
    model = Post
    paginate_by = 3
    ordering = '-date'

    def get_queryset(self):
        if 'uid' in self.kwargs.keys():
            user = get_object_or_404(CustomUser, id=self.kwargs['uid'])
            return Post.objects.filter(owner=user)
        else:
            return Post.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'uid' in self.kwargs.keys():
            context['blog_user'] = get_object_or_404(CustomUser, id=self.kwargs['uid'])
        return context


@method_decorator([login_required, user_same_as_dashboard_user], name='dispatch')
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


class BlogDetailView(DetailView):
    template_name = "blog/blog_detail.html"
    model = Post


@method_decorator(login_required, name='dispatch')
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


@method_decorator([login_required, user_same_as_comment_user_or_admin], name='dispatch')
class CommentDelete(View):
    def get(self, request, *args, **kwargs):
        comment_id = kwargs['id']
        comment = Comment.objects.get(id=comment_id)
        post = comment.post
        comment.delete()
        messages.warning(request, 'نظر حذف شد.')
        url = '/blog/post/' + str(post.id)
        return redirect(url)
