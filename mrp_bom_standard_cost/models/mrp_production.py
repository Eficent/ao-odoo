# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    non_material_ids = fields.One2many(
        related="bom_id.bom_cost_ids",
        string="Labor & Overhead",
    )

    def _prepare_account_move_line_for_non_material(
            self, bom_cost_line, qty, credit_account_id, debit_account_id):
        """
        Generate the account.move.line values to post
        """
        self.ensure_one()
        valuation_amount = abs(bom_cost_line.product_id.standard_price) * qty

        # the standard_price of the product may be in another decimal
        # precision, or not compatible with the coinage of
        # the company currency... so we need to use round() before creating
        # the accounting entries.
        debit_value = self.company_id.currency_id.round(
            valuation_amount)

        # check that all data is correct
        if self.company_id.currency_id.is_zero(debit_value):
            raise UserError(_(
                "The cost of %s is currently equal to 0. Change the cost or "
                "the configuration of your product to avoid an incorrect "
                "valuation.") % (
                bom_cost_line.product_id.display_name,))
        credit_value = debit_value

        debit_line_vals = {
            'name': self.name,
            'product_id': bom_cost_line.product_id.id,
            'quantity': -1 * qty,
            'product_uom_id': bom_cost_line.product_uom_id.id,
            'debit': debit_value if debit_value > 0 else 0,
            'credit': -debit_value if debit_value < 0 else 0,
            'account_id': debit_account_id,
            'manufacture_order_id': self.id,
        }
        credit_line_vals = {
            'name': self.name,
            'product_id': bom_cost_line.product_id.id,
            'quantity': -1 * qty,
            'product_uom_id': bom_cost_line.product_uom_id.id,
            'credit': credit_value if credit_value > 0 else 0,
            'debit': -credit_value if credit_value < 0 else 0,
            'account_id': credit_account_id,
            'manufacture_order_id': self.id,
        }
        res = [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]
        return res

    def _create_account_move_line_non_materials(self, bom_cost_line, quantity):
        self.ensure_one()
        AccountMove = self.env['account.move']
        # Product quantity computed as the finished product qty to produce
        # times the qty needed for each finished product
        quantity = bom_cost_line.product_qty * quantity

        # Depending the cost type we use one account or the other
        cost_type = bom_cost_line.cost_type
        acc_labor, acc_overhead, journal_id = \
            bom_cost_line.product_id.product_tmpl_id\
            .get_accounting_data_for_non_material(
                cost_type)

        credit_account_id = acc_labor if cost_type == 'labor' else acc_overhead
        debit_account_id = self.production_location_id\
            .valuation_in_account_id.id or False

        if not debit_account_id:
            raise UserError(_(
                'Cannot find an account for the product location.'))

        # Create the account move lines
        move_lines = self._prepare_account_move_line_for_non_material(
            bom_cost_line, quantity,
            credit_account_id, debit_account_id)
        if move_lines:
            date = self._context.get('force_period_date',
                                     fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
            })
            new_account_move.post()
