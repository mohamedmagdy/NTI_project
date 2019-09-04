from odoo import models, fields, api
import datetime


class Round(models.Model):
    _name = 'ems.course.round'
    _rec_name = 'sequence'
    _description = 'Describe Course Rounds'

    sequence = fields.Char(string="ID", required=False, default='New', readonly=True)
    course_id = fields.Many2one(comodel_name="ems.course", string="Course ID", required=True, )
    branch_id = fields.Many2one(comodel_name="ems.branch", string="Branch Location", required=True, )
    lab_id = fields.Many2one(comodel_name="ems.branch.labs", string="Lab", required=False, )
    round_types_id = fields.Many2one(comodel_name="ems.round.types", string="Round Type", required=True, )
    reservation_type_ids = fields.Many2many(comodel_name="ems.reservation.types",
                                            relation="round__reservation_type_rel",
                                            column1="round_id", column2="reservation_type_id", string="Reservations",
                                            required=False)
    round_days = fields.Selection(string="Choose Days", selection=[('sat', 'Saturday Only'), ('fri', 'Friday Only'),
                                                                   ('sat-tue', 'Saturday-Tuesday'),
                                                                   ('sun-wed', 'Sunday-Wednesday'),
                                                                   ('mon-thu', 'Monday-Thursday')], required=True, )
    course_hours = fields.Integer(string="Course Hours", required=True, )
    session_hours = fields.Integer(string="Session Hours", required=False, default="1")
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", required=True, )
    from_time = fields.Datetime(string="Time From", required=True, default=fields.Datetime.now)
    to_time = fields.Datetime(string="Until", required=True, )
    # instructor_ids = fields.Many2many(comodel_name="ems.courses.instructors.allocation",
    # relation="round_instructor_rel",
    # column1="instructor_id", column2="round_id", string="Select Instructor", )
    state = fields.Selection(string="Status",
                             selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('start', 'Started'),
                                        ('done', 'Done'), ('cancel', 'Canceled')], required=False, )
    trainee_id = fields.Many2one(comodel_name="res.partner", string="Trainee", required=False, )
    ref = fields.Reference(string="Reference", selection=[('ems.course', 'Course'),
                                                          ('res.partner', 'Package')])
    session_round_ids = fields.One2many(comodel_name="ems.course.session", inverse_name="round_id",
                                        string="Session", required=False, )
    sessions_count = fields.Integer(string="Session Count", required=False, )

    # TODO: log interface

    @api.onchange('session_hours', 'course_hours')
    def _onchange_session_count(self):
        self.sessions_count = self.course_hours / self.session_hours
        print(self.sessions_count)

    @api.onchange('sessions_count', 'start_date', 'round_days')
    def _onchange_end_date(self):
        if self.round_days in ['sat-tue', 'sun-wed', 'mon-thu']:
            countmethod = (self.sessions_count - 1) * 3.5
            self.end_date = self.start_date + datetime.timedelta(days=countmethod)
        else:
            countmethod = (self.sessions_count - 1) * 7
            self.end_date = self.start_date + datetime.timedelta(days=countmethod)

    @api.onchange('session_hours', 'from_time')
    def _onchange_to_time(self):
        self.to_time = self.from_time + datetime.timedelta(hours=self.session_hours)

    _sql_constraints = [
        ('check_count', 'check(sessions_count > 0)', 'sessions count should be MORE THAN ZERO')
    ]

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('ems.course.round')
        vals['session_round_ids'] = []
        for i in range(vals['sessions_count']):
            calc_date = datetime.datetime.strptime(vals['start_date'], '%Y-%m-%d')
            if vals['round_days'] in ['sat-tue', 'sun-wed', 'mon-thu']:
                countmethod = (i * 3.5)
                calc_dates = calc_date + datetime.timedelta(days=countmethod)
            else:
                countmethod = (i * 7)
                calc_dates = calc_date + datetime.timedelta(days=countmethod)
            vals['session_round_ids'].append((0, 0, {'session_date': calc_dates, 'hours': vals['session_hours'],
                                                     'sequence': 'Sect-' + str(i + 1),
                                                     'instructor': vals['trainee_id']}))

        return super(Round, self).create(vals)


class Session(models.Model):
    _name = 'ems.course.session'
    _rec_name = 'round_id'
    _description = 'Describe Course Session'

    round_id = fields.Many2one(comodel_name="ems.course.round", string="Session", required=False, )
    sequence = fields.Char(string="ID", required=False, default='New', readonly=True)
    session_date = fields.Date(string="Session Date", required=False, comodel_name="ems.course.round", rel="start_date")
    instructor = fields.Selection(string="Instructor",
                                  selection=[('salah', 'Mohamed Salah'), ('essam', 'Mohamed Essam'), ],
                                  required=False, )
    hours = fields.Integer(string="Hours", required=False, )



