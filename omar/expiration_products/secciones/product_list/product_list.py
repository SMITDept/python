
from openerp.osv import osv,fields
from datetime import datetime


class product_list_expired(osv.osv):

    _name = 'product.list.expired'

    _columns = {
        'shop_is_m2o': fields.many2one('sale.shop', 'Branch', required=True),
        'ean13': fields.char("Product id", size=13, required=True),
        'name': fields.char('Product name', size=70, readonly=True),
        'month0_4': fields.integer("0-4 Months"),
        'month5_8': fields.integer("5-8 Months"),
        'month9_12': fields.integer("9-12 Months"),
        'over_12': fields.integer('Over 12 months', required=True),
        'db_num': fields.integer('Product in the database', required=True),
        'expired':fields.integer('Expired'),
    }

    _defaults = {
        
    }

product_list_expired()

class product_list_expired_log(osv.osv):

    _name = 'product.list.expired.log'

    _columns = {
        'shop_is_m2o': fields.many2one('sale.shop', 'Branch', required=True),
        'ean13': fields.char("Product id", size=13, required=True),
        'name': fields.char('Product name', size=70, readonly=True),
        'month0_4': fields.integer("0-4 Months"),
        'month5_8': fields.integer("5-8 Months"),
        'month9_12': fields.integer("9-12 Months"),
        'over_12': fields.integer('Over 12 months', required=True),
        'db_num': fields.integer('Product in the database', required=True),
        'expired':fields.integer('Expired'),
        'date_register': fields.datetime('Registration date', required=True),
    }

    _defaults = {
        
    }

product_list_expired_log()