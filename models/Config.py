# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Config(models.Model):
    _name = "ostool.config"

    responsible_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name="res.users",
        string="Résponsable parc automobile"
    )
    responsible_partner_id = fields.Integer(string="Partner ID", related="responsible_id.partner_id.id")
    alert_period = fields.Integer(string="Seuil d'alerte (jours)", default=30, required=True)
