# -*- coding: utf-8 -*-

{
    'name': 'Payments on Admin',
    'description': 'lets invoices display payment options, mostly a back port from v8',
    'version': '1.0',
    'website': 'https://hibou.io/',
    'author': 'Hibou Corp. <hello@hibou.io>',
    'license': 'AGPL-3',
    'data': [
        'views/invoice_payment.xml',
    ],
    'category': 'Account',
    'depends': [
        'account',
        'payment',
    ],
}
