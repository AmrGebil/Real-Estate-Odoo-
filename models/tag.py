from odoo import fields, models



class Owner(models.Model):
    _name = 'tag'

    name = fields.Char(string="Tag Name", required=True, size=20)
