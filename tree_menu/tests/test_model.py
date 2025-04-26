from django.test import TestCase
from django.urls import reverse
from tree_menu.models import TreeMenu


class TreeMenuModelTest(TestCase):
    def setUp(self):
        self.main_menu = TreeMenu.objects.create(
            name='Main',
            menu_name='main_menu',
            url='/'
        )
        self.about = TreeMenu.objects.create(
            name='About',
            menu_name='main_menu',
            parent=self.main_menu,
            url='/about/'
        )
        self.contacts = TreeMenu.objects.create(
            name='Contacts',
            menu_name='main_menu',
            parent=self.main_menu,
            url='/contacts/'
        )
        self.team = TreeMenu.objects.create(
            name='Team',
            menu_name='main_menu',
            parent=self.about,
            url='/about/team/'
        )

    def test_menu_creation(self):
        """ Проверка правильности добавления данных в БД """

        self.assertEqual(self.main_menu.name, 'Main')
        self.assertEqual(self.main_menu.menu_name, 'main_menu')
        self.assertEqual(self.main_menu.url, '/')
        self.assertIsNone(self.main_menu.parent)

        self.assertEqual(self.about.parent, self.main_menu)
        self.assertEqual(self.team.parent, self.about)

    def test_get_url_method(self):
        """ Тест функции получения ссылки """

        self.assertEqual(self.main_menu.get_url(), '/')
        self.assertEqual(self.about.get_url(), '/about/')

        named_url_item = TreeMenu.objects.create(
            name='Test',
            menu_name='test_menu',
            named_url='admin:index'
        )
        self.assertEqual(named_url_item.get_url(), reverse('admin:index'))
