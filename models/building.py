from odoo import models, fields, api


class Building(models.Model):
    _name = 'building'
    _description = "building"
    _inherit = ['mail.thread','mail.activity.mixin']
    


    name = fields.Char(string="Building Name", required=True, size=10)
    number = fields.Integer(string="Building Number")
    description = fields.Text(string="Description")
    code = fields.Integer(string="Building Code")
    active = fields.Boolean(default=True)