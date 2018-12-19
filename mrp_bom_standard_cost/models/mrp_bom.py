# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    standard_cost_total = fields.Float(
        string="Standard Cost (Total)",
        company_dependent=True,
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="Agregated standard cost of this BoM considering material,"
             "labor and overhead.",
    )
    standard_cost_material = fields.Float(
        string="Standard Cost (Material)",
        company_dependent=True,
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of all the materials and sub-assemblies used"
             "in this BoM.",
    )
    standard_cost_labor = fields.Float(
        string="Standard Cost (Labor)",
        company_dependent=True,
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of all the labor applied to this BoM",
    )
    standard_cost_overhead = fields.Float(
        string="Standard Cost (Overhead)",
        company_dependent=True,
        digits=dp.get_precision('Product Price'),
        groups="base.group_user",
        help="standard cost of overhead applied to this BoM.",
    )
    bom_cost_ids = fields.One2many(
        comodel_name="mrp.bom.cost",
        inverse_name="bom_id",
        string="Labor & Overhead",
        copy=True,
    )
