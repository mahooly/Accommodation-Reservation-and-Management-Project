from django.test import TestCase
from .models import Feed, Comment
from registration.models import CustomUser
from django.test.client import Client
from datetime import datetime

class FeedCommentModelsTestCase(TestCase):
    client = Client()

    def setUp(self):
        ### populating the Database
        user = CustomUser.objects.create(username='gatmiry', password='2471351khf')
        feed = Feed.objects.create(title='دریاچه سراوان', description='خیلی خوش گذشت!', owner=user,
                            province='گیلان', city='رشت', address='نبش رشت')
        comment = Comment.objects.create(description='بابا عالی بود', feed=feed, owner=user)
        feed.save()
        comment.save()
        ### authenticating a user
        self.client.post('/register/', {'username': 'gatmirytest', 'password1': '2471351khf', 'password2': '2471351khf',
                                        'first_name': 'khashayar', 'last_name': 'gatmiry',
                                        'birth_date': datetime.now().date(), 'gender': 'male', })



    def test_object_save(self):
        feed = Feed.objects.get(owner__username='gatmiry')
        comment = Comment.objects.get(feed__title='دریاچه سراوان')
        self.assertEqual(feed.title, 'دریاچه سراوان')
        self.assertEqual(feed.description, 'خیلی خوش گذشت!')
        self.assertEqual(feed.province, "گیلان")
        self.assertEqual(feed.city, "رشت")
        self.assertEqual(feed.address, "نبش رشت")
        self.assertEqual(comment.description, 'بابا عالی بود')
        self.assertEqual(comment.feed.owner.username, 'gatmiry')


    def test_request_blog_create(self):
        ## already authenticated
        response = self.client.post('/username%3Dgatmirytest/blog_create/',
                               {'title': 'تخت جمشید', 'description': 'جای تاریخی',
                                'address': 'نبش شیراز', 'city': 'شیراز', 'province': 'فارس'})
        feed = Feed.objects.get(title='تخت جمشید')
        self.assertEqual(feed.title, 'تخت جمشید')
        self.assertEqual(feed.description, 'جای تاریخی')
        self.assertEqual(feed.image.url, '/media/blog_pics/no-picture.png')
        self.assertEqual(feed.address, 'نبش شیراز')
        self.assertEqual(feed.city, 'شیراز')
        self.assertEqual(feed.province, 'فارس')

    def test_request_comment_create(self):
        ## already authenticated
        response = self.client.post('/username=gatmirytest/blog_detail/blog_id=1',{'description':'این کامنت جالبی خواهد شد'})
        feed = Feed.objects.get(title='دریاچه سراوان')
        comment = feed.comment_set.all()[1]
        self.assertEqual(comment.description, 'این کامنت جالبی خواهد شد')

    def test_request_comment_delete(self):
        self.assertFalse(Comment.objects.filter(description='بابا عالی بود').count() == 0)
        comment = Comment.objects.get(description='بابا عالی بود')
        self.assertEqual(comment.feed.title, 'دریاچه سراوان')
        response = self.client.get('/delete_comment/comment_id=1/username=alaki1/feed_id=2')
        self.assertTrue(Comment.objects.filter(description='بابا عالی بود').count() == 0)

    def test_search_redirect(self):
        response = self.client.post('/username=gatmirytest/blog_list/1', {'searched_phrase':"superman"})
        self.assertRedirects(response, '/searched_phrase=superman/page_number=1')

    def test_low_page_redirect(self):
        response = self.client.get('/username=gatmirytest/blog_list/0')
        self.assertRedirects(response, '/username=gatmirytest/blog_list/1')

    def test_high_page_redirect(self):
        response = self.client.get('/username=gatmirytest/blog_list/2')
        self.assertRedirects(response, '/username=gatmirytest/blog_list/1')