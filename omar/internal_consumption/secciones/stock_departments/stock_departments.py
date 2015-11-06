# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

from openerp.osv import osv,fields
from datetime import datetime, timedelta
from pytz import timezone

#Modelo
class stock_departments_internal_consumption(osv.osv):

    #Nombre del Modelo
    _name = 'stock.departments.internal.consumption'

    _columns = {
        'department_id': fields.many2one('departments.internal.consumption', 'Department', required=False),
    	'product_id': fields.many2one('products.internal.consumption', 'Product', required=False),
        'quantity': fields.float("Quantity", digits=(12,3), requred=False),
        'date_register': fields.datetime('Date register', required=False),
    }

    #Valores por defecto de los elementos del arreglo [_columns]
    _defaults = {
        'date_register': datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5),
    }

stock_departments_internal_consumption()

#Modelo
class log_stock_departments_internal_consumption(osv.osv):

    #Nombre del Modelo
    _name = 'log.stock.departments.internal.consumption'

    _columns = {
        'department_id': fields.many2one('departments.internal.consumption', 'Department', required=False),
        'product_id': fields.many2one('products.internal.consumption', 'Product', required=False),
        'quantity': fields.float("Quantity", digits=(12,3), requred=False),
        'date_register': fields.datetime('Date register', required=False),
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    #Valores por defecto de los elementos del arreglo [_columns]
    _defaults = {
        'date_register': datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5),
    }

log_stock_departments_internal_consumption()

#Modelo
class temporary_orders_internal_consumption(osv.osv):

    #Nombre del Modelo
    _name = 'temporary.orders.internal.consumption'

    _columns = {
        'product_id': fields.many2one('products.internal.consumption', 'Product', required=False),
        'quantity': fields.float("Quantity", digits=(12,3), requred=False),
        'date_register': fields.datetime('Date register', required=False),
        'order_m2o_id': fields.many2one('update.product.internal.consumption', 'Update key', required = False),
    }

    #Valores por defecto de los elementos del arreglo [_columns]
    _defaults = {
        'date_register': datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5),
    }

temporary_orders_internal_consumption()