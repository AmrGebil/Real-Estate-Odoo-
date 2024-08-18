from odoo import fields, models



class Owner(models.Model):
    _name = 'owner'

    name = fields.Char(string="Owner Name", required=True, size=20)
    phone = fields.Char(string="Owner Phone")
    adress = fields.Char(string="Owner Adress")