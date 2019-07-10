# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

UNIT = dp.get_precision('Product Price')


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def _compute_bom_standard_cost(self):
        bom_obj = self.env['mrp.bom']
        for template in self:
            template.bom_standard_cost = 0.0
            price = 0.0
            for variant in template.product_variant_ids:
                bom = bom_obj._bom_find(product=variant)
                if bom:
                    price = bom.standard_cost_total
                else:
                    price = template.standard_price
            template.bom_standard_cost = price

    bom_standard_cost = fields.Float(string='Standard cost of BOM',
                                     compute='_compute_bom_standard_cost',
                                     digits=UNIT)
