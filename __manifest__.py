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
      'security/groups.xml',
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/properties_view.xml',
        'views/building.xml',
        'views/sale_order.xml',
        'views/owner.xml',
        'views/properties_history_view.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
        'views/tag.xml',
        'data/sequence.xml'
    ],
    'assets':{
        'web.assets_backend': ['Real_Estate_Odoo\static\src\property.css'],
        'web.report_assets_common': ['Real_Estate_Odoo\static\src\css\ font.css']

    },
    'application':True

}

