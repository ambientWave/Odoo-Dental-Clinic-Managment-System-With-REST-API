from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, timedelta


class AppointmentAttachmentLine(models.Model):
    _name = "appointment.attachment.line"



    appointment_id = fields.Many2one('patient.appointment', 'appointment_attachment_line_id')
    attachment_deposition_date = fields.Date('Date Of Deposition', default=date.today())
    file = fields.Binary(string='File Name')