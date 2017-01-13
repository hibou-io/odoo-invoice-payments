*******************************
Hibou - Ivoice Payments for v10
*******************************

Provides a way to get buttons to pay invoices using configured payment acquirers.

===
Use
===

There are two modules, that cannot be used simultaneously, to provide this behavior.

`invoice_payment`

* Creates a payment transaction for the full invoice amount.
* Will not move the invoice into the done state, and you will need to reconcile the payment externally
(e.g. from a bank statement)

`invoice_payment_auth`

* Creates a payment transaction for 0 amount to store a token.
* You can then use the token in the 'Register Payment' button to complete the invoice and journal entries.
* You can set the amount for the auth/capture per-acquirer in the System Parameters ('payment.auth.amount.{{ id }}')
e.g. when the acquirer needs 0.01 as the auth amount
* You may need to override the acquirer form to just auth to prevent capturing 0.01 on every try
* You may need to change your ACL's for Payment Tokens to be able to use them in the Register Payment wizard

Both use the 'website_published' field on the acquirer. If you don't have `website_payment` installed,
you can manually add that field to the acquirer form to configure.

If your acquirer doesn't work, it was probably changed afterwards.  Known to work with Authorize.net.

=======
Licence
=======

Please see `LICENSE <https://github.com/hibou-io/odoo-invoice-payments/blob/10.0/LICENSE>`_.

Copyright Hibou Corp. 2017
