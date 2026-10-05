from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta, date

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"
    
    # Atributos:
    name = fields.Char(string="Nombre", required=True)
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
    
    # Campos relacionados:
    property_type = fields.Char(related="property_id.property_type_id.name", store=True)
    
    # Acciones:
    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda p: p.status == "accepted"):
                raise UserError("Esta propiedad ya tiene una oferta aceptada.")

            if offer.property_id.state in ["sold", "canceled"]:
                raise UserError(
                    "No se puede aceptar ofertas para una propiedad vendida o cancelada."
                )

            offer.status = "accepted"

            offer.property_id.write(
                {
                    "state": "offer_accepted",
                    "buyer_id": offer.partner_id.id,
                    "selling_price": offer.price,
                }
            )

            # Obtener las otras ofertas y llamar al método sobre ellas
            other_offers = offer.property_id.offer_ids - offer
            other_offers._action_reject_other_offers()

        return True


    def _action_reject_other_offers(self):
        # 'self' aquí serán todas las ofertas que queremos rechazar
        self.write({"status": "refused"})