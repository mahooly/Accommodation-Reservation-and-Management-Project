from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Feed, Comment
from .forms import BlogCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from registration.models import CustomUser
from accommodation.models import Accommodation
from django.template import RequestContext

# Create your views here.

class BlogListView(View):
    template_name = "blog/blog_list.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        username = kwargs['username']
        user2 = CustomUser.objects.get(username=username)
        feed_array = Feed.objects.filter(owner__username = username)
        page_number = kwargs['page_number']
        paginator = Paginator(feed_array, 2)
        if page_number == 0:
            url = "/username="+ username +"/blog_list/1"
            return redirect(url)
        if page_number > paginator.num_pages:     # ran out of pages!
            page_number -= 1
            url = "/username=" + username + "/blog_list/"+str(page_number)
            return redirect(url)
        page_feeds = paginator.page(page_number).object_list
        return render(request,self.template_name , {'username' : username , 'page_feeds' : page_feeds, 'page_number_minos':page_number-1
                                                    , 'page_number' : page_number , 'page_number_plus':page_number+1 ,
                                                    'user_name':user2.get_full_name(), 'is_empty':(len(page_feeds)==0)})
            #HttpResponse("Hello World!")

    def post(self, request, username, page_number):
        searched_phrase = request.POST['searched_phrase']
        url = "/searched_phrase="+searched_phrase+"/page_number=1"
        return redirect(url)


class BlogSearchView(View):
    template_name = "blog/blog_search.html"

    def get(self, request, searched_phrase, page_number):
        keywords = searched_phrase.split()

        feed_array = []
        for feed in Feed.objects.all():
            for word in keywords:
                print("I am in loop for feed = "+ feed.__str__() + " and word = "+word)
                if feed.title.find(word) != -1 or feed.description.find(word) != -1:
                    feed_array.append(feed)
                    break


        paginator = Paginator(feed_array, 2)
        if page_number == 0:
            url = "/searched_phrase=" + searched_phrase + "/page_number=1"
            return redirect(url)
        if page_number > paginator.num_pages:  # ran out of pages!
            page_number -= 1
            url = "/searched_phrase=" + searched_phrase + "/page_number=" + str(page_number)
            return redirect(url)
        page_feeds = paginator.page(page_number).object_list

        #print("page-feeds are ",page_feeds)
        print("len is ",len(page_feeds))
        return render(request, self.template_name, {'page_feeds' : page_feeds, 'page_number_minos':page_number-1
                                                    , 'page_number' : page_number , 'page_number_plus':page_number+1 ,
                                                    'searched_phrase':searched_phrase , 'is_empty':(len(page_feeds)==0)})
        #return HttpResponse("Hello World!")

    def post(self, request, *args, **kwargs):
        searched_phrase = request.POST['searched_phrase']
        url = "/searched_phrase="+searched_phrase+"/page_number=1"
        return redirect(url)


class BlogCreateView(View):
    template_name = "blog/create_blog.html"

    def get(self, request, username):
        form = BlogCreationForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request, username):
        print("hey! I am in blog_create view")
        form = BlogCreationForm(request.POST)
        if form.is_valid():
            owner = request.user
            feed = form.save(commit=False)
            #print("the ... owner is ",owner.birth_date)
            feed.owner = owner
            if 'image' in request.FILES:
                feed.image = request.FILES['image']
            print("latitude is ",feed.latitude)
            print("province is ",feed.province)
            feed.save()
            url = "/username="+str(username)+"/blog_list/1"
            return redirect(url)
        else:
            print("the form was not valid")
            print(form.errors)
            return render(request, self.template_name, {'form':form})


class BlogDetailView(View):
    template_name = "blog/blog_detail.html"

    def get(self, request, username, feed_id):
        feed = Feed.objects.get(pk=feed_id)
        user2 = CustomUser.objects.get(username=username)
        comment = Comment(feed=feed, owner=user2, description="سلام")
        #print("comment owner is ")
        #print(comment.owner)
        #print("this is", feed.comment_set)

        return render(request,self.template_name , {'feed': feed , 'user_name':user2.get_full_name() , 'user2':user2,
                                                    'comments':feed.comment_set.all(), 'request_user_id':request.user.id,
                                                    'username':username})
        #return HttpResponse("Hello!")

    def post(self, requeset, username, feed_id):
        description = requeset.POST['description']
        url = "/username="+username+"/blog_detail/blog_id="+str(feed_id)
        if description == '':
            return redirect(url)
        feed = Feed.objects.get(id=feed_id)
        user = requeset.user
        comment = Comment(description=description, feed=feed, owner=user)
        comment.save()
        return redirect(url)

class CommentDelete(View):

    def get(self, request, comment_id, feed_id, username):
        print("I am here man")
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        url = '/username='+str(username)+'/blog_detail/blog_id='+str(feed_id)
        return redirect(url)