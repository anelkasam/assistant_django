from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Family


class ProfileTest(TestCase):
    fixtures = ['user']

    def setUp(self):
        self.user = User.objects.create(username='Elena', email='anelka.s@mail.ru', password='password')

    def test_create_user_profile(self):
        self.assertIsInstance(self.user.profile, Profile)

    def test_profile_str(self):
        self.assertEqual(self.user.profile.__str__(), f'User {self.user.username}')


class FamilyTest(TestCase):
    def setUp(self):
        self.family = Family.objects.create(last_name='Samoilenko')

    def test_family_str(self):
        self.assertEqual(self.family.__str__(), f'Family {self.family.last_name}')

    def test_generate_verify_token(self):
        token = self.family.generate_token()
        self.assertIsInstance(token, str)
        self.assertEqual(Family.verify_token(token), self.family)

    def test_invalid_token(self):
        self.assertIsNone(Family.verify_token(''))
        self.assertIsNone(Family.verify_token('sdfghjklkjhgf'))
