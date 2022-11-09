# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Payment Reminder Configs',
    'version' : '1.3',
    'summary': 'Payment Reminder Configuration',
    'sequence': 15,
    'description': """
====================
This Module Is For Pyament Reminder Configs

    """,
    'category': 'Payment Reminder/Payment Reminder',
    'website': 'https://www.odoo.com/app/Payment Reminder Configs',
    'depends' : ['base_setup','sale_management'],
    'data': ['security/ir.model.access.csv',
    'data/payment_reminder_sequence_data.xml',
    'data/payment_reminder_email_template.xml',
    'data/payment_reminder_cron.xml',
    'views/payment_reminder.xml',
    'views/sale_inherit_payment_reminder_views.xml',
    'views/sale_inherit_for_filter_views.xml',
    'report/sale_inherit_report.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
