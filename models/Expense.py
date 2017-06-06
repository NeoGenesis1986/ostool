# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Expense(models.Model):
    _name = "ostool.expense"
    _order = "expense_date desc"

    name = fields.Char(string="Titre", required=True)
    description = fields.Text(string="Description")
    cost = fields.Float(string="Coût", digits=(15, 3), required=True)
    expense_date = fields.Date(string="Date", required=True, default=fields.Date.today())
    vehicule_id = fields.Many2one(
        string="Véhicule",
        index=True,
        comodel_name="ostool.vehicule",
        ondelete='restrict',
        required=True
    )
    driver_id = fields.Many2one(
        string="Chauffeur",
        index=True,
        comodel_name="ostool.driver",
        ondelete='restrict'
    )
