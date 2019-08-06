# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on CRM",
    "version": "11.0.1.0.3",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "CRM",
    "depends": ["crm",
                "crm_stage_type",
                "sales_team"],
    "data": [
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/crm_team_views.xml',
        'views/mail_templates.xml',
    ],
    "license": "AGPL-3",
    'installable': True,
}
