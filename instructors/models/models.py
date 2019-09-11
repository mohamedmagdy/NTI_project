from odoo import api, fields, models
from datetime import datetime
from calendar import monthrange



class Instructor(models.Model):
    _name = 'ems.course.instructor'

    # @api.onchange('month')
    # def _get_month(self):
    #     today = datetime.today()
    #     current_month=(monthrange(today.year,int(self.month))[1])
    #     first_day= datetime(today.year,int(self.month),1)
    #     last_day= datetime(today.year,int(self.month),current_month)
    #     session_month =self.env['ems.course.session'].search([('session_date', '>=', first_day), ('session_date', '<=', last_day)])
    #     instructor_session = self.env['ems.course.round'].search(('instructor_', '=', first_day))
    #     self.no_of_session_date=len(session_month)



    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('ems.course.instructor')
        return super(Instructor, self).create(vals)

    @api.multi
    @api.constrains('hour_price', 'working_hours', 'age')
    def check_hours(self):
        # TODO: You can improve the code readability by using: all()
        if self.working_hours and self.hour_price and self.age:
            # FIXME: Wrong condition
            if (self.working_hours and self.hour_price) < 0:
                raise ValueError("The number of hours is invalid")
            if not (25 <= self.age <= 60):
                raise ValueError("The age is invalid")

    # def _check_instructor(self):
    #     self.count = self.env['instructor.availability'].search_count([('instructor_name_ids','in',self.id)])
    #
    # count = fields.Integer(string="", required=False, compute=_check_instructor)

    sequence = fields.Char(string="ID", required=False, )
    name = fields.Char(string="Instructor Name", required=True, )
    age = fields.Float(string="Age", required=False, )
    address = fields.Char(string="Address", required=False, )
    allowed_courses_ids = fields.Many2many(comodel_name="ems.course", relation="instructor_course_rel",
                                           column1="instructor_id", column2="course_id", string="Allowed courses", )
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", required=False, )
    hour_price = fields.Monetary(string="Hour price", currency_field="currency_id", )
    working_hours = fields.Float(string="Working hours per month", required=False, )
    allowed_branches_ids = fields.Many2many(comodel_name="ems.branch", relation="instructor_branch_rel",
                                            column1="instructor_id", column2="branch_id", string="Allowed Branches",
                                            required=True)
    # instructor_id = fields.Many2one(comodel_name="instructor.availability", string="Instructor", required=False, )
    # month = fields.Selection(string="", selection=[('1', 'Janurary'), ('2', 'Feburary'),('3', 'March'),
    #                                                ('4', 'April'),('5', 'May'),('6', 'June'),
    #                                                ('7', 'July'),('8', 'August'),('9', 'September'),
    #                                                ('10', 'October'),('11', 'November'),('12', 'December') ], default='1')
    # # todo
    # # assigned_hours_ids = fields.One2many(comodel_name="ems.course.session", inverse_name="", string="", required=False, )
    # no_of_session_date= fields.Integer(string="Number Of Session Date", required=False, compute=_get_month )



# class InstructorAllocation(models.Model):
#     _name = 'ems.courses.instructors.allocation'
#     _description = 'New Description'
#
#     @api.model
#     def create(self, vals):
#         vals['sequence'] = self.env['ir.sequence'].next_by_code('ems.courses.instructors.allocation')
#         return super(InstructorAllocation, self).create(vals)
#
#     @api.multi
#     @api.constrains('date_time_from','date_time_to')
#     def check_time(self):
#         for record in self:
#             same_day= record.fields.Datetime.date()
#             next_day= record.fields.Datetime.date()
#             if  (same_day != next_day):
#                 raise ValueError('Not the same Day!')
#
#     @api.multi
#     @api.constrains('date_time_from','date_time_to')
#     def check_date_validation(self):
#         if not (self.date_time_from.date() >= self.round_id.start_date and self.date_time_to.date() <= self.round_id.end_date):
#             raise ValueError("Time must be between start day and End Day")
#
#
#
#
#
#     sequence = fields.Char(string="ID", required=False, )
#     instructor = fields.Many2one(comodel_name="ems.course.instructor", string="Instructors allocation",
#                                  required=False, )
#
#
#     round_id = fields.Many2many(comodel_name="ems.course.round", relation="round_instructor_rel", column1="instructor_id", column2="round_id", string="Course Round", )
#     # round_id = fields.Many2one(comodel_name="ems.course.round", string="", required=False, )
#     course_id = fields.Many2one(comodel_name="ems.course", string="Course", required=False, )
#     date_time_from = fields.Datetime(string="Date Time From", required=False, )
#     date_time_to = fields.Datetime(string="Date Time To", required=False, )
#
#     # TODO: constraints

#
# class Instructor_Availability(models.Model):
#     _name = 'instructor.availability'
#
#
#     instructor_name_ids = fields.One2many(comodel_name="ems.course.instructor", inverse_name="instructor_id", string="Instructor Name", required=False, )
#     course_ids = fields.Many2many(comodel_name="ems.course", relation="", column1="", column2="", string="", )
#     start_date = fields.Date(string="Start Date", required=False, )
#     end_date = fields.Date(string="End Date", required=False, )
#     hour_from = fields.Float(string="",  required=False, )
#     hour_to = fields.Float(string="",  required=False, )
#



