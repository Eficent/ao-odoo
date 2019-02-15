# Copyright 2018 Camptocamp SA
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class BomStandardCost(models.TransientModel):
    _name = "mrp.bom.standard.cost"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Starting Bill of Materials",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product Variant',
        domain="[('type', 'in', ['product', 'consu'])]",
        required=True,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
    )
    product_qty = fields.Float(
        related='bom_id.product_qty',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    product_uom_id = fields.Many2one(
        comodel_name="product.uom",
        related="bom_id.product_uom_id",
    )
    line_ids = fields.One2many(
        comodel_name='mrp.bom.standard.cost.line',
        inverse_name='explosion_id',
    )
    standard_cost_total = fields.Float(
        related='bom_id.standard_cost_total',
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_material = fields.Float(
        related='bom_id.standard_cost_material',
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_only_material = fields.Float(
        related='bom_id.standard_cost_only_material',
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_labor = fields.Float(
        related='bom_id.standard_cost_labor',
        digits=dp.get_precision('Product Price'),
    )
    standard_total_cost_labor = fields.Float(
        related='bom_id.standard_total_cost_labor',
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_overhead = fields.Float(
        related='bom_id.standard_cost_overhead',
        digits=dp.get_precision('Product Price'),
    )
    standard_total_cost_overhead = fields.Float(
        related='bom_id.standard_total_cost_overhead',
        digits=dp.get_precision('Product Price'),
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.bom_id = self.env['mrp.bom']._bom_find(
            product_tmpl=self.product_id,
        )

    @api.model
    def _prepare_line(self, bom_line, level, factor):
        return {
            'product_id': bom_line.product_id.id,
            'bom_line': bom_line.id,
            'bom_level': level,
            'product_qty': bom_line.product_qty * factor,
            'product_uom_id': bom_line.product_uom_id.id,
            'explosion_id': self.id,
            'standard_cost_only_material': bom_line.product_id.standard_price,
        }

    @api.multi
    def do_explode(self):
        self.ensure_one()
        line_obj = self.env['mrp.bom.standard.cost.line']

        def _create_lines(bom, level=0, factor=1):
            level += 1
            for line in bom.bom_line_ids:
                vals = self._prepare_line(line, level, factor)
                cost_line = line_obj.create(vals)
                bom = self.env['mrp.bom']._bom_find(product=line.product_id)
                if bom:
                    cost_line.write({
                        'standard_cost_material': bom.standard_cost_material,
                        'standard_cost_only_material':
                            bom.standard_cost_only_material,
                        'standard_cost_labor': bom.standard_cost_labor,
                        'standard_cost_overhead': bom.standard_cost_overhead,
                        'standard_total_cost_labor':
                            bom.standard_total_cost_labor,
                        'standard_total_cost_overhead':
                            bom.standard_total_cost_overhead,
                        'standard_cost_total': bom.standard_cost_total,
                    })
                    line_qty = line.product_uom_id._compute_quantity(
                        line.product_qty,
                        bom.product_uom_id,
                    )
                    new_factor = factor * line_qty / bom.product_qty
                    _create_lines(bom[0], level, new_factor)

        _create_lines(self.bom_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open lines',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'mrp.bom.standard.cost',
            'view_id': self.env.ref(
                'mrp_bom_standard_cost.mrp_bom_standard_cost_view_form2'
            ).id,
            'target': 'new',
            'res_id': self.id,
        }


class BomStandardCostLine(models.TransientModel):
    _name = "mrp.bom.standard.cost.line"

    explosion_id = fields.Many2one(
        comodel_name='mrp.bom.standard.cost',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product Variant',
        readonly=True,
    )
    bom_level = fields.Integer(
        string='BoM Level',
        readonly=True
    )
    product_qty = fields.Float(
        string='Product Quantity',
        readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
    )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Product Unit of Measure',
        readonly=True,
    )
    bom_line = fields.Many2one(
        comodel_name="mrp.bom.line",
        string="BoM line",
    )
    standard_cost_material = fields.Float(
        string='Standard Cost (Material)',
        readonly=True,
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_only_material = fields.Float(
        string='Standard Cost (Only Material)',
        readonly=True,
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_labor = fields.Float(
        string='Standard Cost (Labor)',
        readonly=True,
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_overhead = fields.Float(
        string='Standard Cost (Overhead)',
        readonly=True,
        digits=dp.get_precision('Product Price'),
    )
    standard_total_cost_labor = fields.Float(
        string='Standard Total Cost (Labor)',
        readonly=True,
        default=0.0,
        digits=dp.get_precision('Product Price'),
    )
    standard_total_cost_overhead = fields.Float(
        string='Standard Total Cost (Overhead)',
        readonly=True,
        default=0.0,
        digits=dp.get_precision('Product Price'),
    )
    standard_cost_total = fields.Float(
        string='Standard Total Cost',
        readonly=True,
        default=0.0,
        digits=dp.get_precision('Product Price'),
    )
