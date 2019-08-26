# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reservation(models.Model):
    _name = 'reservation.reservation'
    _rec_name = 'sequence'
    _description = 'Course Reservation'
    _inherit = 'mail.thread'

    reservation_code = fields.Char(string="ID", required=True,  track_visibility="onchange")
    select_course = fields.Many2one(comodel_name="ems.course", string="Select Course/Package Name", required=True,
                                    track_visibility="onchange")
    select_round = fields.Many2one(comodel_name="ems.course.round", string="Select Round ", required=True,
                                   track_visibility="onchange")
    select_round_status = fields.Many2one(comodel_name="ems.round.status", string="Select Round Status",
                                          required=True,  track_visibility="onchange")
    select_round_type = fields.Many2one(comodel_name="ems.round.types", string="Select Round Type", required=True,
                                        track_visibility="onchange")
    round_days = fields.Selection(string="Round Days", related="select_round.round_days", required=True,
                                  track_visibility="onchange")
    session_count = fields.Integer(string="Session count", related="select_round.sessions_count")
    start_date = fields.Date(string="Start Date", related="select_round.start_date")
    end_date = fields.Date(string="End Date", related="select_round.end_date")
    location = fields.Many2one(string="Location", related="select_round.location")
    round_time = fields.Char(string="Round Time", related="select_round.round_time")
