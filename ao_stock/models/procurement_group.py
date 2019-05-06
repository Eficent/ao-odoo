# Copyright 2019 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import re
from odoo import api, models

PG_PATTERN = r"^PG/[0-9]+"


class ProcurementGroup(models.Model):
    _inherit = "procurement.group"

    @api.model
    def run(self, product_id, product_qty, product_uom, location_id, name,
            origin, values):
<<<<<<< 9d97fd9a06af0bee81b983408b60cbb19378d290
<<<<<<< 118a2009a4b76d65d01001489c38745b23de6a64
=======
>>>>>>> Force only to change on orderpoint procurements
        if ('orderpoint_id' in values or 'orderpoint_ids' in values) and \
                name not in origin:
            if re.match(PG_PATTERN, origin):
                origin = re.sub(PG_PATTERN, name, origin)
<<<<<<< 9d97fd9a06af0bee81b983408b60cbb19378d290
=======
        if re.match(PG_PATTERN, origin):
            origin = re.sub(PG_PATTERN, name, origin)
>>>>>>> [11.0] Replace Generic PG/XXXX group (Stock Move) for its route name
=======
>>>>>>> Force only to change on orderpoint procurements
        return super(ProcurementGroup, self).run(product_id, product_qty,
                                                 product_uom, location_id,
                                                 name, origin, values)
