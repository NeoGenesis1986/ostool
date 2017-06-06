# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Visit(models.Model):
    _name = 'ostool.visit'
    _order = 'end_date DESC'

    name = fields.Char(string="Réference", required=True)
    start_date = fields.Date(string="Date Début", required=True)
    end_date = fields.Date(string="Date Fin", required=True)
    amount = fields.Float(string="Montant", digits=(15, 3))
    expiration = fields.Integer(string="Jours restants", compute="_expiration")

    vehicule_id = fields.Many2one(
        required=True,
        index=True,
        comodel_name="ostool.vehicule",
        string="Véhicule"
    )

    @api.depends('end_date')
    def _expiration(self):
        for visit in self:
            if visit.end_date:
                visit.expiration = (datetime.strptime(visit.end_date, '%Y-%m-%d') - datetime.today()).days
