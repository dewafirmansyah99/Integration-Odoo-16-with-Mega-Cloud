# -*- coding: utf-8 -*-
{
    'name': "Odoo Integrations with Mega",

    'summary': """
        This module has been integrated with the API from the https://mega.io/ website""",

    'description': """
        CRUD in MEGA from Odoo 16
    """,

    'author': "Dewa Firmansyah",
    'website': "https://github.com/dewafirmansyah99",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/check_files_views.xml',
        'views/login_user_views.xml',
        'views/upload_file_views.xml',
        'views/folder_name_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}
