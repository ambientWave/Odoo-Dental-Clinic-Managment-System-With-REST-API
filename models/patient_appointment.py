from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

from datetime import timedelta



class PatientAppointment(models.Model):
    _name = "patient.appointment"
    _inherit = ["mail.thread"]
    _rec_name = "appointment_serial"

    _description = "Patient Clinic Appointment"

    appointment_serial = fields.Char(string="Appointment Serial", required=True, copy=False, readonly=True, index=True, default=lambda self: _("New Appointment"))
    patient_id = fields.Many2one('patient.patient', string="Patient Name", tracking=True)
    contact_number = fields.Char('Contact Number', tracking=True)
    appointment_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Appointment Confirmed'),
        ('in_exam', 'Examination'),
        ('completed_exam', 'Examination Completed'),
        ('completed_appointment', 'Appointment Completed'),
        ('cancelled', 'Appointment Cancelled'),
    ], required=False, string="Appointment Status", tracking=True)

    appointment_type = fields.Selection([
        ('reserve', 'Reserved Appointment'),
        ('in_person', 'Walk-in Appointment'),
    ], required=False, string="Appointment Reservation Type", tracking=True)
    
    doctor_id = fields.Many2one('clinic.doctor', string="Doctor Name", tracking=True)

    procedure_line_id = fields.One2many('dental.procedure.line', 'appointment_id', string='Procedures')

    chief_complaints = fields.Text("Chief Complains/Notes")

    appointment_attachment_line_id = fields.One2many('appointment.attachment.line', 'appointment_id')

    patient_appointment_prescription_id = fields.One2many('patient.prescription', 'appointment_id')

    # attachment_line_id = fields.One2many('dental.procedure.line', 'appointment_id', string='Procedures')

    name = fields.Char('Meeting Subject', required=False)
    start = fields.Datetime(
        'Start', required=True, tracking=True, default=fields.Date.today,
        help="Start date of an event, without time for full days events")

    stop = fields.Datetime(
        'Stop', required=True, tracking=True, default=lambda self: fields.Datetime.today() + timedelta(hours=0.5),
        compute='_compute_stop', readonly=False, store=True,
        help="Stop date of an event, without time for full days events")
    
    allday = fields.Boolean('All Day', default=False)

    duration = fields.Float('Duration', compute='_compute_duration', store=True, readonly=False)

    user_id = fields.Many2one('res.users', string='Assistant Name', default=lambda self: self.env.user)

    @api.depends('start', 'duration')
    def _compute_stop(self):
        # stop and duration fields both depends on the start field.
        # But they also depends on each other.
        # When start is updated, we want to update the stop datetime based on
        # the *current* duration. In other words, we want: change start => keep the duration fixed and
        # recompute stop accordingly.
        # However, while computing stop, duration is marked to be recomputed. Calling `event.duration` would trigger
        # its recomputation. To avoid this we manually mark the field as computed.
        duration_field = self._fields['duration']
        self.env.remove_to_compute(duration_field, self)
        for event in self:
            # Round the duration (in hours) to the minute to avoid weird situations where the event
            # stops at 4:19:59, later displayed as 4:19.
            event.stop = event.start and event.start + timedelta(minutes=round((event.duration or 1.0) * 60))
            if event.allday:
                event.stop -= timedelta(seconds=1)
    
    def _get_duration(self, start, stop):
        """ Get the duration value between the 2 given dates. """
        if not start or not stop:
            return 0
        duration = (stop - start).total_seconds() / 3600
        return round(duration, 2)

    @api.depends('stop', 'start')
    def _compute_duration(self):
        for event in self.with_context(dont_notify=True):
            event.duration = self._get_duration(event.start, event.stop)

    @api.model
    def create(self, vals):  # save button in the form view

        if vals.get('appointment_serial', _('New Appointment')) == _('New Appointment'):
            vals['appointment_serial'] = self.env['ir.sequence'].next_by_code('patient.appointment.sequence') or _('New Appointment')
        res = super(PatientAppointment, self).create(vals)
        return res
    
    # allday = fields.Boolean('All Day', default=False)
    
    # attendee_status = fields.Selection(
    #     Attendee.STATE_SELECTION, string='Attendee Status', compute='_compute_attendee')
    # display_time = fields.Char('Event Time', compute='_compute_display_time')
    # start = fields.Datetime(
    #     'Start', required=True, tracking=True, default=fields.Date.today,
    #     help="Start date of an event, without time for full days events")
    # stop = fields.Datetime(
    #     'Stop', required=True, tracking=True, default=lambda self: fields.Datetime.today() + timedelta(hours=1),
    #     compute='_compute_stop', readonly=False, store=True,
    #     help="Stop date of an event, without time for full days events")

    # allday = fields.Boolean('All Day', default=False)
    # start_date = fields.Date(
    #     'Start Date', store=True, tracking=True,
    #     compute='_compute_dates', inverse='_inverse_dates')
    # stop_date = fields.Date(
    #     'End Date', store=True, tracking=True,
    #     compute='_compute_dates', inverse='_inverse_dates')
    # duration = fields.Float('Duration', compute='_compute_duration', store=True, readonly=False)
    # description = fields.Text('Description')
    # privacy = fields.Selection(
    #     [('public', 'Everyone'),
    #      ('private', 'Only me'),
    #      ('confidential', 'Only internal users')],
    #     'Privacy', default='public', required=True)
    # location = fields.Char('Location', tracking=True, help="Location of Event")
    # show_as = fields.Selection(
    #     [('free', 'Free'),
    #      ('busy', 'Busy')], 'Show Time as', default='busy', required=True)

    # # linked document
    # # LUL TODO use fields.Reference ?
    # res_id = fields.Integer('Document ID')
    # res_model_id = fields.Many2one('ir.model', 'Document Model', ondelete='cascade')
    # res_model = fields.Char(
    #     'Document Model Name', related='res_model_id.model', readonly=True, store=True)
    # activity_ids = fields.One2many('mail.activity', 'calendar_event_id', string='Activities')

    # #redifine message_ids to remove autojoin to avoid search to crash in get_recurrent_ids
    # message_ids = fields.One2many(auto_join=False)

    # user_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    # partner_id = fields.Many2one(
    #     'res.partner', string='Responsible Contact', related='user_id.partner_id', readonly=True)
    # active = fields.Boolean(
    #     'Active', default=True,
    #     help="If the active field is set to false, it will allow you to hide the event alarm information without removing it.")
    # categ_ids = fields.Many2many(
    #     'calendar.event.type', 'appointment_category_rel', 'event_id', 'type_id', 'Tags')
    # attendee_ids = fields.One2many(
    #     'calendar.attendee', 'event_id', 'Participant')
    
    # @api.model
    # def _default_partners(self):
    #     """ When active_model is res.partner, the current partners should be attendees """
    #     partners = self.env.user.partner_id
    #     active_id = self._context.get('active_id')
    #     if self._context.get('active_model') == 'res.partner' and active_id:
    #         if active_id not in partners.ids:
    #             partners |= self.env['res.partner'].browse(active_id)
    #     return partners
    
    # partner_ids = fields.Many2many(
    #     'res.partner', 'calendar_event_res_partner_rel',
    #     string='Attendees', default=_default_partners)
    # alarm_ids = fields.Many2many(
    #     'calendar.alarm', 'calendar_alarm_calendar_event_rel',
    #     string='Reminders', ondelete="restrict")
    # is_highlighted = fields.Boolean(
    #     compute='_compute_is_highlighted', string='Is the Event Highlighted')

    # # RECURRENCE FIELD
    # recurrency = fields.Boolean('Recurrent', help="Recurrent Event")
    # recurrence_id = fields.Many2one(
    #     'calendar.recurrence', string="Recurrence Rule", index=True)
    # follow_recurrence = fields.Boolean(default=False) # Indicates if an event follows the recurrence, i.e. is not an exception
    # recurrence_update = fields.Selection([
    #     ('self_only', "This event"),
    #     ('future_events', "This and following events"),
    #     ('all_events', "All events"),
    # ], store=False, copy=False, default='self_only',
    #    help="Choose what to do with other events in the recurrence. Updating All Events is not allowed when dates or time is modified")

    # # Those field are pseudo-related fields of recurrence_id.
    # # They can't be "real" related fields because it should work at record creation
    # # when recurrence_id is not created yet.
    # # If some of these fields are set and recurrence_id does not exists,
    # # a `calendar.recurrence.rule` will be dynamically created.
    # rrule = fields.Char('Recurrent Rule', compute='_compute_recurrence', readonly=False)
    # rrule_type = fields.Selection(RRULE_TYPE_SELECTION, string='Recurrence',
    #                               help="Let the event automatically repeat at that interval",
    #                               compute='_compute_recurrence', readonly=False)
    # event_tz = fields.Selection(
    #     _tz_get, string='Timezone', compute='_compute_recurrence', readonly=False)
    # end_type = fields.Selection(
    #     END_TYPE_SELECTION, string='Recurrence Termination',
    #     compute='_compute_recurrence', readonly=False)
    # interval = fields.Integer(
    #     string='Repeat Every', compute='_compute_recurrence', readonly=False,
    #     help="Repeat every (Days/Week/Month/Year)")
    # count = fields.Integer(
    #     string='Repeat', help="Repeat x times", compute='_compute_recurrence', readonly=False)
    # mo = fields.Boolean('Mon', compute='_compute_recurrence', readonly=False)
    # tu = fields.Boolean('Tue', compute='_compute_recurrence', readonly=False)
    # we = fields.Boolean('Wed', compute='_compute_recurrence', readonly=False)
    # th = fields.Boolean('Thu', compute='_compute_recurrence', readonly=False)
    # fr = fields.Boolean('Fri', compute='_compute_recurrence', readonly=False)
    # sa = fields.Boolean('Sat', compute='_compute_recurrence', readonly=False)
    # su = fields.Boolean('Sun', compute='_compute_recurrence', readonly=False)
    # month_by = fields.Selection(
    #     MONTH_BY_SELECTION, string='Option', compute='_compute_recurrence', readonly=False)
    # day = fields.Integer('Date of month', compute='_compute_recurrence', readonly=False)
    # weekday = fields.Selection(WEEKDAY_SELECTION, compute='_compute_recurrence', readonly=False)
    # byday = fields.Selection(BYDAY_SELECTION, compute='_compute_recurrence', readonly=False)
    # until = fields.Date(compute='_compute_recurrence', readonly=False)

    # def _compute_attendee(self):
    #     for meeting in self:
    #         attendee = meeting._find_my_attendee()
    #         meeting.attendee_status = attendee.state if attendee else 'needsAction'

    # def _compute_display_time(self):
    #     for meeting in self:
    #         meeting.display_time = self._get_display_time(meeting.start, meeting.stop, meeting.duration, meeting.allday)

    # @api.depends('start', 'duration')
    # def _compute_stop(self):
    #     # stop and duration fields both depends on the start field.
    #     # But they also depends on each other.
    #     # When start is updated, we want to update the stop datetime based on
    #     # the *current* duration. In other words, we want: change start => keep the duration fixed and
    #     # recompute stop accordingly.
    #     # However, while computing stop, duration is marked to be recomputed. Calling `event.duration` would trigger
    #     # its recomputation. To avoid this we manually mark the field as computed.
    #     duration_field = self._fields['duration']
    #     self.env.remove_to_compute(duration_field, self)
    #     for event in self:
    #         # Round the duration (in hours) to the minute to avoid weird situations where the event
    #         # stops at 4:19:59, later displayed as 4:19.
    #         event.stop = event.start and event.start + timedelta(minutes=round((event.duration or 1.0) * 60))
    #         if event.allday:
    #             event.stop -= timedelta(seconds=1)
    
    # @api.depends('stop', 'start')
    # def _compute_duration(self):
    #     for event in self.with_context(dont_notify=True):
    #         event.duration = self._get_duration(event.start, event.stop)

    # @api.depends('allday', 'start', 'stop')
    # def _compute_dates(self):
    #     """ Adapt the value of start_date(time)/stop_date(time)
    #         according to start/stop fields and allday. Also, compute
    #         the duration for not allday meeting ; otherwise the
    #         duration is set to zero, since the meeting last all the day.
    #     """
    #     for meeting in self:
    #         if meeting.allday and meeting.start and meeting.stop:
    #             meeting.start_date = meeting.start.date()
    #             meeting.stop_date = meeting.stop.date()
    #         else:
    #             meeting.start_date = False
    #             meeting.stop_date = False

    # @api.depends('recurrence_id', 'recurrency')
    # def _compute_recurrence(self):
    #     recurrence_fields = self._get_recurrent_fields()
    #     false_values = {field: False for field in recurrence_fields}  # computes need to set a value
    #     defaults = self.env['calendar.recurrence'].default_get(recurrence_fields)
    #     default_rrule_values = self.recurrence_id.default_get(recurrence_fields)
    #     for event in self:
    #         if event.recurrency:
    #             event.update(defaults)  # default recurrence values are needed to correctly compute the recurrence params
    #             event_values = event._get_recurrence_params()
    #             rrule_values = {
    #                 field: event.recurrence_id[field]
    #                 for field in recurrence_fields
    #                 if event.recurrence_id[field]
    #             }
    #             rrule_values = rrule_values or default_rrule_values
    #             event.update({**false_values, **event_values, **rrule_values})
    #         else:
    #             event.update(false_values)



