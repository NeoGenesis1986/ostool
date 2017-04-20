# -*- coding: utf-8 -*-
from odoo import http

# class Ostool(http.Controller):
#     @http.route('/ostool/ostool/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ostool/ostool/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ostool.listing', {
#             'root': '/ostool/ostool',
#             'objects': http.request.env['ostool.ostool'].search([]),
#         })

#     @http.route('/ostool/ostool/objects/<model("ostool.ostool"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ostool.object', {
#             'object': obj
#         })