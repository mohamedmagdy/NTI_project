# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Course(models.Model):
    _name = 'ems.course'
    _rec_name = 'name'
    _description = 'EMS Course'

    name = fields.Char(string="Course Name", required=True, )
    sequence = fields.Char(string="ID", required=False, )
    log = fields.Html(string="Log", )



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
    sequence = fields.Char(string='ID', required=False)


class ReservationType(models.Model):
    _name = 'ems.reservation.types'
    _rec_name = 'name'
    _description = 'EMS Reservation Type'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string='ID', required=False)
