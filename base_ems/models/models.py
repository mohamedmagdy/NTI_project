# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
    _name = 'ems.course'
    _rec_name = 'name'
    _description = 'EMS Course'

    name = fields.Char(string="Course Name", required=True, )
    default_hours = fields.Integer(string="Default Hours", required=True, )
    log = fields.Html(string="Log", )
    is_package = fields.Boolean(string="Package", )
    child_ids = fields.Many2many(comodel_name="ems.course", relation="course_package_rel", column1="course_id",
                                 column2="child_ids", string="Child Courses", domain=[('is_package', '=', False)])
    type = fields.Selection(string="Type", selection=[('course', 'Course'), ('package', 'Package'), ], required=False, )

    _sql_constraints = [
        ('check_positive_default_hours', 'check(default_hours > 1)', "Default hours should be greater than 1.",)
    ]

    @api.onchange('is_package')
    def type_change(self):
        if not self.is_package:
            self.type = 'course'
        else:
            self.type = 'package'

    @api.onchange('child_ids')
    def _onchange_child_ids(self):
        y = 0
        for x in self.child_ids:
            y = y + x.default_hours
        self.default_hours = y


class Branch(models.Model):
    _name = 'ems.branch'
    _rec_name = 'name'
    _description = 'EMS Branch'

    sequence = fields.Char(string="ID", required=False, )
    name = fields.Char(string="Branch Name", required=True, )
    address = fields.Text(string="Address", required=False, )


class RoundType(models.Model):
    _name = 'ems.round.types'
    _rec_name = 'name'
    _description = 'EMS Round Type'

    name = fields.Char(string='Name', required=True)


class ReservationType(models.Model):
    _name = 'ems.reservation.types'
    _rec_name = 'name'
    _description = 'EMS Reservation Type'

    name = fields.Char(string='Name', required=True)


class EMSDaysOff(models.Model):
    _name = 'ems.days.off'
    _rec_name = 'name'
    _description = 'EMS Days Off'

    name = fields.Char(string="Name", required=True, )
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    notes = fields.Html(string="Notes", )


class EMSBranchLabs(models.Model):
    _name = 'ems.branch.labs'
    _rec_name = 'name'
    _description = 'EMS Branch Labs'

    name = fields.Char(string="Lab Name", required=False, )
    branch_id = fields.Many2one(comodel_name="ems.branch", string="Branch", required=True, )
    seats_count = fields.Integer(string="Seats Count", required=True, )

    _sql_constraints = [
        ('check_positive_seats_count', 'check(default_hours > 0)', "Default hours should be greater than 1."),
    ]


class Student(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    payment = fields.Selection(string="Payment Method", selection=[('cash', 'Cash'), ('bank', 'Bank Transfer'), ], required=False, )
    mobile = fields.Char(string="Mobile", required=False,)
    mail = fields.Char(string="E-mail", required=False,)