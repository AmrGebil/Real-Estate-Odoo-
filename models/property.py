from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'

    name = fields.Char(string="Property Name", required=True, size=10)
    description = fields.Text(string="Description")  # size attribute is not valid for Text field
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date of Availability")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price")
    bedroom = fields.Integer(string="Number of Bedrooms")
    living_area = fields.Integer(string="Living Area (sq m)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean(string="Has Garage?")
    garden = fields.Boolean(string="Has Garden?")
    garden_area = fields.Integer(string="Garden Area (sq m)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")
    owner_id = fields.Many2one('owner', string='Owner')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'This name already exists')
    ]

    @api.constrains('bedroom')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedroom < 0:
                raise ValidationError("Please add a valid number of bedrooms")

    # @api.model_create_multi
    # def create(self,vals):
    #     res = super(Property,self).create(vals)
    #     #logic
    #     print("create")
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search( domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     # logic
    #     print("read")
    #     return res
    #
    # @api.model
    # def write(self,vals):
    #     res = super(Property,self).write(vals)
    #     #logic
    #     print("write")
    #     return res
    #
    # @api.model
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     # logic
    #     print("delete")
    #     return res
