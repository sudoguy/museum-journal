# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Museum Base",
    'summary': """Базовые записи""",

    'description': """
        В модуле хранятся общие записи и настройки для Museum
    """,

    'author': "sudoguy",
    'website': "",
    'license ': 'Proprietary',

    'application': False,

    'category': "Base",
    'version': '0.1',

    'sequence': 1,

    'auto_install': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data.xml',
    ],
}