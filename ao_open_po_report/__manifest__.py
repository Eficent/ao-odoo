# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Héctor Villarreal Ortega
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Open Purchase Order Line Report",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Purchase",
    "depends": ["purchase",
                "account_invoicing",
                ],
    "data": [
        "views/purchase_order_line_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
