# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class Tax(models.Model):
    _name = 'ostool.tax'
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
        for tax in self:
            if tax.end_date:
                tax.expiration = (datetime.strptime(tax.end_date, '%Y-%m-%d') - datetime.today()).days
