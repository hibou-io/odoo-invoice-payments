from openerp import models, fields, api
from openerp.tools import float_repr


class InvoicePayment(models.Model):
    _inherit = 'account.invoice'

    payment_options = fields.Text(compute='_payment_block')

    @api.multi
    def _payment_block(self):
        self.ensure_one()
        payment_acquirer = self.env['payment.acquirer']

        if self.type == 'out_invoice' and self.state not in ('draft', 'done') and not self.reconciled:
            self.payment_options = payment_acquirer.render_payment_block(self.number, self.residual, self.currency_id.id,
                partner_id=self.partner_id.id, company_id=self.company_id.id)
        else:
            self.payment_options = ''
        return self.payment_options

class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    def render_payment_block(self, cr, uid, reference, amount, currency_id, tx_id=None, partner_id=False, partner_values=None, tx_values=None, company_id=None, context=None):
        html_forms = []
        domain = [('website_published', '=', True)]
        if company_id:
            domain.append(('company_id', '=', company_id))
        acquirer_ids = self.search(cr, uid, domain, context=context)
        for acquirer_id in acquirer_ids:
            button = self.render(
                cr, uid, acquirer_id,
                reference, amount, currency_id,
                partner_id=partner_id, values=partner_values, context=context)
            html_forms.append(button)
        if not html_forms:
            return ''
        html_block = '\n'.join(filter(None, html_forms))
        return self._wrap_payment_block(cr, uid, html_block, amount, currency_id, context=context)

    def _wrap_payment_block(self, cr, uid, html_block, amount, currency_id, context=None):
        payment_header = 'Payment Methods for'
        amount_str = float_repr(amount, self.pool.get('decimal.precision').precision_get(cr, uid, 'Account'))
        currency = self.pool['res.currency'].browse(cr, uid, currency_id, context=context)
        currency_str = currency.symbol or currency.name
        amount = u"%s %s" % ((currency_str, amount_str) if currency.position == 'before' else (amount_str, currency_str))
        result = u"""<div class="payment_acquirers">
                         <div class="payment_header">
                             %s <span class="payment_amount">%s</span>
                         </div>
                         %%s
                     </div>""" % (payment_header, amount)
        return result % html_block.decode("utf-8")