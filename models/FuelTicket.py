# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FuelTicket(models.Model):
    _name = "ostool.fuel_ticket"
    _order = "name asc"
    _rec_name = "display_name"

    name = fields.Float(string="Réference", required=True)
    display_name = fields.Char(string="Réference", compute="_display_name")
    validity = fields.Date(string="Validité", related="fuel_ticket_book_id.validity")
    value = fields.Float(string="Valeur", digit=(16, 3), required=True)
    # ticket_book_reference = fields.Char(string="Ref Carnet", related="fuel_ticket_book_id.name")
    # ticket_book_owner = fields.Many2one(string="Propriétaire", related="fuel_ticket_book_id.owner_id")
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


class TransientFuelTicket(models.TransientModel):
    _name = "ostool.transient_fuel_ticket"

    vehicule_id = fields.Many2one(
        string="Véhicule",
        index=True,
        comodel_name="ostool.vehicule",
        required=True
    )
    fuel_ticket_id = fields.Many2many(
        required=True,
        string="Bons de carburants",
        comodel_name="ostool.fuel_ticket",
        domain=[
            ('state', '=', 'available')
        ]
    )
    driver_id = fields.Many2one(
        string="Chauffeur",
        index=True,
        comodel_name="ostool.driver",
        required=True
    )

    @api.multi
    def affect_fuel_ticket(self):
        self.ensure_one()
        if not self.fuel_ticket_id:
            raise ValidationError("Vous devez sélectionner au moins un bon de carburant!")
        for transient_ticket in self.fuel_ticket_id:
            ticket = self.env['ostool.fuel_ticket'].browse(transient_ticket.id)
            ticket.write({
                'vehicule_id': self.vehicule_id.id,
                'driver_id': self.driver_id.id,
                'state': 'fuel'
            })
        return True
