# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Reservation(models.Model):
    _name = 'reservation.reservation'
    _rec_name = 'sequence'
    _description = 'Course Reservation'
    _inherit = 'mail.thread'

    # Initialize Database Fields And Initialize Related Fields
    sequence = fields.Char(string="Reservation Code", required=True, track_visibility="onchange", )
    reservation_type = fields.Selection(string="Reservation Type",
                                        selection=[('schedule', 'Schedule'), ('waiting', 'Waiting List'),
                                                   ('online', 'Online'), ], required=True,
                                        track_visibility="onchange", )
    select_course_id = fields.Many2one(comodel_name="ems.course", string="Select Course/Package", required=True,
                                       track_visibility="onchange", )
    select_round_id = fields.Many2one(comodel_name="ems.course.round", string="Select Round", required=True,
                                      track_visibility="onchange", )
    branch_id = fields.Many2one(comodel_name="ems.branch", string="Branch", related="select_round_id.branch_id",
                                track_visibility="onchange", )
    branch_lab_id = fields.Many2one(comodel_name="ems.branch.labs", string="Branch Labs",
                                    related="select_round_id.lab_id", track_visibility="onchange", )
    seats = fields.Integer(string="Seats", related='branch_lab_id.seats_count', track_visibility="onchange", )
    select_round_type_id = fields.Many2one(comodel_name="ems.round.types", string="Round Type",
                                           related="select_round_id.round_types_id",
                                           track_visibility="onchange", )
    round_days = fields.Selection(string="Round Days", related="select_round_id.round_days",
                                  track_visibility="onchange", )
    session_count = fields.Integer(string="Session count", related="select_round_id.sessions_count",
                                   track_visibility="onchange", )
    start_date = fields.Date(string="Start Date", related="select_round_id.start_date", track_visibility="onchange", )
    end_date = fields.Date(string="End Date", related="select_round_id.end_date", track_visibility="onchange", )
    round_time = fields.Float(string="Round Time", related="select_round_id.from_time",
                                 track_visibility="onchange", )
    student_id = fields.Many2one(comodel_name="res.partner", string="Student", required=True,
                                 track_visibility="onchange", )
    payment_type = fields.Selection(string="Payment Type",
                                    selection=[('bank', 'Bank Transfer'), ('check', 'Check'), ('cash', 'Cash'), ],
                                    required=True, track_visibility="onchange", )
    source_of_knowing = fields.Char(string="Source Of Knowing", track_visibility="onchange", )
    report_print_counter = fields.Integer(string="Print Counter", copy=False, )
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.user, track_visibility="onchange")

    # Create Sequence Function
    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('reservation.reservation')
        return super(Reservation, self).create(vals)

    #   Reset Select Round Selection
    @api.onchange('select_course_id')
    def reset_select(self):
        self.select_round_id = False

    #   Increase Print Reservation Number
    @api.multi
    def print_xreport(self):
        self.report_print_counter += 1
