from odoo import models, fields
from dateutil.relativedelta import relativedelta

def _default_date_availability(self):
    return fields.Date.today() + relativedelta(months=3)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Propiedad"
    
    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código postal")
    date_availability = fields.Date(string="Fecha disponibilidad", copy=False, default=_default_date_availability)
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta", copy=False)
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardín")
    garden_orientation = fields.Selection(selection=[('north','Norte'),('south','Sur'),('east','Este'),('west','Oeste')], default="north", string="Orientación del jardín")
    garden_area = fields.Integer(string="Superficie jardín")
    state= fields.Selection(selection=[('new','Nuevo'),('offer_received','Oferta recibida'),('offer_accepted','Oferta aceptada'),('sold','Vendido'),('canceled','Cancelado')], string="Estado", default="new", copy=False, required=True)
