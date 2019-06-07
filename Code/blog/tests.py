from django.test import TestCase
from .models import Post, Comment
from registration.models import CustomUser
from django.test.client import Client
from datetime import datetime


class FeedCommentModelsTestCase(TestCase):
    client = Client()

    def setUp(self):
        user = CustomUser.objects.create(username='gatmiry', password='2471351khf')
        feed = Post.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                                   province='گیلان', city='رشت')
        comment = Comment.objects.create(description='بابا عالی بود', feed=feed, owner=user)
        feed.save()
        comment.save()
        self.client.post('/register/', {'username': 'gatmirytest', 'password1': '2471351khf', 'password2': '2471351khf',
                                        'first_name': 'khashayar', 'last_name': 'gatmiry',
                                        'birth_date': datetime.now().date(), 'gender': 'male', })

    def test_object_save(self):
        feed = Post.objects.get(owner__username='gatmiry')
        comment = Comment.objects.get(feed__title='دریاچه سراوان')
        self.assertEqual(feed.title, 'دریاچه سراوان')
        self.assertEqual(feed.description, 'خیلی خوش گذشت!')
        self.assertEqual(feed.province, "گیلان")
        self.assertEqual(feed.city, "رشت")
        self.assertEqual(comment.description, 'بابا عالی بود')
        self.assertEqual(comment.feed.owner.username, 'gatmiry')

    def test_request_blog_create(self):
        response = self.client.post('/username%3Dgatmirytest/blog_create/',
                                    {'title': 'تخت جمشید', 'description': 'جای تاریخی', 'city': 'شیراز', 'province': 'فارس'})
        feed = Post.objects.get(title='تخت جمشید')
        self.assertEqual(feed.title, 'تخت جمشید')
        self.assertEqual(feed.description, 'جای تاریخی')
        self.assertEqual(feed.image.url, '/media/blog_pics/no-picture.png')
        self.assertEqual(feed.city, 'شیراز')
        self.assertEqual(feed.province, 'فارس')

    def test_request_comment_create(self):
        response = self.client.post('/username=gatmirytest/blog_detail/blog_id=1',
                                    {'description': 'این کامنت جالبی خواهد شد'})
        feed = Post.objects.get(title='دریاچه سراوان')
        comment = feed.comment_set.all()[1]
        self.assertEqual(comment.description, 'این کامنت جالبی خواهد شد')

    def test_request_comment_delete(self):
        self.assertFalse(Comment.objects.filter(description='بابا عالی بود').count() == 0)
        comment = Comment.objects.get(description='بابا عالی بود')
        self.assertEqual(comment.feed.title, 'دریاچه سراوان')
        response = self.client.get('/delete_comment/comment_id=1/username=alaki1/feed_id=2')
        self.assertTrue(Comment.objects.filter(description='بابا عالی بود').count() == 0)

