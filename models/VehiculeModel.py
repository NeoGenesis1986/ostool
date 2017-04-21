# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VehiculeModel(models.Model) :
    _name = "ostool.vehicule_model"

    name = fields.Char(string="Modèle", required=True)
