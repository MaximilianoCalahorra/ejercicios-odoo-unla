from odoo import fields, models

class AccountMove(models.Model):
    _inherit = "account.move"
    
    # Atributo:
    property_id = fields.Many2one(comodel_name="estate.property")