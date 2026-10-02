from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"
    
    # Atributos:
    price = fields.Float(string="Precio", required=True)
    status = fields.Selection([("accepted","Aceptada"),("refused","Rechazada")])
    
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