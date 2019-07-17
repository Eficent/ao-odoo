# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on stock",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Warehouse Management",
    "depends": ["stock", "stock_inventory_exclude_sublocation"],
    "data": [
        # "security/ao_stock_security.xml",
        # "security/ir.model.access.csv",
        "views/stock_view.xml",
        "views/report_stockpicking_operations.xml",
        "views/report_stockinventory.xml",
        "views/report_deliveryslip.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
