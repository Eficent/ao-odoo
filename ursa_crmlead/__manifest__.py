# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Lead Set Reply-To",
    "version": "12.0.1.1.0",
    "author": "Ursa Information Systems, Eficent",
    "license": "AGPL-3",
    "category": "CRM",
    "summary": "Sets reply-to in the lead items",
    "website": "https://www.eficent.com",
    "depends": [
        "mail",
        "crm",
        "fetchmail",
    ],
    "data": [
        "views/crm_lead_view.xml",
        "data/crm_lead_config_data.xml",
        "views/crm_team_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
