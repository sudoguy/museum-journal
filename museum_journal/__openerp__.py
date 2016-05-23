# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Museum Journal",
    'summary': """Система управления работой музея им. Сурикова""",

    'description': """
        Модуль для ведения учета посетителей
    """,

    'author': "sudoguy",
    'website': "http://www.surikov-museum.ru",
    'license ': 'Proprietary',

    'application': True,

    'category': 'journal',
    'version': '0.2',

    'sequence': 21,

    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['museum_base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'view/museum_journal_view.xml',

        'menu/museum_journal_menu.xml',
    ],
}