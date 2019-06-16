from django.contrib.auth.models import User, AnonymousUser
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from ..models import Profile, Family


class RegistrationTest(TestCase):
    fixtures = ['user']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=1)

    def test_success_registration_get(self):
        response = self.client.get('/auth/register/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('auth/register.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context.get('user'), AnonymousUser)

    def test_success_registration_post(self):
        response = self.client.post('/auth/register/', data={
            'username': 'anelka',
            'password': 'password',
            'password2': 'password',
            'email': 'example@test.com'
        }, follow=True)

        self.assertRedirects(response, '/')
        user = User.objects.all().last()
        self.assertEqual(user.username, 'anelka')
        self.assertEqual(int(self.client.session.get('_auth_user_id')), user.id)
        self.assertContains(response, 'Congratulations!!! You successfully register on our site!')

    def test_duplicate_username(self):
        response = self.client.post('/auth/register/', data={
            'username': 'user1',
            'password': 'password',
            'password2': 'password',
            'email': 'example@test.com'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User with given username address is already registered.')
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_duplicate_email(self):
        response = self.client.post('/auth/register/', data={
            'username': 'anelka',
            'password': 'password',
            'password2': 'password',
            'email': 'test1@gmail.com'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User with given email address is already registered.')
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_invalid_password2(self):
        response = self.client.post('/auth/register/', data={
            'username': 'anelka',
            'password': 'password',
            'password2': 'password2',
            'email': 'example@test.com'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please check the confirmation password.')
        self.assertIsNone(self.client.session.get('_auth_user_id'))

    def test_profile_creation(self):
        response = self.client.post('/auth/register/', data={
            'username': 'anelka',
            'password': 'password',
            'password2': 'password',
            'email': 'example@test.com'
        }, follow=True)

        self.assertRedirects(response, '/')
        user = User.objects.all().last()
        self.assertEqual(user.username, 'anelka')
        self.assertEqual(int(self.client.session.get('_auth_user_id')), user.id)
        self.assertContains(response, 'Congratulations!!! You successfully register on our site!')
        self.assertIsInstance(user.profile, Profile)

    def test_register_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get('/auth/register/', follow=True)

        self.assertRedirects(response, '/')
        self.assertContains(response, 'Only unregitered users can create new account!')

    def test_invalid_method(self):
        response = self.client.patch('/auth/register/')

        self.assertEqual(response.status_code, 200)


class ProfilePageTest(TestCase):
    fixtures = ['user']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(id=1)
        self.client.force_login(self.user)

    def test_success_get(self):
        response = self.client.get('/auth/user_profile/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)

    def test_success_post(self):
        response = self.client.post('/auth/user_profile/', data={
            'first_name': 'Elena',
            'last_name': 'Samoilenko'
        })

        self.user.refresh_from_db()
        self.assertRedirects(response, '/auth/user_profile/')
        self.assertEqual(self.user.first_name, 'Elena')
        self.assertEqual(self.user.last_name, 'Samoilenko')

    def test_anonymous_user(self):
        self.client.logout()
        response = self.client.get('/auth/user_profile/')
        self.assertRedirects(response, '/auth/login/?next=/auth/user_profile/')

    def test_create_family_get(self):
        response = self.client.get('/auth/create_family/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_create_family_anonymous_user(self):
        self.client.logout()
        response = self.client.get('/auth/user_profile/')
        self.assertRedirects(response, '/auth/login/?next=/auth/user_profile/')

    def test_create_family_post(self):
        response = self.client.post('/auth/create_family/', data={
            'last_name': 'Samoilenko'
        }, follow=True)

        self.assertRedirects(response, '/auth/user_profile/')
        self.user.refresh_from_db()
        family = Family.objects.all().last()
        self.assertEqual(self.user.profile.family, family)
        self.assertTrue(self.user.profile.is_admin)
        self.assertContains(response, 'New Family was created.')

    def test_create_family_failed(self):
        family = Family.objects.create(last_name='Samoilenko')
        self.user.profile.family = family
        self.user.save()

        respose = self.client.post('/auth/create_family/', data={
            'last_name': 'TestTest'
        }, follow=True)

        self.assertRedirects(respose, '/auth/user_profile/')
        self.assertContains(respose, 'ou cannot create new Family as you belong to one.')

    def test_generate_token(self):
        family = Family.objects.create(last_name='Samoilenko')
        self.user.profile.family = family
        self.user.profile.is_admin = True
        self.user.save()

        response = self.client.get('/auth/create_token/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.content, bytes)

    def test_generate_token_failed(self):
        response = self.client.get('/auth/create_token/', follow=True)

        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'Just Family admins can create the token.')

        family = Family.objects.create(last_name='Samoilenko')
        self.user.profile.family = family
        self.user.save()

        response = self.client.get('/auth/create_token/', follow=True)

        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'Just Family admins can create the token.')

    def test_generate_token_anonymous(self):
        self.client.logout()
        response = self.client.get('/auth/create_token/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/create_token/')

    def test_connect_to_family_success(self):
        family = Family.objects.create(last_name='Samoilenko')
        token = family.generate_token()

        response = self.client.post('/auth/connect_to_family/', data={'token': token})
        self.assertRedirects(response, '/auth/user_profile/')
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.family, family)
        self.assertFalse(self.user.profile.is_admin)

    def test_connect_to_family_bag_token(self):
        response = self.client.post('/auth/connect_to_family/', data={}, follow=True)
        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'Token cannot be empty.')

        response = self.client.post('/auth/connect_to_family/', data={'token':'sdfghjk'}, follow=True)
        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'Invalid token.')

        response = self.client.get('/auth/connect_to_family/')
        self.assertEqual(response.status_code, 405)

    def test_connect_to_family_have_family(self):
        family = Family.objects.create(last_name='Samoilenko')
        self.user.profile.family = family
        self.user.save()

        response = self.client.post('/auth/connect_to_family/', data={'token': family.generate_token()}, follow=True)

        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'You cannot connect to another family.')

    def test_leave_family_success(self):
        family = Family.objects.create(last_name='Samoilenko')
        self.user.profile.family = family
        self.user.save()

        response = self.client.get('/auth/leave_family/')
        self.assertRedirects(response, '/auth/user_profile/')

    def test_leave_family_anonymous(self):
        self.client.logout()
        response = self.client.get('/auth/leave_family/', follow=True)
        self.assertRedirects(response, '/auth/login/?next=/auth/leave_family/')

    def test_leave_family_no_family(self):
        response = self.client.get('/auth/leave_family/', follow=True)
        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'You do not belong to the Family')

    def test_leave_family_admin(self):
        family = Family.objects.create(last_name='Samoilenko')
        self.user.profile.family = family
        self.user.profile.is_admin = True
        self.user.save()

        response = self.client.get('/auth/leave_family/', follow=True)
        self.assertRedirects(response, '/auth/user_profile/')
        self.assertContains(response, 'Admin cannot leave the Family. Set up new admin first.')
