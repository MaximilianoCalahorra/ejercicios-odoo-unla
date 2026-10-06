from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Tipo de propiedad"
    
    # Atributo:
    name = fields.Char(string="Nombre", required=True)
    
    # Constraints:
    _estate_property_type_name_unique = models.Constraint("unique(name)", "El nombre del tipo de propiedad debe ser único.")