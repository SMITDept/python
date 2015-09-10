
from openerp.osv import osv,fields
from datetime import datetime

class purchases_internal_consumption(osv.osv):

    _name = 'purchases.internal.consumption'

    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")

    def current_user(self, cr, uid, ids,context = None):
        current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        return current_user.id

    def create(self, cr, uid, values, context=None):
        id_product = values.get('product_id')
        pieces = values.get('pieces')
        cr.execute(
            """
              SELECT stock
              FROM products_internal_consumption
              WHERE id = %s
            """,(id_product,))
        stock = cr.fetchone()
        stock = int(stock[0]) + pieces
        cr.execute(
            """
            UPDATE products_internal_consumption SET stock = %s
            WHERE id = %s
            """,(stock, id_product))
        return super(purchases_internal_consumption, self).create(cr, uid, values, context=context)


    _columns = {
    	'product_id': fields.many2one('products.internal.consumption', 'Products', required=True),
    	'pieces': fields.float("Pieces", digits=(12,3), required=True),
        'date_register': fields.datetime('Registration date', required=True),
        'price': fields.float("Unit price", digits=(12,3), required=True),
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    _defaults = {
        'date_register': datetime.strptime(date, "%d-%m-%Y %H:%M:%S.%f"),
        'user_id': current_user,
    }

purchases_internal_consumption()