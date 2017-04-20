from odoo import models, fields, api


class Make(models.Model) :
    _name = "ostool.make"

    name = fields.Char(string="Marque", required=True)
