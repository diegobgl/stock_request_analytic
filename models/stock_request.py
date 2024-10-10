from odoo import models, fields, api

class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    analytic_account_ids = fields.Many2many(
         'account.analytic.account', 
         string='Analytic Accounts'
     )

    @api.model
    def create(self, vals):
        res = super(StockRequestOrder, self).create(vals)
        return res

    def write(self, vals):
        res = super(StockRequestOrder, self).write(vals)  
        if 'analytic_account_ids' in vals:
            self.sudo()._assign_analytic_accounts()  
        return res
    
    def _assign_analytic_accounts(self):
        for order in self:
            if order.analytic_account_ids:
                order.stock_picking_id.analytic_account_ids = [(6, 0, order.analytic_account_ids.ids)]
            else:
                order.stock_picking_id.analytic_account_ids = [(5, 0, 0)]  
    # def _assign_analytic_accounts(self):
    #     # Asignar cuentas analíticas a las líneas relacionadas
    #     for order in self.sudo():
    #         if order.analytic_account_ids:
    #             # Asignar a los movimientos de stock
    #             order.move_ids.sudo().write({'analytic_account_ids': [(6, 0, order.analytic_account_ids.ids)]})
    #             # Asignar a los pickings
    #             order.picking_ids.sudo().write({'analytic_account_ids': [(6, 0, order.analytic_account_ids.ids)]})
