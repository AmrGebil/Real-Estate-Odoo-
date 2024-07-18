from odoo import models, fields


class Property(models.Model):
    _name ='property'

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availabilty = fields.Date()
    expect_price = fields.Float()
    selling_price = fields.Float()
    bedroom = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_oriantation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east', 'East'),
        ('west', 'West'),

    ])
