# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class RmaOrderLine(models.Model):
    _inherit = "rma.order.line"

    helpdesk_id = fields.Many2one(
        string='Originating Helpdesk Ticket',
        comodel_name='crm.helpdesk', readonly=True,
        copy=False,
    )

    @api.model
    def create(self, vals):
        rma_line = super(RmaOrderLine, self).create(vals)
        if not rma_line.helpdesk_id:
            rma_line.helpdesk_id = rma_line.rma_id.originating_helpdesk_id or \
                                   False
        if rma_line.helpdesk_id:
            body = """%s created.
            <ul><li>Partner: %s</li>
            <li>Product: %s</li></ul>
            """ % (rma_line.name, rma_line.partner_id.name,
                   rma_line.product_id.name)
            rma_line.helpdesk_id.message_post(
                body=body, subtype='mail.mt_note')
        return rma_line
