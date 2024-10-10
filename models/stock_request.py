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
    # Asignar cuentas analíticas a las líneas relacionadas
        for order in self:
            if order.analytic_account_ids:
                # Asignar a los movimientos de stock
                if order.move_ids:
                    order.move_ids.sudo().write({
                        'analytic_account_id': order.analytic_account_ids.id  # Reemplazar campo si es necesario
                    })
                # Asignar a los pickings
                if order.picking_ids:
                    order.picking_ids.sudo().write({
                        'analytic_account_id': order.analytic_account_ids.id  # Reemplazar campo si es necesario
                    })

    # def _assign_analytic_accounts(self):
    #     # Asignar cuentas analíticas a las líneas relacionadas
    #     for order in self.sudo():
    #         if order.analytic_account_ids:
    #             # Asignar a los movimientos de stock
    #             order.move_ids.sudo().write({'analytic_account_ids': [(6, 0, order.analytic_account_ids.ids)]})
    #             # Asignar a los pickings
    #             order.picking_ids.sudo().write({'analytic_account_ids': [(6, 0, order.analytic_account_ids.ids)]})
