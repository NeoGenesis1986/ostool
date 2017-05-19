# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Vehicule(models.Model):
    _name = "ostool.vehicule"
    _order = "name asc"

    name = fields.Char(string="Vehicule", required=True)
    license_plate = fields.Char(string="Matricule", required=True)
    image = fields.Binary(string="Photo", related="vehicule_model_id.logo")
    color = fields.Char(string="Couleur")
    seats = fields.Integer(string="Places")
    doors = fields.Integer(string="Portes")
    first_release_date = fields.Date(string="Mise en circulation")
    purchase_date = fields.Date(string="Date d'acquisistion")
    power = fields.Integer(string="Puissance")
    fiscal_power = fields.Integer(string="Puissance Fiscale")
    energy = fields.Selection(string="Carburant", selection=[
        ('petrol', 'Essence'),
        ('diesel', 'Gasoil'),
        ('gaz', 'Gaz'),
        ('electric', 'Electrique')
    ], default='petrol')
    transmission = fields.Selection(string="Transmission", selection=[
        ('manual', 'Manuelle'),
        ('automatic', 'Automatique')
    ], default='manual')
    gearbox_speeds = fields.Integer(string="Nombre de rapports")
    engine_volume = fields.Float(string="Cylindrée")
    state = fields.Selection(string="Etat", required=True, selection=[
        ('marche', 'En Marche'),
        ('panne', 'En Panne')
    ], default='marche')
    state_bool = fields.Boolean(compute="_state_bool")
    description = fields.Text(string="Description")
    brand = fields.Char(string="Marque", related="vehicule_model_id.brand_id.name")
    vehicule_model_id = fields.Many2one(
        string="Modèle",
        index=True,
        comodel_name='ostool.vehicule_model',
        ondelete='restrict',
        required=True
    )
    owner_id = fields.Many2one(
        string="Propriétaires",
        index=True,
        comodel_name="ostool.owner",
        ondelete='restrict',
        required=True
    )
    drivers_id = fields.Many2many(
        string="Chauffeurs",
        comodel_name="ostool.driver"
    )
    odometers_id = fields.One2many(
        comodel_name="ostool.odometer",
        inverse_name="vehicule_id",
        string="Lectures Kilométrage"
    )
    last_odometer_reading = fields.Char(string="Kilométrage", digit=(10, 0), compute="_last_odometer_reading")
    expenses_id = fields.One2many(
        comodel_name="ostool.expense",
        inverse_name="vehicule_id",
        string="Dépenses"
    )
    total_expenses = fields.Float(String="Total Dépenses", digits=(15, 3), compute="_total_expenses")

    _sql_constraints = [
        ('licence_unique', 'UNIQUE(licence_plate)', "Le matricule doit être unique"),
        ('name_unique', 'UNIQUE(name)', "Le matricule doit être unique")
    ]

    @api.one
    def toggle_state(self):
        if self.state == 'marche':
            self.state = 'panne'
        else:
            self.state = 'marche'
        return True

    @api.depends("state")
    def _state_bool(self):
        for v in self:
            v.state_bool = (v.state != 'panne')

    @api.depends("odometers_id")
    def _last_odometer_reading(self):
        for v in self:
            if v.odometers_id:
                v.last_odometer_reading = str(long(v.odometers_id[0].reading)) + " Km"
            else:
                v.last_odometer_reading = "N/A"

    @api.depends("expenses_id")
    def _total_expenses(self):
        for v in self:
            total = 0.0
            for expense in v.expenses_id:
                total += expense.cost
            v.total_expenses = total

    @api.one
    def last_odometer_reading_click(self):
        return True

    @api.one
    def total_expenses_click(self):
        return True
