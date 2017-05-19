# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FuelTicketsBook(models.Model):
    _name = "ostool.fuel_tickets_book"
    _order = "name asc"

    name = fields.Float(string="Réference Carnet", digits=(15, 0), required=True)
    validity = fields.Date(string="Validité", required=True)
    owner_id = fields.Many2one(
        string="Propriétaire",
        index=True,
        comodel_name="ostool.owner",
        ondelete='restrict',
        required=True
    )
    fuel_tickets_id = fields.One2many(
        comodel_name="ostool.fuel_ticket",
        inverse_name="fuel_ticket_book_id",
        string="Bons de Carburants"
    )
    first_ticket_reference = fields.Float(string="Réference 1er Bon", digits=(15, 0), required=True)
    tickets_count = fields.Integer(string="Nb de Bons", required=True)
    ticket_value = fields.Float(string="Valeur du Bon de Carburant", digits=(15, 3), required=True)
    available_tickets_count = fields.Integer(string="Bons disponibles", compute="_available_tickets_count")
    available_tickets_value = fields.Float(string="Valeur bons disponibles", digits=(15, 3), compute="_available_tickets_value")
    str_name = fields.Char(string="Réference", compute="_str_name")

    _sql_constraints = [('name_unique', 'UNIQUE(name)', "La réference du carnet de bons de carburants doit être unique")]

    @api.constrains('tickets_count')
    def _check_tickets_count(self):
        if self.tickets_count <= 0:
            raise ValidationError("Le nombre de bon de carburant doit être > 0")
        return True

    @api.depends('fuel_tickets_id')
    def _available_tickets_count(self):
        for ticket_book in self:
            count = 0
            for ticket in ticket_book.fuel_tickets_id:
                if ticket.state == "available":
                    count += 1
            ticket_book.available_tickets_count = count

    @api.depends('fuel_tickets_id')
    def _available_tickets_value(self):
        for ticket_book in self:
            count = 0
            for ticket in ticket_book.fuel_tickets_id:
                if ticket.state == "available":
                    count += 1
            ticket_book.available_tickets_value = count

    @api.depends('name')
    def _str_name(self):
        for ticket_book in self:
            ticket_book.str_name = str(long(ticket_book.name)).rjust(12, '0')

    @api.multi
    def create(self, vals):
        rec = super(FuelTicketsBook, self).create(vals)
        for i in range(0, vals.get('tickets_count')):
            self.env['ostool.fuel_ticket'].create({
                'name': vals.get('first_ticket_reference') + i,
                'value': vals.get('ticket_value'),
                'fuel_ticket_book_id': rec.id
            })
        return True
