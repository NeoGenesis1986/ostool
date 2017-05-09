# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Owner(models.Model):
    _name = "ostool.owner"
    _order = "name asc"

    name = fields.Char(string="Société", required=True)
    logo = fields.Binary(string="logo")

    vehicules_id = fields.One2many(
        comodel_name="ostool.vehicule",
        inverse_name="vehicule_model_id",
        string="Véhicules"
    )

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "Le nom du propriétaire doit être unique")]
