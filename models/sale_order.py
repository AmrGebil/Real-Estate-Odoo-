from odoo import fields, models


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    property = fields.Many2one('property',string='Property')

    # def action_confirm(self):
    #     rec = super(SalesOrder, self).action_confirm()
    #     print("fff")
    #     return rec


