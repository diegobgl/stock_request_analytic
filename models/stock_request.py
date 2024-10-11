from odoo import models, fields, api

class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    analytic_account_ids = fields.Many2many(
         'account.analytic.account', 
         string='Analytic Accounts'
     )
    available_qty = fields.Float( string="Stock Disponible", compute="_compute_available_qty", store=False)

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
                    'origin': order.name,  
                    'move_type': 'direct',  
                }
                picking = self.env['stock.picking'].create(picking_vals)
                order.stock_picking_id = picking.id

            if order.analytic_account_ids:
                _logger.info(f"Asignando cuentas analíticas: {order.analytic_account_ids.ids}")
                
                # Asignar cuentas analíticas al picking
                order.stock_picking_id.analytic_account_ids = [(6, 0, order.analytic_account_ids.ids)]
            else:
                # Si no hay cuentas analíticas, limpiar el campo
                order.stock_picking_id.analytic_account_ids = [(5, 0, 0)]

    @api.depends('product_id', 'route_id')
    def _compute_available_qty(self):
        for line in self:
            if line.product_id and line.route_id:
                # Obtener la ubicación de origen asociada con la ruta seleccionada
                route = line.route_id
                # Obtener la ubicación de origen de la ruta (de la primera regla asociada)
                location_origin = route.rule_ids.filtered(lambda r: r.location_src_id).mapped('location_src_id')
                
                # Si hay una ubicación de origen en la ruta, calcular el stock disponible
                if location_origin:
                    stock_qty = self.env['stock.quant'].sudo().search([
                        ('product_id', '=', line.product_id.id),
                        ('location_id', '=', location_origin[0].id)  # Usamos la primera ubicación de origen de la regla
                    ]).quantity
                    line.available_qty = stock_qty
                else:
                    line.available_qty = 0.0
            else:
                line.available_qty = 0.0
