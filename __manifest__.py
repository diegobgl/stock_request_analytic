
{
    'name': 'Request_analytic',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Inherit analytic accounts in stock requests',
    'description': 'Adds analytic account fields to stock requests and their lines.',
    'author': 'Diego Gajardo, Camilo Neira',
    'depends': ['stock_request', 'account'],
    'data': [
        'views/stock_request_views.xml',
        'report/order_report.xml',
        'report/report_stock_request_order_template.xml'
    ],
    'installable': True,
    'application': False,
}
