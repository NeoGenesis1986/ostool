# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Vehicule(models.Model):
    _name = "ostool.vehicule"
    _order = "name asc"

#    _inherit = ["mail.thread"]

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
    insurances_id = fields.One2many(
        comodel_name="ostool.insurance",
        inverse_name="vehicule_id",
        string="Contrats d'assurance"
    )
    taxes_id = fields.One2many(
        comodel_name="ostool.tax",
        inverse_name="vehicule_id",
        string="Vignettes"
    )
    visits_id = fields.One2many(
        comodel_name="ostool.visit",
        inverse_name="vehicule_id",
        string="Visites Techniques"
    )
    fuel_tickets_id = fields.One2many(
        comodel_name="ostool.fuel_ticket",
        inverse_name="vehicule_id",
        string="Bons de carburant"
    )

    _sql_constraints = [
        ('licence_unique', 'UNIQUE(license_plate)', "Le matricule doit être unique"),
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

    def _cron_check_insurance_expiration_date(self):
        # print "insurance cron in"
        vehicules_ids = self.search([])
        config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
        if not config:
            raise UserError("Configuration Introuvable")
        config = config[0]
        alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        about = 'insurance'
        for v_id in vehicules_ids:
            alert = False
            name = u""
            description = u""
            insurances = self.env['ostool.insurance'].search_read([('vehicule_id', '=', v_id.id)], ['expiration'], order='end_date DESC')
            v = self.browse(v_id.id)
            if insurances:
                expiration = insurances[0].get('expiration')
                if expiration <= 0:
                    alert = True
                    alert_type = 'alert'
                    name = u"Expiration"
                    description = u"Le contrat d'assurance du véhicule '" + v.name + u"' est expiré."
                elif expiration <= alert_period:
                    alert = True
                    alert_type = 'warning'
                    name = u"Délais d'expiration proche"
                    description = u"Le contrat d'assurance du véhicule '" + v.name + u"' expire dans " + unicode(str(expiration), 'utf-8') + u" jour(s)."
            else:
                alert = True
                alert_type = 'info'
                name = u"Risque"
                description = u"Le véhicule '" + v.name + u"' ne possède aucun contrat d'assurance."
            if alert:
                # print description
                self.env['ostool.alert'].create({
                    'name': name,
                    'description': description,
                    'alert_level': alert_type,
                    'about': about,
                    'alert_date': fields.datetime.today(),
                    'vehicule_id': v.id
                })
        # print "insurance cron out"
        return True

    def _cron_check_tax_expiration_date(self):
        # print "tax cron in"
        vehicules_ids = self.search([])
        config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
        if not config:
            raise UserError("Configuration Introuvable")
        config = config[0]
        alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        about = 'tax'
        for v_id in vehicules_ids:
            alert = False
            name = u""
            description = u""
            taxes = self.env['ostool.tax'].search_read([('vehicule_id', '=', v_id.id)], ['expiration'], order='end_date DESC')
            v = self.browse(v_id.id)
            if taxes:
                expiration = taxes[0].get('expiration')
                if expiration <= 0:
                    alert = True
                    alert_type = 'alert'
                    name = u"Expiration"
                    description = u"La vignette du véhicule '" + v.name + u"' est expirée."
                elif expiration <= alert_period:
                    alert = True
                    alert_type = 'warning'
                    name = u"Délais d'expiration proche"
                    description = u"La vignette du véhicule '" + v.name + u"' expire dans " + unicode(str(expiration), 'utf-8') + u" jour(s)."
            else:
                alert = True
                alert_type = 'info'
                name = u"Risque"
                description = u"Le véhicule '" + v.name + u"' ne possède aucune vignette."
            if alert:
                # print description
                self.env['ostool.alert'].create({
                    'name': name,
                    'description': description,
                    'alert_level': alert_type,
                    'about': about,
                    'alert_date': fields.datetime.today(),
                    'vehicule_id': v.id
                })
        print "tax cron out"
        return True

    def _cron_check_visit_expiration_date(self):
        print "visit cron in"
        vehicules_ids = self.search([])
        config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
        if not config:
            raise UserError("Configuration Introuvable")
        config = config[0]
        alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        about = 'visit'
        for v_id in vehicules_ids:
            alert = False
            name = u""
            description = u""
            visits = self.env['ostool.visit'].search_read([('vehicule_id', '=', v_id.id)], ['expiration'], order='end_date DESC')
            v = self.browse(v_id.id)
            if visits:
                expiration = visits[0].get('expiration')
                if expiration <= 0:
                    alert = True
                    alert_type = 'alert'
                    name = u"Expiration"
                    description = u"La visite technique du véhicule '" + v.name + u"' est expirée."
                elif expiration <= alert_period:
                    alert = True
                    alert_type = 'warning'
                    name = u"Délais d'expiration proche"
                    description = u"La visite technique du véhicule '" + v.name + u"' expire dans " + unicode(str(expiration), 'utf-8') + u" jour(s)."
            else:
                alert = True
                alert_type = 'info'
                name = u"Risque"
                description = u"Le véhicule '" + v.name + u"' ne possède aucune visite technique."
            if alert:
                # print description
                self.env['ostool.alert'].create({
                    'name': name,
                    'description': description,
                    'alert_level': alert_type,
                    'about': about,
                    'alert_date': fields.datetime.today(),
                    'vehicule_id': v.id
                })
        print "visit cron out"
        return True
