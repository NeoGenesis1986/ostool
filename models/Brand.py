# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Brand(models.Model):
    _name = 'ostool.brand'
    _order = 'name asc'

    name = fields.Char(string="Marque", required=True)
    logo = fields.Binary(string="Logo de la marque")
    vehicule_models_id = fields.One2many(
        comodel_name="ostool.vehicule_model",
        inverse_name="brand_id",
        string="Modèles"
    )
