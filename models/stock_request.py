
from odoo import models, fields

class StockRequest(models.Model):
    _inherit = 'stock.request'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account', 
        string='Analytic Accounts'
    )

    def create(self, vals):
        request = super(StockRequest, self).create(vals)
        if 'analytic_account_ids' in vals:
            for line in request.line_ids:
                line.analytic_account_ids = [(6, 0, vals['analytic_account_ids'][0][2])]
        return request

    def write(self, vals):
        res = super(StockRequest, self).write(vals)
        if 'analytic_account_ids' in vals:
            for request in self:
                for line in request.line_ids:
                    line.analytic_account_ids = [(6, 0, vals['analytic_account_ids'][0][2])]
        return res
