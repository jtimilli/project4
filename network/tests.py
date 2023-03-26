from django.test import TestCase, Client

from .models import Following, User

# Create your tests here.

#TODO Write test case for clicks count, following 

class FollowingTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create users
        cls.user1 = User.objects.create(username="user1", password="password1", email="user1@email.com")
        cls.user2 = User.objects.create(username="user2", password="password1", email="user1@email.com")
        cls.user3 = User.objects.create(username="user3", password="password1", email="user1@email.com")
        cls.user4 = User.objects.create(username="user4", password="password1", email="user1@email.com")

        # Create following
        Following.objects.create(user=cls.user1, following=cls.user2)
        Following.objects.create(user=cls.user2, following=cls.user1)
        Following.objects.create(user=cls.user3, following=cls.user1)
        Following.objects.create(user=cls.user4, following=cls.user1)

    def test_following_count(self):
        # Count amount of user's are following a user1
        a1 = Following.objects.filter(following=self.__class__.user1)
        self.assertEqual(a1.count(), 3)

    
    def test_views(self):

        c = Client()
        response = c.get(f"/")
        self.assertEqual(response.status_code, 200)
        
