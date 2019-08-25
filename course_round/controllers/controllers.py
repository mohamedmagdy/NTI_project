# -*- coding: utf-8 -*-
from odoo import http

# class CourseRound(http.Controller):
#     @http.route('/course_round/course_round/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/course_round/course_round/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('course_round.listing', {
#             'root': '/course_round/course_round',
#             'objects': http.request.env['course_round.course_round'].search([]),
#         })

#     @http.route('/course_round/course_round/objects/<model("course_round.course_round"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('course_round.object', {
#             'object': obj
#         })