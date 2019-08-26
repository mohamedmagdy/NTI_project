# -*- coding: utf-8 -*-
from odoo import http

# class Instructors(http.Controller):
#     @http.route('/instructors/instructors/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/instructors/instructors/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('instructors.listing', {
#             'root': '/instructors/instructors',
#             'objects': http.request.env['instructors.instructors'].search([]),
#         })

#     @http.route('/instructors/instructors/objects/<model("instructors.instructors"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('instructors.object', {
#             'object': obj
#         })