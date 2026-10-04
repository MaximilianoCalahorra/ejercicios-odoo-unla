from odoo import models, fields, api
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"
    
    # Atributos:
    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(string="Estado", selection=[("accepted","Aceptada"),("refused","Rechazada")])
    validity = fields.Integer(string="Validez (días)", default=7)
    
    # Relaciones:
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Ofertante",
        required=True
    )
    
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Propiedad",
        required=True
    )
    
    # Campos computados
    date_deadline = fields.Date(string="Fecha límite", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    
    # Funciones para campos computados:
    @api.depends("validity")
    def _compute_date_deadline(self):
        for rec in self:
            if rec.validity:
                rec.date_deadline = fields.Datetime.now() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = False 
    
    def _inverse_date_deadline(self):
        for rec in self:
            if rec.date_deadline and rec.create_date:
                delta = rec.date_deadline - rec.create_date.date()
                rec.validity = delta.days