# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Standard Cost",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Manufacturing",
    "depends": [
        "account_move_line_manufacture_info",
    ],
    "data": [
        "reports/templates/layouts.xml",
        "reports/report_mrpstandardcost.xml",
        "wizard/mrp_bom_standard_cost_report_view.xml",
        "views/mrp_bom_views.xml",
        "views/mrp_bom_cost_views.xml",
        "views/report_template.xml",
        "views/product_views.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
