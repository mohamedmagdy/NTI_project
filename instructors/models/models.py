from odoo import api, fields, models
from datetime import  datetime


class Instructor(models.Model):
    _name = 'ems.course.instructor'

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('ems.course.instructor')
        return super(Instructor, self).create(vals)

    @api.multi
    @api.constrains('hour_price', 'working_hours', 'age')
    def check_hours(self):
        if self.working_hours and self.hour_price and self.age:
            if (self.working_hours and self.hour_price) < 0:
                raise ValueError("The number of hours is invalid")
            if not (25 <= self.age <= 60):
                raise ValueError("The age is invalid")

    sequence = fields.Char(string="ID", required=False, )
    name = fields.Char(string="Instructor Name", required=True, )
    age = fields.Float(string="Age", required=False, )
    address = fields.Char(string="Address", required=False, )
    allowed_courses_ids = fields.Many2many(comodel_name="ems.course", relation="instructor_course_rel",
                                           column1="instructor_id", column2="course_id", string="Allowed courses", )
    hour_price = fields.Float(string="Hour price", required=False, )
    working_hours = fields.Float(string="Working hours per month", required=False, )
    allowed_branches_ids = fields.Many2many(comodel_name="ems.branch", relation="instructor_branch_rel",
                                            column1="instructor_id", column2="branch_id", string="Allowed Branches",
                                            required=True)


class InstructorAllocation(models.Model):
    _name = 'ems.courses.instructors.allocation'
    _description = 'New Description'

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('ems.courses.instructors.allocation')
        return super(InstructorAllocation, self).create(vals)


    @api.multi
    @api.constrains('date_time_from','date_time_to')
    def check_time(self):
        for record in self:
            same_day= record.date_time_from.date()
            next_day= record.date_time_to.date()
            if not  (same_day == next_day):
                raise ValueError('Not the same Day!')

    @api.multi
    @api.constrains('date_time_from','date_time_to')
    def check_date_validation(self):
        if not (self.date_time_from.date() >= self.round_ids.start_date.date() and self.date_time_to.date() <= self.round_ids.end_date.date()):
            raise ValueError("Time must be between start day and End Day")





    sequence = fields.Char(string="ID", required=False, )
    instructor = fields.Many2one(comodel_name="ems.course.instructor", string="Instructors allocation",
                                 required=False, )


    # round_ids = fields.Many2many(comodel_name="ems.course.round", relation="round_instructor_rel", column1="instructor_id", column2="round_id", string="Course Round", )
    round_ids = fields.Many2one(comodel_name="ems.course.round", string="", required=False, )
    date_time_from = fields.Datetime(string="Date Time From", required=False, )
    date_time_to = fields.Datetime(string="Date Time To", required=False, )

    # TODO: constraints
