# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reservation(models.Model):
    _name = 'reservation.reservation'
    _rec_name = 'sequence'
    _description = 'Course Reservation'
    _inherit = 'mail.thread'

    # Initialize Database Fields
    sequence = fields.Char(string="ID", required=False, )
    select_course = fields.Many2one(comodel_name="ems.course", string="Select Course/Package", required=True,
                                    track_visibility="onchange")
    select_round_id = fields.Many2one(comodel_name="ems.course.round", string="Select Round ", required=True,
                                      track_visibility="onchange")
    select_round_status_id = fields.Many2one(comodel_name="ems.round.status", string="Select Round Status",
                                             required=True, track_visibility="onchange")
    select_round_type_id = fields.Many2one(comodel_name="ems.round.types", string="Select Round Type", required=True,
                                           track_visibility="onchange")
    source_of_knowing = fields.Char(string="Source Of Knowing", track_visibility="onchange", )
    payment_type = fields.Selection(string="Payment Type",
                                    selection=[('bank', 'Bank Transfer'), ('check', 'Check'), ('cash', 'Cash'), ],
                                    required=True, track_visibility="onchange", )
    student_id = fields.Many2one(comodel_name="res.partner", string="Student", required=True,
                                 track_visibility="onchange", )

    reservation_type = fields.Selection(string="Reservation Type",
                                        selection=[('schedule', 'Schedule'), ('waiting', 'Waiting List'),
                                                   ('online', 'Online'), ], required=False, )
    branch_lab_id = fields.Many2one(comodel_name="ems.branch.labs", string="Branch Labs", required=False, )
    seats = fields.Integer(string="Seats", required=False, relation='branch_lab_id.seats_count')

    # Initialize Related Fields With ems.course.round Table
    round_days = fields.Selection(string="Round Days", related="select_round_id.round_days")
    session_count = fields.Integer(string="Session count", related="select_round_id.sessions_count")
    start_date = fields.Date(string="Start Date", related="select_round_id.start_date")
    end_date = fields.Date(string="End Date", related="select_round_id.end_date")
    round_time = fields.Datetime(string="Round Time", related="select_round_id.from_time")

    # Create Sequence Function
    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('reservation.reservation')
        return super(Reservation, self).create(vals)
