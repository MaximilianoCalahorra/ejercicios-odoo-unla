from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"
    
    # Atributos:
    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(string="Estado", selection=[("accepted","Aceptada"),("refused","Rechazada")])
    validity = fields.Integer(string="Validez (días)", default=7)
    date_deadline = fields.Date(string="Fecha límite")
    
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