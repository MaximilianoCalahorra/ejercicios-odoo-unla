from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

def _default_date_availability(self):
    return fields.Date.today() + relativedelta(months=3)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Propiedad"
    
    # Atributos:
    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código postal")
    date_availability = fields.Date(string="Fecha disponibilidad", copy=False, default=_default_date_availability)
    expected_price = fields.Float(string="Precio esperado", onchange="_on_change_expected_price")
    selling_price = fields.Float(string="Precio de venta", copy=False)
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardín", onchange="_on_change_garden")
    garden_orientation = fields.Selection(selection=[('north','Norte'),('south','Sur'),('east','Este'),('west','Oeste')], default="north", string="Orientación del jardín")
    garden_area = fields.Integer(string="Superficie jardín")
    state= fields.Selection(selection=[('new','Nuevo'),('offer_received','Oferta recibida'),('offer_accepted','Oferta aceptada'),('sold','Vendido'),('canceled','Cancelado')], string="Estado", default="new", copy=False, required=True)

    # Relaciones:
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Tipo propiedad",
        required=True
    )
    
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Comprador"
    )
    
    salesman_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendedor",
        copy=False,
        default=lambda self: self.env.user
    )
    
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Etiquetas"
    )
    
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Ofertas"
    )
    
    offer_partner_ids = fields.One2many(
        comodel_name="res.partner",
        string="Compradores interesados",
        compute="_compute_offer_partner_ids"
    )
    
    # Campos computados:
    total_area = fields.Integer(string="Superficie total", compute="_compute_total_area", store=True)
    best_offer = fields.Float(string="Mejor oferta", compute="_compute_best_offer", store=True)
    
    # Funciones para campos computados:
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for rec in self:
            offers = rec.offer_ids.mapped("price")
            
            if offers:
                rec.best_offer = max(offers)
            else:
                rec.best_offer = 0
    
    @api.depends("offer_ids.partner_id")
    def _compute_offer_partner_ids(self):
        for rec in self:
            rec.offer_partner_ids = rec.offer_ids.mapped("partner_id")
    
    # Funciones onchange:
    @api.onchange("garden")
    def _on_change_garden(self):
        if self.garden:
            self.garden_area = 10
        else:
            self.garden_area = 0
            
    @api.onchange("expected_price")
    def _on_change_expected_price(self):
        if self.expected_price and self.expected_price != 0 and self.expected_price < 10000:
            return {
                "warning": {
                    "title": "Aviso de precio bajo",
                    "message": "El precio ingresado es menor a 10.000. Por favor, verifique si no fue un error de tipeo.",
                    "type": "notification",
                }
            }

    # Acciones:
    def action_mark_as_sold(self):
        for rec in self:
            if rec.state == "canceled":
                raise UserError("No se puede marcar como vendida una propiedad cancelada.")
            rec.state = "sold"
        return True
    
    def action_cancel(self):
        for rec in self:
            if rec.state == "sold":
                raise UserError("No se puede cancelar una propiedad vendida.")
            rec.state = "canceled"
        return True