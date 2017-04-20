from odoo import models, fields, api


class Driver(models.Model) :
    _name = "ostool.driver"

    name = fields.Char(string="Nom", required=True)
