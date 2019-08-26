from odoo import models, fields, api
import datetime


class Round(models.Model):
    _name = 'ems.course.round'
    _rec_name = 'sequence'
    _description = 'Describe Course Rounds '

    sequence = fields.Char(string="ID", required=True, )
    course_id = fields.Many2one(comodel_name="ems.course", string="Course ID", required=True, )
    location = fields.Many2one(comodel_name="ems.branch", string="Branch Location", required=True, )
    round_status = fields.Many2many(comodel_name="ems.course.round", relation="round_round_status_rel",
                                    column1="round_id", column2="round_status_id", string="Round Status",
                                    required=True)
    round_type = fields.Many2many(comodel_name="ems.course.round", relation="round_round_types_rel", column1="round_id",
                                  column2="round_status_id", string="Round Types", required=True)
    reservation_type = fields.Many2many(comodel_name="ems.course.round", relation="round__reservation_type_rel",
                                        column1="round_id", column2="reservation_type_id", string="Reservations",
                                        required=True)
    round_days = fields.Selection(string="Choose Days", selection=[('sat', 'Saturday Only'), ('fri', 'Friday Only'),
                                                                   ('sat-tue', 'Saturday-Tuesday'),
                                                                   ('sun-wed', 'Sunday-Wednesday'),
                                                                   ('mon-thu', 'Monday-Thursday')], required=True, )
    sessions_count = fields.Integer(string="Sessions Count", required=True, )
    start_date = fields.Date(string="Start Date", required=True, )
    end_date = fields.Date(string="End Date", required=True, )
    round_time = fields.Char(string="Round Time", required=False, )
    # instructor = fields.One2many(comodel_name="ems.course.instructors.allocation", inverse_name="", string="",
    # required=False, ) #inverse name
    state = fields.Selection(string="Status",
                             selection=[('draft', 'Draft'), ('confirm', 'Confirmed'), ('start', 'Started'),
                                        ('done', 'Done'), ('cancel', 'Canceled')], required=False, )
    trainee_id = fields.Many2one(comodel_name="res.partner", string="Trainee", required=False, )
    ref = fields.Reference(string="Reference", selection=[('hr.employee', 'Course'),
                                                          ('res.partner', 'Package')])

    @api.onchange('start_date', 'round_days', 'sessions_count')
    def _onchange_end_date(self):

        if self.start_date:
            if self.round_days == 'sat' or 'fri':
                countmethod = (self.sessions_count - 1) * 7
                self.end_date = self.start_date + datetime.timedelta(days=countmethod)
            else:
                countmethod = (self.sessions_count - 1) * 3.5
                self.end_date = self.start_date + datetime.timedelta(days=countmethod)

    _sql_constraints = [
        ('check_count', 'check(sessions_count > 0)', 'sessions count should be MORE THAN ZERO')
    ]
