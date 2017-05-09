# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Driver(models.Model):
    _name = 'ostool.driver'
    _order = 'name asc'

    name = fields.Char(string="Nom", required=True)
    avatar = fields.Binary(string="Photo")
    phone = fields.Char(string="Telephone")
    comments = fields.Text(string="Commentaires")
    vehicules_id = fields.Many2many(
        string="Véhicules",
        comodel_name="ostool.vehicule"
    )
