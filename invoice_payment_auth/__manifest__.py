# -*- coding: utf-8 -*-

{
    'name': 'Payments (Token Auth) on Admin',
    'description': 'lets invoices display payment options for the sole purpose of obtaining a saved payment method '
                   'auth so that you can directly pay an invoice',
    'version': '1.0',
    'website': 'https://hibou.io/',
    'author': 'Hibou Corp. <hello@hibou.io>',
    'license': 'AGPL-3',
    'data': [
        'invoice_payment.xml',
    ],
    'category': 'Account',
    'depends': [
        'account',
        'payment',
    ],
}
