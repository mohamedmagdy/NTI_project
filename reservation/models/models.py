# -*- coding: utf-8 -*-

from odoo import models, fields, api


class reservation(models.Model):
    _name = 'reservation.reservation'
    _rec_name = 'reservation_code'
    _description = 'New Description'

    reservation_code = fields.Char(string="ID", required=True, )
    select_course = fields.Many2one(comodel_name="ems.course", string="Select Course/Package Name", required=True, )
    select_round = fields.Many2one(comodel_name="ems.course.rounds", string="Select Round ", required=True, )
    select_round_status = fields.Many2one(comodel_name="ems.round.status", string="Select Round Status",
                                          required=True, )
    select_round_type = fields.Many2one(comodel_name="ems.round.types", string="Select Round Type", required=True, )
    log = fields.Html(string="Log", )
    # TODO:Round Days  :  related field = round.days
    # TODO:Sessions Count  :  related field = round.sessions_count
    # TODO:Start Date :  related field = round.start_date
    # TODO:End Date :  :  related field = round.end_date
    # TODO:Location :  related field = round.location
    # TODO:Round Time : related field = round.location
