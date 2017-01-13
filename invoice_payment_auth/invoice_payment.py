from odoo import models, fields, api


class InvoicePayment(models.Model):
    _inherit = 'account.invoice'

    payment_options = fields.Text(compute='_payment_block')

    @api.multi
    def _payment_block(self):
        if len(self) != 1:
            for r in self:
                r.payment_options = ''
            return
        self.ensure_one()
        payment_acquirers = self.env['payment.acquirer'].sudo().search([('website_published', '=', True)])
        PaymentTransaction = self.env['payment.transaction'].sudo()

        if self.type == 'out_invoice' and self.state not in ('draft', 'done') and not self.reconciled:
            self.payment_options = ''
            payment_options = ''
            for acquirer in payment_acquirers:
                reference = self.number + '-by-' + str(acquirer.id)
                amount = self._get_auth_amount(acquirer.id)
                txn = PaymentTransaction.search([('reference', '=', reference)])
                values = {
                    'amount': amount,
                    'acquirer_id': acquirer.id,
                    'currency_id': self.currency_id.id,
                    'reference': reference,
                    'partner_id': self.partner_id.id,
                    'partner_name': self.partner_id.name,
                    'partner_country_id': self.partner_id.country_id.id,
                }
                if len(txn) > 0 and (txn[0].state == 'error' or txn[0].state == 'cancel'):
                    txn[0].unlink()
                    PaymentTransaction.create(values)
                elif len(txn) == 0:
                    PaymentTransaction.create(values)

                payment_options += acquirer.sudo().render(
                    reference,
                    amount,
                    self.currency_id.id,
                    partner_id=self.partner_id.id)

            self.payment_options = payment_options
        else:
            self.payment_options = ''
        return self.payment_options

    def _get_auth_amount(self, id):
        config = self.env['ir.config_parameter'].sudo()
        key = 'payment.auth.amount.' + str(id)

        amount_config = config.search([('key', '=', key)])
        if not amount_config:
            amount_config = config.create({'key': key, 'value': '0.00'})
        return float(amount_config.value)
