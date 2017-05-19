# -*- coding: utf-8 -*-
{
    'name': "Ostool",

    'summary': """
        Gestion parc automobile.
        """,

    'description': """
        Module qui vise la gestion d'un parc automobile et ses dépenses.
    """,

    'author': "Khidma sarl",
    'website': "http://www.khidma.tn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Automobile',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/Driver.xml',
        'views/Brand.xml',
        'views/VehiculeModel.xml',
        'views/Owner.xml',
        'views/Vehicule.xml',
        'views/FuelTicketsBook.xml',
        'views/Menu.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True
}