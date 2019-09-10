from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError


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
    round_days = fields.Selection(string="Choose Days",
                                  selection=[('Saturday', 'Saturday Only'), ('Friday', 'Friday Only'),
                                             ('Saturday-tue', 'Saturday-Tuesday'),
                                             ('Sunday', 'Sunday-Wednesday'),
                                             ('Monday', 'Monday-Thursday')], required=True, )
    course_hours = fields.Integer(string="Course Hours", required=True, )
    session_hours = fields.Float(string="Session Hours", required=False, default="1")
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", required=True, )
    from_time = fields.Float(string='Time From', required=True, )
    to_time = fields.Float(string='Until', required=True, )
    state = fields.Selection(string="Status",
                             selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('start', 'Started'),
                                        ('done', 'Done'), ('cancel', 'Canceled')], required=False, )
    instructor_id = fields.Many2one(comodel_name="ems.course.instructor", string="Instructor", )
    ref = fields.Reference(string="Reference", selection=[('ems.course', 'Course'),
                                                          ('res.partner', 'Package')])
    session_round_ids = fields.One2many(comodel_name="ems.course.session", inverse_name="round_id",
                                        string="Session", required=False, )
    sessions_count = fields.Integer(string="Session Count", required=False, )
    day_off_id = fields.Many2one(comodel_name="ems.days.off", string="", required=False, )
    week_day = fields.Integer(string="Start Day", required=False, )

    # TODO: log interface

    @api.onchange('session_hours', 'course_hours')
    def _onchange_session_count(self):
        # method to calculate number of sessions
        self.sessions_count = self.course_hours / self.session_hours

    @api.onchange('sessions_count', 'start_date', 'round_days')
    def _onchange_end_date(self):
        # method to calculate end date
        if self.round_days in ['Saturday-tue', 'Sunday', 'Monday']:
            count_method = (self.sessions_count - 1) * 3.5
            self.end_date = self.start_date + datetime.timedelta(days=count_method)
        else:
            count_method = (self.sessions_count - 1) * 7
            self.end_date = self.start_date + datetime.timedelta(days=count_method)

    @api.onchange('session_hours', 'from_time')
    def _onchange_to_time(self):
        # method to calculate session end time
        self.to_time = self.from_time + self.session_hours

    @api.onchange('start_date', 'week_day')
    def _get_week_day(self):
        # method to get what day is it in start date
        self.week_day = self.start_date.weekday()

    @api.onchange('branch_id')
    def _lab_by_branch_id(self):
        # method to show only labs related to a specific branch
        return {
            'domain': {'lab_id': [('branch_id', '=', self.branch_id.id)]},
        }

    @api.onchange('course_id')
    def _get_course_hours(self):
        # method to get the default hours per course
        return {
            'value': {'course_hours': self.course_id.default_hours},
        }

    _sql_constraints = [
        ('check_count', 'check(sessions_count > 0)', 'sessions count should be MORE THAN ZERO'),
    ]

    @api.constrains('round_days')
    def _check_round_days(self):
        # constrains on start_date
        if self.round_days in ['Saturday']:
            if not self.week_day == 5:
                raise ValidationError('Start Date Should be Saturday')
        elif self.round_days == 'Friday':
            if not self.week_day == 4:
                raise ValidationError('Start Date Should be Friday')
        elif self.round_days == 'Sunday':
            if self.week_day not in [6, 2]:
                raise ValidationError('Start Date Should be Sunday or Wednesday')
        elif self.round_days == 'Monday':
            if self.week_day not in [0, 3]:
                raise ValidationError('Start Date Should be Monday or Thursday')
        elif self.round_days in ['Saturday-tue']:
            if self.week_day not in [5, 1]:
                raise ValidationError('Start Date Should be Saturday or Tuesday')

    @api.model
    def create(self, vals):
        # method to create a sequence for round and also create sessions corresponding to course hours and session hours
        vals['sequence'] = self.env['ir.sequence'].next_by_code('ems.course.round')
        vals['session_round_ids'] = []
        i = vals['sessions_count']
        x = 1
        _calc_date = datetime.datetime.strptime(vals['start_date'], '%Y-%m-%d')
        calc_date = _calc_date.date()
        calc_dates = calc_date
        session_number = 1
        count_method = 0
        days_off = self.env['ems.days.off'].search_read(domain=[], fields=['start_date', 'end_date'])
        while x <= i:
            o = 0
            if vals['round_days'] in ['Saturday-tue', 'Sunday', 'Monday']:
                # to append sessions when there is 2 sessions per week
                if vals['week_day'] in [5, 6, 0]:
                    # to append sessions when start_date = [Saturday or Sunday or Monday]
                    count_method = (x * 3.5)
                elif vals['week_day'] in [1, 2, 3]:
                    # to append sessions when start_date = [Tuesday or Wednesday or Thursday]
                    if x % 2 == 0:
                        count_method = (x * 3.5)
                    else:
                        count_method = (x * 3.5) + 1
            else:
                # to append sessions when there is 1 sessions per week
                count_method = (x * 7)
            for z in days_off:
                if z['start_date'] <= calc_dates <= z['end_date']:
                    calc_dates = calc_date + datetime.timedelta(days=count_method)
                    i = i + 1
                else:
                    o = o + 1
                    if o == len(days_off):
                        vals['session_round_ids'].append(
                            (0, 0, {'session_date': calc_dates, 'hours': vals['session_hours'],
                                    'sequence': 'Sect-' + str(session_number),
                                    'session_instructor_id': vals['instructor_id'],
                                    'from_time_se': vals['from_time'],
                                    'to_time_se': vals['to_time']}))
                        vals['end_date'] = calc_dates
                        calc_dates = calc_date + datetime.timedelta(days=count_method)
                        session_number = session_number + 1
            x = x + 1
        return super(Round, self).create(vals)


class Session(models.Model):
    _name = 'ems.course.session'
    _rec_name = 'round_id'
    _description = 'Describe Course Session'

    round_id = fields.Many2one(comodel_name="ems.course.round", string="Session", required=False, )
    sequence = fields.Char(string="ID", required=False, default='New', readonly=True)
    session_date = fields.Date(string="Session Date", required=False, comodel_name="ems.course.round", rel="start_date")
    session_instructor_id = fields.Many2one(comodel_name="ems.course.instructor", string="Instructor", required=False, )
    hours = fields.Integer(string="Hours", required=False, )
    from_time_se = fields.Float(string='From', required=True, )
    to_time_se = fields.Float(string='To', required=True, )
