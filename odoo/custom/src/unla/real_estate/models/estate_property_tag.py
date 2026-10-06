from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiqueta de propiedad"
    
    # Atributo:
    name = fields.Char(string="Nombre", required=True)
    
    # Constraints:
    _estate_property_tag_name_unique = models.Constraint("unique(name)", "El nombre de la etiqueta debe ser único.")