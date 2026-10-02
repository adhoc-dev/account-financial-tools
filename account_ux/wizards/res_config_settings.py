##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sale_tax_id = fields.Many2one(
        "account.tax",
        string="Default Sale Tax",
        related="company_id.account_sale_tax_id",
        readonly=False,
        check_company=True,
        domain=[("type_tax_use", "in", ["sale", "all"])],
    )
    purchase_tax_id = fields.Many2one(
        "account.tax",
        string="Default Purchase Tax",
        related="company_id.account_purchase_tax_id",
        readonly=False,
        check_company=True,
        domain=[("type_tax_use", "in", ["purchase", "all"])],
    )
