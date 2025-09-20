from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from datetime import date, timedelta



class ClinicDoctor(models.Model):
    _name = "clinic.doctor"
    _rec_name = "doctor_name"

    appointment_id = fields.One2many('patient.appointment', 'doctor_id')

    doctor_name = fields.Char("Doctor Name")