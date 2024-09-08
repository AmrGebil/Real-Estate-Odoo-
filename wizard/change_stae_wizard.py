from odoo import fields, models


class ChangeState(models.TransientModel):
    _name = 'change.state'

    property_id = fields.Many2one('property', string="Property")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
    ], default='draft')

    reason = fields.Char(string="Reason")

    def action_confirm(self):
        if self.property_id.state == 'colsed':
            self.property_id.state = self.state
            self.property_id.change_state('colsed', self.state, self.reason)





