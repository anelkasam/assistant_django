from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User

from todo.models import Category, Task, Goal


class CategoryTest(TestCase):
    fixtures = ['user', 'category']

    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(title='Housework', user=self.user)

    def test_delete(self):
        with self.assertRaises(Exception):
            Category.objects.get(id=1).delete()

        cat = Category.objects.get(id=2)
        cat.delete()
        with self.assertRaises(Category.DoesNotExist):
            cat.refresh_from_db()

    def test_str(self):
        self.assertEqual(Category.objects.get(id=1).__str__(), 'Other')


class TaskTest(TestCase):
    fixtures = ['user', 'category']

    def setUp(self):
        self.user = User.objects.create(username='user', password='password')
        self.other_cat = Category.objects.get(id=1)
        self.task = Task.objects.create(title='test', user=self.user)

    def test_str(self):
        self.assertEqual(self.task.__str__(), 'test (Other). Due to None')

    def test_delete(self):
        self.assertEqual(self.task.status, Task.NEW)
        self.task.delete()
        self.assertEqual(self.task.status, Task.CANCELED)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.CANCELED)


class GoalTest(TestCase):
    pass
