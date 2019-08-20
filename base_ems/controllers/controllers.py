# -*- coding: utf-8 -*-
from odoo import http

# class BaseEms(http.Controller):
#     @http.route('/base_ems/base_ems/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_ems/base_ems/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_ems.listing', {
#             'root': '/base_ems/base_ems',
#             'objects': http.request.env['base_ems.base_ems'].search([]),
#         })

#     @http.route('/base_ems/base_ems/objects/<model("base_ems.base_ems"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_ems.object', {
#             'object': obj
#         })