from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from datetime import date, timedelta

class PatientPrescription(models.Model):
    _name = "patient.prescription"

    prescription_serial = fields.Char(string="Prescription Serial", required=True, copy=False, readonly=True, index=True, default=lambda self: _("New Prescription"))
    prescription_date = fields.Date('Date Of Formulation', default=date.today())

    patient_id = fields.Many2one(related="appointment_id.patient_id")
    appointment_id = fields.Many2one('patient.appointment', invisible=True)
    appointment_id_name = fields.Char('Appointment Name', related='appointment_id.appointment_serial', readonly=True)
    prescription_line_id = fields.One2many("patient.prescription.line", "prescription_id")
    notes = fields.Text("Notes")

    @api.model
    def create(self, vals):  # save button in the form view

        if vals.get('prescription_serial', _('New Prescription')) == _('New Prescription'):
            vals['prescription_serial'] = self.env['ir.sequence'].next_by_code('patient.appointment.prescription.sequence') or _('New Prescription')
        res = super(PatientPrescription, self).create(vals)
        return res

                                      

class PatientPrescriptionLine(models.Model):
    _name = "patient.prescription.line"

    prescription_id = fields.Many2one('patient.prescription', invisible=True)
    prescription_id_name = fields.Char(related='prescription_id.prescription_serial', string='Prescription ID')
    medicine_trade_name = fields.Char(string="Trade Name of Medicine")
    therapeutic_regimen = fields.Char(string="Therapeutic Regimen of Medicine")

                                      