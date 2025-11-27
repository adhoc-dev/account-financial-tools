from odoo import models
from odoo.tools import SQL


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _asset_difference_search(self, account_type, operator, operand):
        if operator not in ("<", "=", ">", ">=", "<="):
            return []
        if not isinstance(operand, (float, int)):
            return []
        sign = 1
        if account_type == "liability_payable":
            sign = -1

        # Optimization: Return a subquery using SQL object instead of fetching IDs.
        # This allows the database to optimize the execution plan when combined with other domains.
        return [
            (
                "id",
                "in",
                SQL(
                    """(
            SELECT aml.partner_id
              FROM res_partner partner
         LEFT JOIN account_move_line aml ON aml.partner_id = partner.id
              JOIN account_move move ON move.id = aml.move_id
              JOIN res_company line_company ON line_company.id = aml.company_id
        RIGHT JOIN account_account acc ON aml.account_id = acc.id
             WHERE acc.account_type = %s
               AND NOT acc.deprecated
               AND SPLIT_PART(line_company.parent_path, '/', 1)::int = %s
               AND move.state = 'posted'
          GROUP BY aml.partner_id
            HAVING %s * COALESCE(SUM(aml.amount_residual), 0) %s %s
            )""",
                    account_type,
                    self.env.company.root_id.id,
                    sign,
                    SQL(operator),
                    operand,
                ),
            )
        ]
