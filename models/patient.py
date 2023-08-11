from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from datetime import date, timedelta



class Patient(models.Model):
    _name = "patient.patient"
    _inherit = ['mail.thread']
    _rec_name = "patient_name"

    patient_serial = fields.Char(string="Patient Serial", required=True, copy=False, readonly=True, index=True, default=lambda self: _("New Patient"))
    patient_name = fields.Char('Patient Name')
    contact_number = fields.Char('Contact Number', tracking=True)
    appointment_id = fields.One2many('patient.appointment', 'patient_id')
    date_of_birth = fields.Date(string='Date Of Birth', default=date.today())
    age = fields.Char(string='Age In Years', compute="compute_age", store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=False, string="Gender", tracking=True)
    occupation = fields.Char('Occupation')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
    ], required=False, string="Marital Status", tracking=True)
    blood_type = fields.Selection([
        ('a-', 'A without Rh-factor'),
        ('a+', 'A with Rh-factor'),
        ('b-', 'B without Rh-factor'),
        ('b+', 'B with Rh-factor'),
    ], required=False, string="Blood Typing", tracking=True)

    qstn_1 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),], required=False)
    qstn_1_note = fields.Char()
    qstn_2 = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No'),], required=False)
    qstn_2_note = fields.Char()

    patient_prescriptions = fields.One2many('patient.prescription', 'patient_id')



    @api.depends('date_of_birth')
    def compute_age(self):
        try:

            age = date.today() - self.date_of_birth
            age_in_years = age.days // 365.2425
            self.age = str(age_in_years) + "Years Old"
        except:
            pass
        
    @api.model
    def create(self, vals):  # save button in the form view

        if vals.get('patient_serial', _('New Patient')) == _('New Patient'):
            vals['patient_serial'] = self.env['ir.sequence'].next_by_code('patient.sequence') or _('New Patient')
        res = super(Patient, self).create(vals)
        return res
        # for rec in self:
        #     # todo don't forget to clarify that both two following variables are updated on
        #     # every change in sale order form
        #     sale_line_count = 0
        #     added_items_price_ordered_list = rec.order_line_id.mapped('price')
        #     added_items_quantity_ordered_list = rec.order_line_id.mapped('qty')

        #     item_price_multiplied_by_quantity = [price * qty for price, qty in
        #                                          zip(added_items_price_ordered_list, added_items_quantity_ordered_list)]
            
        #     sale_total_value = sum(item_price_multiplied_by_quantity)

            
        #     print(item_price_multiplied_by_quantity) # a list that contains each line subtotal
        #     print(rec.order_line_id.ids)
        #     rec.order_total = sale_total_value

