from odoo import models, fields, api

class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    analytic_account_ids = fields.Many2many(
         'account.analytic.account', 
         string='Analytic Accounts'
     )

    @api.model
    def create(self, vals):
        # Heredar las cuentas analíticas en las líneas de stock move y stock picking
        res = super(StockRequestOrder, self).create(vals)
        if res.analytic_account_ids:
            res._assign_analytic_accounts()
        return res

    def write(self, vals):
        # Al escribir en el registro, asegúrate de que las cuentas analíticas se actualicen en las líneas
        res = super(StockRequestOrder, self).write(vals)
        if 'analytic_account_ids' in vals:
            self._assign_analytic_accounts()
        return res

    def _assign_analytic_accounts(self):
        # Asignar cuentas analíticas a las líneas relacionadas
        for order in self:
            if order.analytic_account_ids:
                # Asignar a los movimientos de stock
                order.move_ids.write({'analytic_account_ids': [(6, 0, order.analytic_account_ids.ids)]})
                # Asignar a los pickings
                order.picking_ids.write({'analytic_account_ids': [(6, 0, order.analytic_account_ids.ids)]})
