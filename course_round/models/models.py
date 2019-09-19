from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError


class Round(models.Model):
    _name = 'ems.course.round'
    _rec_name = 'name'
    _description = 'Course Rounds'

    name = fields.Char(string="ID", required=False, default='New', readonly=True)
    course_id = fields.Many2one(comodel_name="ems.course", string="Course Name", required=True, )
    branch_id = fields.Many2one(comodel_name="ems.branch", string="Branch Location", required=True, )
    lab_id = fields.Many2one(comodel_name="ems.branch.labs", string="Lab", required=True,
                             domain="[('branch_id', '=', branch_id)]", )
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
    session_hours = fields.Float(string="Session Hours", required=True, default="1")
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", required=True, )
    from_time = fields.Float(string='Time From', required=True, default="10")
    to_time = fields.Float(string='Until', required=True, )
    state = fields.Selection(string="Status",
                             selection=[('tentative', 'Tentative'), ('confirm', 'Confirmed'), ('start', 'Started'),
                                        ('done', 'Done'), ('cancel', 'Canceled')], required=True, default="tentative", )
    instructor_id = fields.Many2one(comodel_name="ems.course.instructor", string="Instructor", required=True)
    course_type = fields.Selection(string="Course Type", selection=[('Course', 'Course'), ('Package', 'Package'), ],
                                   required=True, default="Course", )
    session_round_ids = fields.One2many(comodel_name="ems.course.session", inverse_name="round_id",
                                        string="Session", required=False, )
    sessions_count = fields.Integer(string="Session Count", required=False, )
    day_off_id = fields.Many2one(comodel_name="ems.days.off", string="", required=False, )
    week_day = fields.Integer(string="Start Day", required=False, )
    sub_course_ids = fields.Many2many(comodel_name="ems.course", relation="round_sub_course_rel", column1="round_id",
                                      column2="sub_course_id", string="Sub Courses", readonly=True)
    is_package = fields.Boolean(string="is package", default=False, )
    next_session = fields.Char(string="Next Session", compute='compute_next_session', )

    @api.depends('name')
    def compute_next_session(self):
        for rec in self:
            today = fields.Date.to_date(datetime.date.today())
            sessions = rec.env['ems.course.session'].search_read(
                domain=[('round_id', '=', rec.id), ('session_date', '>=', fields.Date.today())],
                fields=['session_date'], limit=1, order='session_date ASC')
            for session in sessions:
                if session['session_date'] == today:
                    rec.next_session = "Today"
                else:
                    rec.next_session = session['session_date']

    @api.onchange('course_id')
    # method to show only instructors allocated for a spacific course
    def _onchange_course_id(self):
        self.instructor_id = 0
        return {
            'value': {'sub_course_ids': self.course_id.child_ids},
        }

    # TODO: log interface

    @api.onchange('session_hours', 'course_hours')
    # method to calculate number of sessions
    def _onchange_session_count(self):
        self.sessions_count = self.course_hours / self.session_hours

    @api.onchange('sessions_count', 'start_date', 'round_days')
    # method to calculate end date
    def _onchange_end_date(self):
        if self.round_days in ['Saturday-tue', 'Sunday', 'Monday']:
            count_method = (self.sessions_count - 1) * 3.5
            self.end_date = self.start_date + datetime.timedelta(days=count_method)
        else:
            count_method = (self.sessions_count - 1) * 7
            self.end_date = self.start_date + datetime.timedelta(days=count_method)

    @api.onchange('session_hours', 'from_time')
    # method to calculate session end time
    def _onchange_to_time(self):
        self.to_time = self.from_time + self.session_hours

    @api.onchange('start_date', 'week_day')
    # method to get what day is it in start date
    def _get_week_day(self):
        self.week_day = self.start_date.weekday()

    @api.onchange('branch_id')
    # method to show only labs related to a specific branch
    def _lab_by_branch_id(self):
        self.lab_id = 0

    @api.onchange('course_id')
    # method to show only instructors related to a specific course
    def _lab_by_course_id(self):
        if self.course_type == 'Course':
            return {
                'domain': {'instructor_id': [('allowed_courses_ids', '=', self.course_id.id)]},
            }

    @api.onchange('sub_course_ids')
    # method to show only instructors related to a specific course
    def _lab_by_sub_course_ids(self):
        courses = []
        if self.course_type == 'Package':
            for course in self.sub_course_ids:
                courses.append(course.id)
            return {
                'domain': {'instructor_id': [('allowed_courses_ids', '=', courses)]},
            }

    @api.onchange('course_type')
    # method to show courses only or packages only
    def check_package(self):
        if self.course_type == 'Course':
            self.is_package = False
        else:
            self.is_package = True

    @api.onchange('course_id')
    # method to get the default hours per course
    def _get_course_hours(self):
        return {
            'value': {'course_hours': self.course_id.default_hours},
        }

    @api.one
    def check_tentative(self):
        self.state = 'tentative'

    @api.one
    def check_confirm(self):
        self.state = 'confirm'

    @api.one
    def check_start(self):
        self.state = 'start'

    @api.one
    def check_done(self):
        self.state = 'done'

    @api.one
    def check_cancel(self):
        self.state = 'cancel'

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
    def create(self, val):
        # method to create a sequence
        val['name'] = self.env['ir.sequence'].next_by_code('ems.course.round')
        return super(Round, self).create(val)

    @api.multi
    def create_sessions(self, vals):
        # create sessions corresponding to course hours and session hours
        vals['session_round_ids'] = []
        i = self.sessions_count
        x = 1
        calc_date = fields.Date.to_date(self.start_date)
        calc_dates = calc_date
        session_number = 1
        count_method = 0
        days_off = self.env['ems.days.off'].search_read(domain=[], fields=['start_date', 'end_date'])
        if len(self.session_round_ids) > 0:
            vals['session_round_ids'].append((5, 0, 0))
        while x <= i:
            o = 0
            if self.round_days in ['Saturday-tue', 'Sunday', 'Monday']:
                # to append sessions when there is 2 sessions per week
                if self.week_day in [5, 6, 0]:
                    # to append sessions when start_date = [Saturday or Sunday or Monday]
                    count_method = (x * 3.5)
                elif self.week_day in [1, 2, 3]:
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
                elif session_number <= self.sessions_count:
                    o = o + 1
                    if o == len(days_off):
                        vals['session_round_ids'].append(
                            (0, 0, {'session_date': calc_dates, 'hours': self.session_hours,
                                    'sequence': 'Sess-' + str(session_number),
                                    'session_instructor_id': self.instructor_id.id,
                                    'from_time_se': self.from_time,
                                    'to_time_se': self.to_time,
                                    'round_name': self.name}))
                        self.end_date = calc_dates
                        calc_dates = calc_date + datetime.timedelta(days=count_method)
                        session_number = session_number + 1
            x = x + 1
        return super(Round, self).write(vals)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s/ %s: %s" % (rec.name, rec.course_type, rec.course_id.name)))
        return result


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
    round_name = fields.Char(string="Round Name", required=True, default="RND", )
