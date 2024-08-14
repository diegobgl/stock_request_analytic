from odoo import models, fields, api

class StockRequest(models.Model):
    _inherit = 'stock.request'

    analytic_account_ids = fields.Many2many(
        'account.analytic.account', 
        string='Analytic Accounts'
    )

    @api.model
    def create(self, vals):
        # Heredar las cuentas analíticas en las líneas de stock move y stock picking
        res = super(StockRequest, self).create(vals)
        if res.analytic_account_ids:
            res._assign_analytic_accounts()
        return res

    def write(self, vals):
        # Al escribir en el registro, asegúrate de que las cuentas analíticas se actualicen en las líneas
        res = super(StockRequest, self).write(vals)
        if 'analytic_account_ids' in vals:
            self._assign_analytic_accounts()
        return res

    def _assign_analytic_accounts(self):
        # Asignar cuentas analíticas a las líneas relacionadas
        for request in self:
            if request.analytic_account_ids:
                # Asignar a los movimientos de stock
                request.move_ids.write({'analytic_account_ids': [(6, 0, request.analytic_account_ids.ids)]})
                # Asignar a los pickings
                request.picking_ids.write({'analytic_account_ids': [(6, 0, request.analytic_account_ids.ids)]})
