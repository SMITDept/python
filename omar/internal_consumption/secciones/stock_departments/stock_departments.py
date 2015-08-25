
from openerp.osv import osv,fields
from datetime import datetime


class stock_departments_internal_consumption(osv.osv):

    _name = 'stock.departments.internal.consumption'

    _columns = {
    	'department_id': fields.many2one('departments.internal.consumption', 'Department', required=False),
    	'product_id': fields.many2one('products.internal.consumption', 'Product', required=False),
        'quantity': fields.float("Quantity", digits=(12,3), requred=False),
        'date_register': fields.datetime('Date register', required=False),
        'update_m2o_id': fields.many2one('update.product.internal.consumption', 'Update key', required = False),
    }

    _defaults = {
        'date_register': datetime.now(),
    }

stock_departments_internal_consumption()


class log_stock_departments_internal_consumption(osv.osv):

    _name = 'log.stock.departments.internal.consumption'

    _columns = {
        'department_id': fields.many2one('departments.internal.consumption', 'Department', required=False),
        'product_id': fields.many2one('products.internal.consumption', 'Product', required=False),
        'quantity': fields.float("Quantity", digits=(12,3), requred=False),
        'date_register': fields.datetime('Date register', required=False),
        #'update_m2o_id': fields.many2one('update.product.internal.consumption', 'Update key', required = False),
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    _defaults = {
        'date_register': datetime.now(),
    }

log_stock_departments_internal_consumption()
