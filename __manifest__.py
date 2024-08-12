
{
    'name': 'stock_request_analytic',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Inherit analytic accounts in stock requests',
    'description': 'Adds analytic account fields to stock requests and their lines.',
    'author': 'Your Name',
    'depends': ['stock_logistics_request', 'account'],
    'data': [
        'views/stock_request_line_views.xml',
    ],
    'installable': True,
    'application': False,
}
