
from openerp.osv import osv,fields


class products_internal_consumption(osv.osv):

    _name = 'products.internal.consumption'

    MEASURE = [
    ('Piezas', 'Piezas'),
    ('Caja', 'Caja'),
    ('Paquete', 'Paquete')
	]

    _columns = {
        'name': fields.char('Product name', size=100, required=True),
        'stock': fields.float("Stock products", digits=(12,3), requred=False),
        'measure': fields.selection(MEASURE, 'Measure', required=True),
    }

    _defaults = {
        'stock': 0,
    }

products_internal_consumption()
