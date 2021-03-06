# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

from openerp.osv import osv,fields
from datetime import datetime

#Modelo 
class product_list_expired(osv.osv):

    #Nombre del Modelo
    _name = 'product.list.expired'

    _columns = {
        'shop_is_m2o': fields.many2one('sale.shop', 'Branch', required=True),
        'ean13': fields.char("Product id", size=13, required=True),
        'name': fields.char('Product name', size=70, readonly=True),
        'month0_4': fields.float("0-4 Months", digits=(12,3)),
        'month5_8': fields.float("5-8 Months", digits=(12,3)),
        'month9_12': fields.float("9-12 Months", digits=(12,3)),
        'over_12': fields.float('Over 12 months', digits=(12,3), required=True),
        'db_num': fields.float('Product in the database', digits=(12,3), required=True),
        'expired':fields.float('Expired', digits=(12,3)),
        'date_register': fields.datetime('Registration date', required=True),
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    _defaults = {
        
    }

product_list_expired()

#Modelo 
class product_list_expired_log(osv.osv):

     #Nombre del Modelo
    _name = 'product.list.expired.log'

    _columns = {
        'shop_is_m2o': fields.many2one('sale.shop', 'Branch', required=True),
        'ean13': fields.char("Product id", size=13, required=True),
        'name': fields.char('Product name', size=70, readonly=True),
        'month0_4': fields.float("0-4 Months", digits=(12,3)),
        'month5_8': fields.float("5-8 Months", digits=(12,3)),
        'month9_12': fields.float("9-12 Months", digits=(12,3)),
        'over_12': fields.float('Over 12 months', digits=(12,3), required=True),
        'db_num': fields.float('Product in the database', digits=(12,3), required=True),
        'expired':fields.float('Expired', digits=(12,3)),
        'date_register': fields.datetime('Registration date', required=True),
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    _defaults = {
        
    }

product_list_expired_log()