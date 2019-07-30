# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on sale",
    "version": "11.0.1.1.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Sales",
    "depends": ["sale", "mrp"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_view.xml",
        "views/report_saleorder.xml",
        "views/product_view.xml",
        "views/res_partner_view.xml",
        "report/ao_sale_report.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
