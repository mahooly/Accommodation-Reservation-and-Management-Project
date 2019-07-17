import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Comment
from registration.models import CustomUser
from django.test.client import Client
from datetime import datetime


class BlogViewsTestCase(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')
        self.client = Client()

    def test_request_blog_create(self):
        CustomUser.objects.create(username='gatmiry', password='2471351khf',
                                  birth_date=datetime.today(), image=self.img, first_name='خشایار',
                                  last_name='گتمیری', gender='male')
        user = CustomUser.objects.get(username='gatmiry')
        self.client.force_login(user)
        response = self.client.post(reverse('blog_create', kwargs={'uid': user.id}),
                                    {'title': 'تخت جمشید', 'description': 'جای تاریخی', 'province': 'فارس',
                                     'city': 'شیراز'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get(owner=user)
        self.assertEqual(post.title, 'تخت جمشید')
        self.assertEqual(post.description, 'جای تاریخی')
        self.assertFalse(bool(post.image))
        self.assertEqual(post.city, 'شیراز')
        self.assertEqual(post.province, 'فارس')

    def test_request_comment_create(self):
        CustomUser.objects.create(username='gatmiry', password='2471351khf',
                                  birth_date=datetime.today(), image=self.img, first_name='خشایار',
                                  last_name='گتمیری', gender='male')
        user = CustomUser.objects.get(username='gatmiry')
        self.client.force_login(user)
        post = Post.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                                   province='گیلان', city='رشت', image=self.img)
        response = self.client.post(reverse('post_comment', kwargs={'pk': post.id}),
                                    {'description': 'این کامنت جالبی خواهد شد'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
        response = self.client.post(reverse('post_comment', kwargs={'pk': post.id}),
                                    {'comment': 'این کامنت جالبی خواهد شد'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get(post=post)
        self.assertEqual(comment.comment, 'این کامنت جالبی خواهد شد')

    def test_request_comment_delete(self):
        CustomUser.objects.create(username='gatmiry', password='2471351khf',
                                  birth_date=datetime.today(), image=self.img, first_name='خشایار',
                                  last_name='گتمیری', gender='male')
        user = CustomUser.objects.get(username='gatmiry')
        self.client.force_login(user)
        post = Post.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                                   province='گیلان', city='رشت', image=self.img)
        Comment.objects.create(comment='بابا عالی بود', post=post, user=user)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get(comment='بابا عالی بود')
        response = self.client.get(reverse('comment_delete', kwargs={'id': comment.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_request_blog_search(self):
        CustomUser.objects.create(username='gatmiry', password='2471351khf',
                                  birth_date=datetime.today(), image=self.img, first_name='خشایار',
                                  last_name='گتمیری', gender='male')
        user = CustomUser.objects.get(username='gatmiry')
        self.client.force_login(user)
        Post.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                            province='گیلان', city='رشت', image=self.img)
        Post.objects.create(title='دریاچه آرام', description='عجب جایی بود!', owner=user,
                            province='گیلان', city='رشت', image=self.img)
        Post.objects.create(title='بازار جامع', description='بابا دس مریزاد!', owner=user,
                            province='گیلان', city='ترخو', image=self.img)

        response = self.client.get(reverse('blog_list', kwargs={'uid': user.pk}) + '?province=گیلان')
        self.assertContains(response, 'blog-post', 3)
        response = self.client.get(reverse('blog_list', kwargs={'uid': user.pk}) + '?province=گیلان&keyword=دریاچه')
        self.assertContains(response, 'blog-post', 2)
        response = self.client.get(reverse('blog_list', kwargs={'uid': user.pk}) + '?city=آرام&keyword=عجب')
        self.assertContains(response, 'blog-post', 0)
        response = self.client.get(reverse('blog_list', kwargs={'uid': user.pk}) + '?city=رشت&keyword=خیلی')
        self.assertContains(response, 'blog-post', 1)
        response = self.client.get(reverse('blog_list', kwargs={'uid': user.pk}) + '?city=ترخو&keyword=مریزاد')
        self.assertContains(response, 'blog-post', 1)
