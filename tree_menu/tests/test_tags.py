from django.test import TestCase
from django.urls import reverse
from tree_menu.models import TreeMenu
from tree_menu.templatetags.menu_tag import (
    get_active_item, get_dict_tree, forming_menu_tree, get_active_item_tree
)
from django.template import Template, Context
from django.http import HttpRequest


class GetActiveItemTest(TestCase):
    """ Тестирование функции get_active_item """

    def setUp(self):
        self.item1 = TreeMenu.objects.create(
            name='Item1',
            menu_name='test_menu',
            url='/item1/'
        )
        self.item2 = TreeMenu.objects.create(
            name='Item2',
            menu_name='test_menu',
            url='/item2/'
        )

    def test_get_active_item_found(self):
        current_url = '/item1/'
        active_item = get_active_item([self.item1, self.item2], current_url, None)
        self.assertEqual(active_item, self.item1)

    def test_get_active_item_not_found(self):
        current_url = '/неизвестная_ссылка/'
        active_item = get_active_item([self.item1, self.item2], current_url, None)
        self.assertIsNone(active_item)

    def test_get_active_item_with_named_url(self):
        """ Получение активного пункта меню с использованием именованной ссылки """

        named_item = TreeMenu.objects.create(
            name='Admin',
            menu_name='test_menu',
            named_url='admin:index'
        )
        current_url = reverse('admin:index')
        active_item = get_active_item([named_item], current_url, None)
        self.assertEqual(active_item, named_item)


class GetDictTreeTest(TestCase):
    """ Тестирование функции get_dict_tree """

    def setUp(self):
        self.item1 = TreeMenu.objects.create(
            name='Item1',
            menu_name='test_menu',
            url='/item1/'
        )
        self.item2 = TreeMenu.objects.create(
            name='Item2',
            menu_name='test_menu',
            parent=self.item1,
            url='/item2/'
        )

    def test_get_dict_tree(self):
        """ Тестирование построения словаря всех элементов дерева без детей """

        item_dict = {}
        get_dict_tree([self.item1, self.item2], item_dict)

        self.assertEqual(len(item_dict), 2)
        self.assertIn(self.item1.pk, item_dict)
        self.assertIn(self.item2.pk, item_dict)

        self.assertEqual(item_dict[self.item1.pk]['item'], self.item1)
        self.assertEqual(item_dict[self.item2.pk]['item'], self.item2)

        self.assertEqual(item_dict[self.item1.pk]['children'], [])
        self.assertEqual(item_dict[self.item2.pk]['children'], [])

        self.assertFalse(item_dict[self.item1.pk]['is_active'])
        self.assertFalse(item_dict[self.item2.pk]['is_active'])

        self.assertFalse(item_dict[self.item1.pk]['is_parent_active'])
        self.assertFalse(item_dict[self.item2.pk]['is_parent_active'])


class FormingMenuTreeTest(TestCase):
    """ Тестирование функции forming_menu_tree """

    def setUp(self):
        self.item1 = TreeMenu.objects.create(
            name='Item1',
            menu_name='test_menu',
            url='/item1/'
        )
        self.item2 = TreeMenu.objects.create(
            name='Item2',
            menu_name='test_menu',
            parent=self.item1,
            url='/item2/'
        )
        self.item3 = TreeMenu.objects.create(
            name='Item3',
            menu_name='test_menu',
            parent=self.item2,
            url='/item3/'
        )
        self.item4 = TreeMenu.objects.create(
            name='Item4',
            menu_name='test_menu',
            parent=self.item2,
            url='/item4/'
        )

    def test_forming_menu_tree(self):
        """ Тест формирования списка меню из словаря и QuerySet """

        item_dict = {}
        menu_tree = []

        get_dict_tree([self.item1, self.item2, self.item3, self.item4], item_dict)
        forming_menu_tree([self.item1, self.item2, self.item3, self.item4], item_dict, menu_tree)

        self.assertEqual(len(menu_tree), 1)
        self.assertEqual(len(item_dict[self.item1.pk]['children']), 1)
        self.assertEqual(len(item_dict[self.item2.pk]['children']), 2)
        self.assertEqual(item_dict[self.item1.pk]['children'][0]['item'], self.item2)
        self.assertEqual(item_dict[self.item2.pk]['children'][0]['item'], self.item3)
        self.assertEqual(item_dict[self.item2.pk]['children'][1]['item'], self.item4)

        self.assertEqual(menu_tree[0]['item'], self.item1)


class GetActiveItemTreeTest(TestCase):
    """ Тестирование функции get_active_item_tree """

    def setUp(self):
        self.item1 = TreeMenu.objects.create(
            name='Item1',
            menu_name='test_menu',
            url='/item1/'
        )
        self.item2 = TreeMenu.objects.create(
            name='Item2',
            menu_name='test_menu',
            parent=self.item1,
            url='/item2/'
        )
        self.item3 = TreeMenu.objects.create(
            name='Item3',
            menu_name='test_menu',
            parent=self.item2,
            url='/item3/'
        )
        self.item4 = TreeMenu.objects.create(
            name='Item4',
            menu_name='test_menu',
            parent=self.item2,
            url='/item4/'
        )

    def test_get_active_item_tree(self):
        """ Тест выделения активных элементов и их родителей """

        item_dict = {}
        get_dict_tree([self.item1, self.item2, self.item3, self.item4], item_dict)

        # Нет активных
        get_active_item_tree(None, item_dict)
        self.assertFalse(item_dict[self.item1.pk]['is_active'])
        self.assertFalse(item_dict[self.item2.pk]['is_active'])
        self.assertFalse(item_dict[self.item3.pk]['is_active'])
        self.assertFalse(item_dict[self.item4.pk]['is_active'])

        # Активен item3
        get_active_item_tree(self.item3, item_dict)

        self.assertTrue(item_dict[self.item3.pk]['is_active'])
        self.assertFalse(item_dict[self.item3.pk]['is_parent_active'])

        self.assertTrue(item_dict[self.item1.pk]['is_parent_active'])
        self.assertTrue(item_dict[self.item2.pk]['is_parent_active'])
        self.assertFalse(item_dict[self.item4.pk]['is_parent_active'])

        self.assertFalse(item_dict[self.item1.pk]['is_active'])
        self.assertFalse(item_dict[self.item2.pk]['is_active'])
        self.assertFalse(item_dict[self.item4.pk]['is_active'])


class TemplateTagTest(TestCase):
    """ Тестирование шаблонного тега """

    def setUp(self):
        self.main_menu = TreeMenu.objects.create(
            name='Main',
            menu_name='main_menu',
            url='/'
        )
        self.request = HttpRequest()
        self.request.path_info = '/'
        self.context = Context({'request': self.request})

    def test_template_tag_rendering(self):
        """ Тестирование создания шаблонного тега """

        template = Template(
            '{% load menu_tag %}'
            '{% draw_menu "main_menu" %}'
        )
        rendered = template.render(self.context)
        # Проверка наличия данных в шаблоне
        self.assertIn('Main', rendered)
        self.assertIn('main_menu', rendered)
