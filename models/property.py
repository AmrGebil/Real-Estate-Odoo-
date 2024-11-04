from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _description = "Property"
    _inherit = ['mail.thread','mail.activity.mixin']

    ref = fields.Char(default='New', readonly=True)
    name = fields.Char(string="Property Name", required=True, size=10)
    description = fields.Text(string="Description")  # size attribute is not valid for Text field
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date of Availability", tracking=1)
    expected_selling_date = fields.Date(string="Expected Selling Data", tracking=1)
    is_late = fields.Boolean(default=False)
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
        ('colsed', 'Closed')
    ], default='draft')
    owner_id = fields.Many2one('owner', string='Owner')
    owner_phone = fields.Char(related="owner_id.phone" ,readonly=0)
    owner_adress = fields.Char(related="owner_id.adress" ,readonly=0 )
    tag_ids = fields.Many2many('tag', string='Tags')
    lines_ids = fields.One2many('property.line', 'property_id' )
    active = fields.Boolean(default=True)


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
            rec.change_state(rec.state, 'draft',)
            rec.state = 'draft'
            # rec.write({
            #     'state':'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.change_state(rec.state, 'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.change_state(rec.state, 'sold')
            rec.state = 'sold'

    def action_colsed(self):
        for rec in self:
            rec.change_state(rec.state, 'colsed')
            rec.state = 'colsed'

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

    def _expected_selling_date_check(self):
        properties_ids=self.search([])
        for rec in properties_ids:
            if rec.state != 'sold':
                if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                    rec.is_late = True

    @api.model
    def create(self, vals):
        res = super(Property,self).create(vals)
        if res.ref == 'New':
            res.ref = self.env["ir.sequence"].next_by_code('property_sequence')
        return res

    def change_state(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                     'user_id': rec.env.uid,
                     "property_id": rec.id ,
                     'old_state': old_state,
                     "new_state": new_state,
                     "reason": reason or "",
                     "line_ids": [(0, 0, {'description': line.description, 'area': line.area})for line in rec.lines_ids]
              })

    def change_state_wizard(self):
        wizard = self.env['ir.actions.actions']._for_xml_id('Real_Estate_Odoo.change_state_action')
        wizard['context'] = {'default_property_id': self.id}
        return wizard

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('Real_Estate_Odoo.owner_action')
        view_id = self.env.ref('Real_Estate_Odoo.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action







    def action(self):
        #self.env.user
        #self.env.uid
        #self.env.company
        #self.env.context)
        #self.env.cr
        #self.env['owner']

       # self.env['owner'].create({
       #      'name':"owner one",
       #      "phone":'01151762358'
       #  })

       #self.env['owner'].search([])
       #self.env['owner'].search([('id', '=', 1)]).unlink()

       # self.env['owner'].search([('id', '=', 1)]).write({
        #         'name': "Amr one",
        #         'phone': '01151762358'
        #     })

        print(self.env['owner'].search([("id", "=", 1)]).write({
        'name': "Amr Gebil",
        'phone': '01151762358'
    }))

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