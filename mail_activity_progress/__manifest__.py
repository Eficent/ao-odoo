# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Mail Activity Progress",
    "version": "11.0.1.0.0",
    "author": "Eficent",
    "license": "LGPL-3",
    "category": "Discuss",
    "depends": [
        'mail',
        'mail_activity_board',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/mail_activity_progress_views.xml',
        'views/mail_activity_views.xml',
        'views/calendar_event_view.xml',
    ],
}
