# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    balance_due = fields.Float(
        string="Invoiced", readonly=True, compute='_compute_balance_due',
        store=False
    )

    @api.multi
    def _compute_balance_due(self):
        to_compute = self.filtered(
            lambda r: r.state in ['purchase'])
        for rec in to_compute:
            if rec.invoice_lines:
                for invoice_line in rec.invoice_lines:
                    rec.balance_due += invoice_line.price_total
