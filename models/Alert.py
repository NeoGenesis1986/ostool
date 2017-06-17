# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Alert(models.Model):
    _name = "ostool.alert"
    _order = "alert_date DESC"

    name = fields.Char(string="Titre", required=True)
    alert_date = fields.Date(string="Date", required=True)
    alert_level = fields.Selection(string="Niveau", selection=[
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('alert', 'Alerte')
    ], required=True)
    about = fields.Selection(string="A propos", selection=[
        ('insurance', 'Contrat d\'Assurance'),
        ('tax', 'Vignettes'),
        ('visit', 'Visite technique')
    ], required=True)
    description = fields.Text(string="Description")
    vehicule_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name="ostool.vehicule",
        string="Véhicule"
    )
