from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_use_documents = fields.Boolean(
        'Sale Use Documents'
    )
    purchase_use_documents = fields.Boolean(
        'Purchase Use Documents'
    )

    @api.onchange('localization')
    def account_documentonchange_localization(self):
        if self.localization:
            self.sale_use_documents = True
            self.purchase_use_documents = True
