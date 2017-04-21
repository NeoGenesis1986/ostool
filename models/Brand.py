# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Brand(models.Model) :
    _name = "ostool.brand"

    name = fields.Char(string="Marque", required=True)
