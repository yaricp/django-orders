from django import template

from django.utils.translation import ugettext_lazy as _

register = template.Library()

top_menu_items = [{'url': "create_order",
                        'title': _(u"Create order")},

                    ]

top_menu_admin_items = [{'url': "create_type_work",
                            'title': _(u"Create type of works")},
                       ]


top_menu_order_items = [{'url': "order_detail",
                        'title': _(u"properties")},
                    {'url': "edit",
                        'title': _(u"edit")},
                    {'url': "applicants_book",
                        'title': _(u"applicants")}, ]


@register.inclusion_tag('tags/menu.html', takes_context=True)
def orders_top_menu(context):
    ob_list = top_menu_items
    if context['user'].is_superuser:
        ob_list = top_menu_items + top_menu_admin_items
    return {'object_list': ob_list}


@register.inclusion_tag('tags/menu.html', takes_context=True)
def top_order_menu(context):
    if (context['object'].client == context['user'] or context['user'].is_staff
         or context['user'].is_superuser):
        return {'object_list': top_menu_order_items}
    else:
        return {'object_list': None}


