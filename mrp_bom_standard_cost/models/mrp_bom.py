# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    standard_cost_total = fields.Float(
        string="Standard Cost (Total)",
        compute='compute_costs',
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="Agregated standard cost of this BoM considering material,"
             "labor and overhead.",
    )
    standard_cost_material = fields.Float(
        string="Standard Cost (Material)",
        compute="compute_costs",
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of all the materials and sub-assemblies used"
             "in this BoM.",
    )
    standard_cost_only_material = fields.Float(
        string="Standard Cost (Only Material)",
        compute="compute_costs",
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of taking into account only materials.",
    )
    standard_cost_labor = fields.Float(
        string="Standard Cost (Labor)",
        compute='compute_non_material_costs',
        store=True,
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of all the labor applied to this BoM",
    )
    standard_total_cost_labor = fields.Float(
        string="Aggregate Cost (Labor)",
        compute='compute_costs',
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard total cost of all the labor applied to this BoM"
             "and BoM's included inside this one",
    )
    standard_cost_overhead = fields.Float(
        string="Standard Cost (Overhead)",
        compute='compute_non_material_costs',
        store=True,
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of overhead applied to this BoM.",
    )
    standard_total_cost_overhead = fields.Float(
        string="Aggregate Cost (Overhead)",
        compute='compute_costs',
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard total cost of all the overhead applied to this BoM"
             "and BoM's included inside this one",
    )
    bom_cost_ids = fields.One2many(
        comodel_name="mrp.bom.cost",
        inverse_name="bom_id",
        string="Labor & Overhead",
    )

    @api.multi
    @api.depends('bom_line_ids')
    def compute_costs(self):
        for bom in self:
            bom.standard_cost_material, \
                bom.standard_cost_only_material, \
                bom.standard_total_cost_labor, \
                bom.standard_total_cost_overhead \
                = bom.get_bom_standard_material_cost()
            # Compute total cost adding materials, labor and overhead
            bom.standard_cost_total = bom.standard_cost_material + \
                bom.standard_cost_labor + \
                bom.standard_cost_overhead

    def get_bom_standard_material_cost(self):
        """Computes in a recursive way the costs (total, materials, labor
            and overhead) of a BoM taking into account all the components """

        # Initialization of variables
        total = 0.0
        materials = 0.0
        labor = self.standard_cost_labor
        overhead = self.standard_cost_overhead
        starting_factor = self.product_uom_id._compute_quantity(
            self.product_qty, self.product_tmpl_id.uom_id,
            round=False)
        # Iterate over all the lines in the current BoM
        for line in self.bom_line_ids:
            # If the a component is manufactured we continue exploding.
            bom = self._bom_find(product=line.product_id)
            if bom:
                sub_total, sub_materials, sub_labor, sub_overhead = \
                    bom.get_bom_standard_material_cost()
                # We update values taking into account the quantity defined
                # in the BoM line
                cost = sub_total + bom.standard_cost_labor + \
                    bom.standard_cost_overhead
                total += line.product_qty * cost
                materials += line.product_qty * sub_materials
                labor += line.product_qty * sub_labor
                overhead += line.product_qty * sub_overhead
            else:
                total += line.product_qty * line.product_id.standard_price
                materials += line.product_qty * line.product_id.standard_price
        return starting_factor * total, starting_factor * \
            materials, starting_factor * labor, starting_factor * overhead

    @api.multi
    @api.depends('bom_cost_ids')
    def compute_non_material_costs(self):
        for bom in self:
            labor_cost = 0.0
            overhead_cost = 0.0
            for bom_cost in bom.bom_cost_ids:
                qty = bom_cost.product_qty
                if bom_cost.cost_type == 'labor':
                    labor_cost += bom_cost.product_id.standard_price * qty
                else:
                    overhead_cost += bom_cost.product_id.standard_price * qty
            bom.standard_cost_labor = labor_cost
            bom.standard_cost_overhead = overhead_cost

    def run_recompute_costs(self):
        self.compute_non_material_costs()
        self.compute_costs()
