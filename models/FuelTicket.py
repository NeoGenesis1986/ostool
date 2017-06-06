# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FuelTicket(models.Model):
    _name = "ostool.fuel_ticket"
    _order = "name asc"
    _rec_name = "display_name"

    name = fields.Float(string="Réference", required=True)
    display_name = fields.Char(string="Réference", compute="_display_name")
    validity = fields.Date(string="Validité", related="fuel_ticket_book_id.validity")
    value = fields.Float(string="Valeur", digit=(16, 3), required=True)
#    ticket_book_reference = fields.Char(string="Ref Carnet", related="fuel_ticket_book_id.name")
#    ticket_book_owner = fields.Char(string="Propriétaire", related="fuel_ticket_book_id.owner_id.name")
    state = fields.Selection(string="Utilisation", required="True", selection=[
        ('available', 'Disponible'),
        ('fuel', 'Consommation'),
        ('payment', 'Paiement'),
        ('lost', 'Perdu')
    ], default="available")
    vehicule_id = fields.Many2one(
        string="Véhicule",
        index=True,
        comodel_name="ostool.vehicule",
        ondelete='restrict'
    )
    driver_id = fields.Many2one(
        string="Chauffeur",
        index=True,
        comodel_name="ostool.driver",
        ondelete='restrict',
    )
    fuel_ticket_book_id = fields.Many2one(
        string="Carnet",
        index=True,
        comodel_name="ostool.fuel_tickets_book",
        ondelete='restrict',
        required=True
    )

    @api.depends('name')
    def _display_name(self):
        for ticket in self:
            ticket.display_name = str(long(ticket.name)).rjust(12, '0')
