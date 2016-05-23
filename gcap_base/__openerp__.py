# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Gcap Base",
    'summary': """Базовые записи Gravicap""",

    'description': """
        В модуле хранятся общие записи и настройки для Gravicap
    """,

    'author': "TroLL",
    'website': "http://www.gravicap.ru",
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