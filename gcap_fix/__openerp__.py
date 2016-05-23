# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Gcap FIX",
    'summary': """Система управления работой сервис-центра Gravicap""",

    'description': """
        Модуль для управления работой подразделения по ремонту электроники Gravicap
    """,

    'author': "TroLL",
    'website': "http://www.gravicap.com",
    'license ': 'Proprietary',

    'application': True,

    'category': 'FIX',
    'version': '0.2',

    'sequence': 21,

    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'gcap_base', 'report_aeroo', 'cron'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'view/user.xml',
        'view/gcap_fix_view.xml',

        'menu/gcap_fix_menu.xml',

        'reports/gcap_fix_report.xml',
    ],
}