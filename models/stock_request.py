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
            # Verifica si el picking ya fue creado
            if not order.stock_picking_id:
                # Crear el picking si es necesario
                picking_vals = {
                    'origin': order.name,  # Ajusta según sea necesario
                    'move_type': 'direct',  # Directo o según la lógica que uses
                    # Otros campos necesarios para crear el picking
                }
                picking = self.env['stock.picking'].create(picking_vals)
                order.stock_picking_id = picking.id

            # Verificar los datos de las cuentas analíticas
            if order.analytic_account_ids:
                # Imprimir los IDs de las cuentas analíticas para depuración
                _logger.info(f"Asignando cuentas analíticas: {order.analytic_account_ids.ids}")
                
                # Asignar cuentas analíticas al picking
                order.stock_picking_id.analytic_account_ids = [(6, 0, order.analytic_account_ids.ids)]
            else:
                # Si no hay cuentas analíticas, limpiar el campo
                order.stock_picking_id.analytic_account_ids = [(5, 0, 0)]
