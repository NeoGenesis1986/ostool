# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VehiculeModel(models.Model):
    _name = "ostool.vehicule_model"
    _order = "brand_id, name asc"

    name = fields.Char(string="Modèle", required=True)
    brand_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name="ostool.brand",
        string="Marque"
    )
    logo = fields.Binary(string="logo", related="brand_id.logo")
    vehicules_id = fields.One2many(
        comodel_name="ostool.vehicule",
        inverse_name="vehicule_model_id",
        string="Véhicules"
    )
