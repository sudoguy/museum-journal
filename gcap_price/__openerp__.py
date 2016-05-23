# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Gcap Price",
    'summary': """Система менеджмента прайс-листов для оптовых покупателей Gravicap""",

    'description': """
        Модуль для управления прайс-листами Gcap и их отображением
    """,

    'author': "TroLL",
    'website': "http://www.gravicap.com",
    'license ': 'Proprietary',

    'application': True,

    'category': 'Price',
    'version': '0.1',

    'sequence': 22,

    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'gcap_base', 'report_aeroo', 'cron'],

    # always loaded
    'data': [
#        'security/security.xml',
#        'security/ir.model.access.csv',
#        'view/gcap_price_view.xml',
        'menu/gcap_price_menu.xml',
#        'reports/gcap_price_report.xml',
    ],
}