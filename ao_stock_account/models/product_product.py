# Copyright 2018 Aleph Objects Inc.
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

import operator as py_operator

OPERATORS = {
    '<': py_operator.lt,
    '>': py_operator.gt,
    '<=': py_operator.le,
    '>=': py_operator.ge,
    '=': py_operator.eq,
    '!=': py_operator.ne
}


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_date_moved = fields.Datetime(
        compute='_compute_last_date_moved',
        search='_search_last_date_moved',
    )

    @api.multi
    def _compute_last_date_moved(self):
        last_move = {}
        self.env.cr.execute("""
            SELECT product_id, max(date) as last_move_date
            FROM stock_move
            GROUP BY product_id
        """)
        for product_id,  last_move_date in self.env.cr.fetchall():
            last_move[product_id] = last_move_date
        for rec in self:
            if rec.id in last_move.keys():
                rec.last_date_moved = last_move[rec.id]

    def _search_last_date_moved(self, operator, value):
        # to prevent sql injections
        if operator not in ('<', '>', '=', '!=', '<=', '>='):
            raise UserError(_('Invalid domain operator %s') % operator)
        if not isinstance(value, (str, bool)):
            raise UserError(_('Invalid domain right operand %s') % value)

        ids = []
        for product in self.with_context(prefetch_fields=False).search([]):
            if OPERATORS[operator](product['last_date_moved'], value):
                ids.append(product.id)
        return [('id', 'in', ids)]
