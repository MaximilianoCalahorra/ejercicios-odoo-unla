from odoo import Command, models

class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    # Función:
    def action_mark_as_sold(self):
        for rec in self:
            self.env["account.move"].create({
                "partner_id": rec.buyer_id.id,  # Comprador.
                "move_type": "out_invoice",  # Factura a un cliente.
                "property_id": rec.id,  # Propiedad.
                # Ítems de la factura:
                "line_ids": [
                    # Propiedad vendida:
                    Command.create({
                        "name": rec.name,
                        "quantity": 1,
                        "price_unit": rec.selling_price
                    }),
                    
                    # Gastos administrativos:
                    Command.create({
                        "name": "Gastos administrativos",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            })
        return super().action_mark_as_sold()