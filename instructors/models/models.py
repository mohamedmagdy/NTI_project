from odoo import api, fields, models


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
    # TODO: allowed couses M2M with ems.course
    allowed_couses_ids = fields.Many2many(comodel_name="ems.course", relation="instructor_course_rel",
                                     column1="instructor_id", column2="course_id",
                                     string="Allowed couses", )
    hour_price = fields.Float(string="Hour price", required=False, )
    working_hours = fields.Float(string="Working hours per month", required=False, )
    allowed_branches_ids = fields.Many2many(comodel_name="ems.branch", relation="instructor_branch_rel",
                                            column1="instructor_id", column2="branch_id", string="Allowed Branches",
                                            required=True)

class InstructorAllocation(models.Model):
    _name = 'ems.courses.instructors.allocation'
    _description = 'New Description'

    sequence = fields.Char(string="ID", required=False, )
    instructor = fields.Many2one(comodel_name="ems.course.instructor", string="Instructors allocation"
                                 , required=False, )

    round = fields.Many2one(comodel_name="ems.course.round", string="Round", required=False, )
    date_time_from = fields.Datetime(string="Date Time From", required=False, )
    date_time_to = fields.Datetime(string="Date Time To", required=False, )

    # TODO: constraints
        