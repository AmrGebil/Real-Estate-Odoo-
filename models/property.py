from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = "Property"
    _inherit = ['mail.thread','mail.activity.mixin']


    name = fields.Char(string="Property Name", required=True, size=10)
    description = fields.Text(string="Description")  # size attribute is not valid for Text field
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date of Availability", tracking=1)
    expected_price = fields.Float(string="Expected Price", required=True, tracking=1)
    selling_price = fields.Float(string="Selling Price", tracking=1)
    diff = fields.Integer(string="differance Price", compute='_compute_diff')
    bedroom = fields.Integer(string="Number of Bedrooms", tracking=1)
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

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='draft')
    owner_id = fields.Many2one('owner', string='Owner')
    owner_phone = fields.Char(related="owner_id.phone" ,readonly=0)
    owner_adress = fields.Char(related="owner_id.adress" ,readonly=0 )
    tag_ids = fields.Many2many('tag', string='Tags')
    lines_ids = fields.One2many('property.line', 'property_id' )


    _sql_constraints = [
        ('name_unique', 'unique(name)', 'This name already exists')
    ]

    @api.constrains('bedroom')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedroom <= 0:
                raise ValidationError("Please add a valid number of bedrooms")


    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
            # rec.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.state = 'sold'

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('diff')
    def warning(self):
        for rec in self:
            if rec.diff < 0:
                return{
                    'warning':{ 'title':'warning' , 'message':'he value of differance peice is negative','type':'notification '}
                }
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

class PropertyLine(models.Model):
    _name = "property.line"

    property_id = models.fields.Many2one('property')
    area = fields.Integer(string="Area")
    description = fields.Text(string="Description")