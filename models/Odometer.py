# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Odometer(models.Model):
    _name = "ostool.odometer"
    _order = "reading_date desc"

    reading = fields.Float(string="Lecture", digits=(10, 0), required=True)
    reading_date = fields.Date(string="Date", required=True, default=fields.Date.today())
    vehicule_id = fields.Many2one(
        string="Véhicule",
        index=True,
        comodel_name="ostool.vehicule",
        ondelete='cascade',
        required=True
    )

    @api.constrains('reading')
    def _check_reading(self):
        if self.reading < 0:
            raise ValidationError("Le kilométrage ne peut pas être négatif.")
        return True

    @api.constrains('reading_date')
    def _check_reading_date(self):
        if datetime.strptime(self.reading_date, '%Y-%m-%d') > datetime.today():
            raise ValidationError("La date de lecture ne peut pas être supérieure à la date d'aujourdhui")
        return True
