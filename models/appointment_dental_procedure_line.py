from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError




class DentalProcedureLine(models.Model):
    _name = "dental.procedure.line"

    patient_id = fields.Many2one(related="appointment_id.patient_id")
    appointment_id = fields.Many2one('patient.appointment', ondelete='cascade', required=False, index=True)
    tooth_no = fields.Selection([
        ('Tooth1', 'Tooth1'),
        ('Tooth2', 'Tooth2'),
        ('Tooth3', 'Tooth3'),
        ('Tooth4', 'Tooth4'),
        ('Tooth5', 'Tooth5'),
        ('Tooth6', 'Tooth6'),
        ('Tooth7', 'Tooth7'),
        ('Tooth8', 'Tooth8'),
        ('Tooth9', 'Tooth9'),
        ('Tooth10', 'Tooth10'),
        ('Tooth11', 'Tooth11'),
        ('Tooth12', 'Tooth12'),
        ('Tooth13', 'Tooth13'),
        ('Tooth14', 'Tooth14'),
        ('Tooth15', 'Tooth15'),
        ('Tooth16', 'Tooth16'),
        ('Tooth17', 'Tooth17'),
        ('Tooth18', 'Tooth18'),
        ('Tooth19', 'Tooth19'),
        ('Tooth20', 'Tooth20'),
        ('Tooth21', 'Tooth21'),
        ('Tooth22', 'Tooth22'),
        ('Tooth23', 'Tooth23'),
        ('Tooth24', 'Tooth24'),
        ('Tooth25', 'Tooth25'),
        ('Tooth26', 'Tooth26'),
        ('Tooth27', 'Tooth27'),
        ('Tooth28', 'Tooth28'),
        ('Tooth29', 'Tooth29'),
        ('Tooth30', 'Tooth30'),
        ('Tooth31', 'Tooth31'),
        ('Tooth32', 'Tooth32'),
        
    ], required=False, string="Tooth number", tracking=True)
    service_item_id = fields.Many2one('product.product', 'Procedure Name', domain=[('sale_ok', '=', True)], required=False, change_default=True)
    cost = fields.Float(related="service_item_id.lst_price", string='Procedure Cost', digits=0)
