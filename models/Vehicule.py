# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class Vehicule(models.Model):
    _name = "ostool.vehicule"
    _order = "name asc"

    _inherit = ["mail.thread"]

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

    @api.model
    def _cron_check_insurance_expiration_date(self):
        print "insurance cron in"
        # vehicules = self.search([])
        # config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
        # if not config:
        #     raise UserError("Configuration Introuvable")
        # config = config[0]
        # alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        # for v in vehicules:
        #     alert = False
        #     subject = u""
        #     body = u""
        #     insurances = self.env['ostool.insurance'].search_read([('vehicule_id', '=', v.id)], ['expiration'], order='end_date DESC')
        #     if insurances:
        #         expiration = insurances[0].get('expiration')
        #         if expiration <= 0:
        #             alert = True
        #             subject = u"Alerte"
        #             body = u"<h3>Alerte</h3><br/>Le contrat d'assurance du véhicule <strong>'" + v.name + u"'</strong> est expiré."
        #         elif expiration <= alert_period:
        #             alert = True
        #             subject = u"Notification"
        #             body = u"<h3>Notification</h3><br/>Le contrat d'assurance du véhicule <strong>'" + v.name + u"'</strong> expire dans <strong>" + unicode(str(expiration), 'utf-8') + u"</strong> jour(s)."
        #     else:
        #         alert = True
        #         subject = u"Alerte"
        #         body = u"<h3>Alerte</h3><br/><br/>Le véhicule <strong>'" + v.name + u"'</strong> ne possède aucun contrat d'assurance."
        #     if alert:
        #         print body
        #         v.message_post(
        #             subject=subject,
        #             body=body,
        #             partner_ids=[responsible_id]
        #         )
        print "insurance cron out"
        return True

    def _cron_check_tax_expiration_date(self):
        print "tax cron in"
        # vehicules = self.search([])
        # config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
        # if not config:
        #     raise UserError("Configuration Introuvable")
        # config = config[0]
        # alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        # for v in vehicules:
        #     alert = False
        #     subject = u""
        #     body = u""
        #     taxes = self.env['ostool.tax'].search_read([('vehicule_id', '=', v.id)], ['expiration'], order='end_date DESC')
        #     if taxes:
        #         expiration = taxes[0].get('expiration')
        #         if expiration <= 0:
        #             alert = True
        #             subject = u"Alerte"
        #             body = u"La vignette du véhicule '" + v.name + u"' est expirée."
        #         elif expiration <= alert_period:
        #             alert = True
        #             subject = u"Notification"
        #             body = u"La vignette du véhicule '" + v.name + u"' expire dans " + unicode(str(expiration), 'utf-8') + u" jour(s)."
        #     else:
        #         alert = True
        #         subject = u"Alerte"
        #         body = u"Le véhicule '" + v.name + u"' ne possède aucune vignette."
        #     if alert:
        #         self.message_post(
        #             message_type='notification',
        #             subtype='mt_comment',
        #             subject=subject,
        #             body=body,
        #             partner_ids=[responsible_id]
        #         )
        print "tax cron out"
        return True

    def _cron_check_visit_expiration_date(self):
        print "visit cron in"
        # vehicules = self.search([])
        # config = self.env['ostool.config'].search_read([], order='write_date DESC', limit=1)
        # if not config:
        #     raise UserError("Configuration Introuvable")
        # config = config[0]
        # alert_period = config.get('alert_period')
        # responsible_id = config.get('responsible_partner_id')
        # for v in vehicules:
        #     alert = False
        #     subject = u""
        #     body = u""
        #     visits = self.env['ostool.visit'].search_read([('vehicule_id', '=', v.id)], ['expiration'], order='end_date DESC')
        #     if visits:
        #         expiration = visits[0].get('expiration')
        #         if expiration <= 0:
        #             alert = True
        #             subject = u"Alerte"
        #             body = u"La visite technique du véhicule '" + v.name + u"' est expirée."
        #         elif expiration <= alert_period:
        #             alert = True
        #             subject = u"Notification"
        #             body = u"La visite technique du véhicule '" + v.name + u"' expire dans " + unicode(str(expiration), 'utf-8') + u" jour(s)."
        #     else:
        #         alert = True
        #         subject = u"Alerte"
        #         body = u"Le véhicule '" + v.name + u"' ne possède aucune visite technique."
        #     if alert:
        #         self.message_post(
        #             message_type='notification',
        #             subtype='mt_comment',
        #             subject=subject,
        #             body=body,
        #             partner_ids=[responsible_id]
        #         )
        print "visit cron out"
        return True
