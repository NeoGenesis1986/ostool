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
    ])
    transmission = fields.Selection(string="Transmission", selection=[
        ('manual', 'Manuelle'),
        ('automatic', 'Automatique')
    ])
    gearbox_speeds = fields.Integer(string="Nombre de rapports")
    engine_volume = fields.Float(string="Cylindrée")
    state = fields.Selection(string="Etat", required=True, default='marche', selection=[
        ('marche', 'En Marche'),
        ('panne', 'En Panne')
    ])
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
