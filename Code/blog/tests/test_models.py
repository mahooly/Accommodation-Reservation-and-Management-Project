import filecmp
import os
import datetime
from Code.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from blog.models import Post, Comment
from registration.models import CustomUser


class BlogModelsTestCase(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')

    def test_post_model(self):
        exp_data = {"title": "دریاچه سراوان", "description": "خیلی خوش گذشت!", "province": "گیلان",
                    "city": "رشت", "date": datetime.datetime.today().date(), "image": self.img}
        CustomUser.objects.create(username='gatmiry', password='2471351khf',
                                  birth_date=datetime.datetime.today(), image=self.img, first_name='خشایار',
                                  last_name='گتمیری', gender='male')
        user = CustomUser.objects.get(username='gatmiry')
        Post.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                            province='گیلان', city='رشت', image=self.img)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get(owner=user)
        self.assertEqual(post.title, exp_data['title'])
        self.assertEqual(post.description, exp_data['description'])
        self.assertEqual(post.province, exp_data['province'])
        self.assertEqual(post.city, exp_data['city'])
        self.assertEqual(post.date, exp_data['date'])
        self.assertTrue(filecmp.cmp(os.path.join(BASE_DIR, post.image.path), self.image_path))

    def test_comment_model(self):
        exp_data = {'comment': 'بابا عالی بود'}
        CustomUser.objects.create(username='gatmiry', password='2471351khf',
                                  birth_date=datetime.datetime.today(), image=self.img, first_name='خشایار',
                                  last_name='گتمیری', gender='male')
        user = CustomUser.objects.get(username='gatmiry')
        Post.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                            province='گیلان', city='رشت', image=self.img)
        post = Post.objects.get(owner=user)
        Comment.objects.create(comment='بابا عالی بود', post=post, user=user)
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.get(post=post)
        self.assertEqual(comment.comment, exp_data['comment'])
        self.assertEqual(comment.user.username, 'gatmiry')
