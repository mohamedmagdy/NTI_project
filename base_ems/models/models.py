# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
    _name = 'ems.course'
    _rec_name = 'name'
    _description = 'EMS Course'

    name = fields.Char(string="Course Name", required=True, )
    default_hours = fields.Integer(string="Default Hours", required=True, )
    sequence = fields.Char(string="ID", required=False, )
    log = fields.Html(string="Log", )
    is_package = fields.Boolean(string="Package", )
    child_ids = fields.One2many(comodel_name="ems.course", inverse_name="parent_id", string="Child Courses",
                                domain=[('is_package', '=', False)] )
    parent_id = fields.Many2one(comodel_name="ems.course", string="Parent Course", required=False, )

    _sql_constraints = [
        ('check_positive_default_hours', 'check(default_hours > 1)', "Default hours should be greater than 1.",)
    ]


class Branch(models.Model):
    _name = 'ems.branch'
    _rec_name = 'name'
    _description = 'EMS Branch'

    sequence = fields.Char(string="ID", required=False, )
    name = fields.Char(string="Branch Name", required=True, )
    address = fields.Text(string="Address", required=False, )


class Round(models.Model):
    _name = 'ems.round.status'
    _rec_name = 'name'
    _description = 'EMS Round'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='ID', required=False)


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
