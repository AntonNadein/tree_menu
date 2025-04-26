from typing import Dict, List, Optional
from django import template
from django.urls import NoReverseMatch
from tree_menu.models import TreeMenu

register = template.Library()


@register.inclusion_tag('tree_menu/tags/menu.html', takes_context=True)
def draw_menu(context: Dict, menu_name: str) -> Dict:
    """ Отображение древовидного меню """

    request = context['request']
    current_url = request.path_info
    menu_items = TreeMenu.objects.filter(menu_name=menu_name)

    active_item = None
    active_item = get_active_item(menu_items, current_url, active_item)

    # Собираем дерево меню
    menu_tree = []
    item_dict = {}

    get_dict_tree(menu_items, item_dict)
    forming_menu_tree(menu_items, item_dict, menu_tree)
    get_active_item_tree(active_item, item_dict)

    return {
        'menu_tree': menu_tree,
        'menu_name': menu_name,
        'current_url': current_url,
    }


def get_active_item(menu_items: List[TreeMenu],
                    current_url: str,
                    active_item: Optional[TreeMenu]
                    ) -> Optional[TreeMenu]:
    """ Получаем активный пункт меню """

    for item in menu_items:
        try:
            item_url = item.get_url()
            if item_url == current_url:
                active_item = item
                break
        except NoReverseMatch:
            continue
    return active_item


def get_dict_tree(menu_items: List[TreeMenu],
                  item_dict: Dict[int, Dict]
                  ) -> None:
    """ Создаем все элементы дерева без детей """

    for item in menu_items:
        item_dict[item.pk] = {
            'item': item,
            'children': [],
            'is_active': False,
            'is_parent_active': False,
        }


def forming_menu_tree(menu_items: List[TreeMenu],
                      item_dict: Dict[int, Dict],
                      menu_tree: List[Dict]
                      ) -> None:
    """ Формируем список меню из словаря и QuerySet """

    for item in menu_items:
        if item.parent:
            # если у item есть наследник, то добавляем его
            item_dict[item.parent.pk]['children'].append(item_dict[item.pk])
        else:
            menu_tree.append(item_dict[item.pk])


def get_active_item_tree(active_item: Optional[TreeMenu],
                         item_dict: Dict[int, Dict]
                         ) -> None:
    """ Отмечаем активные элементы и их родителей """

    if active_item:
        current = item_dict.get(active_item.pk)
        if current:
            current['is_active'] = True

            # Помечаем всех родителей как активные
            if active_item.parent:
                parent_id = active_item.parent.pk
                while parent_id:
                    parent = item_dict.get(parent_id)
                    if parent:
                        parent['is_parent_active'] = True
                        parent_id = parent['item'].parent_id
                    else:
                        break
