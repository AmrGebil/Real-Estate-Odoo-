# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Real Estate',
    'version': '17.0.0.1.0',
    'author': 'Amr Gebil',
    # 'category': '',
    'description': """module to learn odoo""",
    # 'website': '',
    # 'price': 60,
    # 'currency': 'EUR',
    'license': 'LGPL-3',
    'summary': 'module to learn odoo',
    'depends': ['base','sale_management','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/properties_view.xml',
        'views/building.xml',
        'views/sale_order.xml',
       'views/owner.xml',
       'views/tag.xml'
    ],
    'assets':{
        'web.assets_backend':['Real-Estate-Odoo-\static\src\property.css']

    },
    'application':True

}

