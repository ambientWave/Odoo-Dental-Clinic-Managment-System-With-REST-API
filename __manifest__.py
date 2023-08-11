# -*- coding: utf-8 -*-

{
    'name': 'Dental Clinic Mangement System',
    'version': '1.0',
    'sequence': -101,
    'category': 'Accounting/Accounting',
    'summary': 'Management',
    'description': """Helping you to insure a great experience""",
    'depends': ['base', 'account' ,'calendar', 'sales_team', 'payment', 'portal', 'utm', 'sale', 'mail', 'crm', 'l10n_co',
                'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'data/data.xml',
        # 'wizard/remove_invoice_views.xml',
        'views/appointment_view.xml',
        'views/patient_view.xml',
        'views/backend.xml',
        'views/Patient_Appointment_Form_view_customization.xml',
        # 'views/inventory_stock.xml',
        # 'report/report_sale_receipt_template.xml',
        # 'report/report.xml',
             ],
    'qweb': [
        'static/src/xml/toothChart.xml',
            ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
