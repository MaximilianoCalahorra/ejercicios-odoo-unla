from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiqueta de propiedad"
    
    # Atributo:
    name = fields.Char(string="Nombre", required=True)