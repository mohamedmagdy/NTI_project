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
    allowed_branches_ids = fields.Many2many(comodel_name="ems.branch", relation="", column1="", column2="",
    hour_price = fields.Float(string="Hour price", required=False, )
    working_hours = fields.Float(string="Working hours per month", required=False, )
