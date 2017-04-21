# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Owner(models.Model) :
    _name = "ostool.owner"

    name = fields.Char(string="Société", required=True)
