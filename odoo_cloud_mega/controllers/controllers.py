# -*- coding: utf-8 -*-
# from odoo import http


# class OdooCloudMega(http.Controller):
#     @http.route('/odoo_cloud_mega/odoo_cloud_mega', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_cloud_mega/odoo_cloud_mega/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_cloud_mega.listing', {
#             'root': '/odoo_cloud_mega/odoo_cloud_mega',
#             'objects': http.request.env['odoo_cloud_mega.odoo_cloud_mega'].search([]),
#         })

#     @http.route('/odoo_cloud_mega/odoo_cloud_mega/objects/<model("odoo_cloud_mega.odoo_cloud_mega"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_cloud_mega.object', {
#             'object': obj
#         })
