# -*- coding: utf-8 -*-
from odoo import http

# class Reservation(http.Controller):
#     @http.route('/reservation/reservation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reservation/reservation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reservation.listing', {
#             'root': '/reservation/reservation',
#             'objects': http.request.env['reservation.reservation'].search([]),
#         })

#     @http.route('/reservation/reservation/objects/<model("reservation.reservation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reservation.object', {
#             'object': obj
#         })