# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Insurance(models.Model):
    _name = "ostool.insurance"
    _order = "start_date desc"

    name = fields.Char(string="Réference", required=True)
    start_date = fields.Date(string="Date début", required=True)
    end_date = fields.Date(string="Date fin", required=True)
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
        for insurance in self:
            if insurance.end_date:
                insurance.expiration = (datetime.strptime(insurance.end_date, '%Y-%m-%d') - datetime.today()).days
