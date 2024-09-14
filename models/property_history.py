from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property.history'
    _description = "Property History"

    user_id = fields.Many2one('res.users', string="User")
    property_id = fields.Many2one('property', string="Property")
    old_state = fields.Char(string="Old State")
    new_state = fields.Char(string="New State")
    reason = fields.Char(string="Reason")
    line_ids = fields.One2many('property.history.line', 'property_history_id', string="History Lines", ondelete='cascade')


class HistoryLine(models.Model):
    _name = 'property.history.line'
    _description = "Property History Lines"

    property_history_id = fields.Many2one('property.history', string="Property History", ondelete='cascade')
    area = fields.Integer(string="Area")
    description = fields.Text(string="Description")