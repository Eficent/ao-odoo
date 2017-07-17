# -*- coding: utf-8 -*-
# Copyright 2017 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'CRM Helpdesk',
    'category': 'Customer Relationship Management',
    'version': '10.0.1.0.0',
    'summary': "Helpdesk Management",
    'author': 'OpenERP SA, Eficent',
    'website': 'https://github.com/Eficent/ao-odoo',
    'license': 'AGPL-3',
    'depends': ['crm'],
    'data': [
        'views/crm_helpdesk_view.xml',
        'views/crm_helpdesk_menu.xml',
        'security/ir.model.access.csv',
        'report/crm_helpdesk_report_view.xml',
        'data/crm_helpdesk_data.xml',
    ],
    'demo': ['demo/crm_helpdesk_demo.xml'],
    'installable': True,
    'application': False,
}
