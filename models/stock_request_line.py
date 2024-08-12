
from odoo import models, fields

class StockRequestLine(models.Model):
    _inherit = 'stock.request.line'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account', 
        string='Analytic Accounts'
    )
