# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Driver(models.Model):
    _name = 'ostool.driver'
    _order = 'name asc'

    name = fields.Char(string="Nom", required=True)
    avatar = fields.Binary(string="Photo")
    phone = fields.Char(string="Télephone")
    comments = fields.Text(string="Commentaires")
    vehicules_id = fields.Many2many(
        string="Véhicules",
        comodel_name="ostool.vehicule"
    )
    expenses_id = fields.One2many(
        comodel_name="ostool.expense",
        inverse_name="driver_id",
        string="Dépenses"
    )
    fuel_tickets_id = fields.One2many(
        comodel_name="ostool.fuel_ticket",
        inverse_name="driver_id",
        string="Bons de carburant"
    )
    total_expenses = fields.Float(String="Total Dépenses", digits=(15, 3), compute="_total_expenses")

    @api.depends("expenses_id")
    def _total_expenses(self):
        for v in self:
            total = 0.0
            for expense in v.expenses_id:
                total += expense.cost
            v.total_expenses = total
