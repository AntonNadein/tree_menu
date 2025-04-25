from django import template
from django.urls import reverse, resolve, NoReverseMatch
from tree_menu.models import TreeMenu

register = template.Library()


@register.inclusion_tag('tree_menu/tags/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """ Отображение древовидного меню """

    request = context['request']
    current_url = request.path_info

    # Получаем все пункты меню за один запрос
    menu_items = TreeMenu.objects.filter(menu_name=menu_name)

    # Определяем активный пункт меню
    active_item = None
    for item in menu_items:
        try:
            item_url = item.get_url()
            # active_item = item
            if item_url == current_url:
                active_item = item
                break
        except NoReverseMatch:
            continue

    # Собираем дерево меню
    menu_tree = []
    item_dict = {}

    # Сначала создаем все элементы без детей
    for item in menu_items:
        item_dict[item.id] = {
            'item': item,
            'children': [],
            'is_active': False,
            'is_parent_active': False,
        }

    # Затем строим дерево
    for item in menu_items:
        if item.parent_id:
            item_dict[item.parent_id]['children'].append(item_dict[item.id])
        else:
            menu_tree.append(item_dict[item.id])

    # Помечаем активные элементы и их родителей
    if active_item:
        current = item_dict.get(active_item.id)
        if current:
            current['is_active'] = True

            # Помечаем всех родителей как активные
            parent_id = active_item.parent_id
            while parent_id:
                parent = item_dict.get(parent_id)
                if parent:
                    parent['is_parent_active'] = True
                    parent_id = parent['item'].parent_id
                else:
                    break

    fd = {
        'menu_tree': menu_tree,
        'menu_name': menu_name,
        'current_url': current_url,
    }
    return fd

