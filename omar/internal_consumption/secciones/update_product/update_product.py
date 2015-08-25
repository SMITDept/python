# coding: utf-8

from datetime import datetime, timedelta
from osv import fields, osv
from openerp.tools.translate import _

def create_log(self, cr, uid, department, product, stock, context=None):
	current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
	cr.execute(
		"""
		INSERT INTO log_stock_departments_internal_consumption 
		(department_id, product_id, quantity, date_register, user_id) 
		VALUES (%s, %s, %s, %s, %s)
		""",(department, product, stock, datetime.now(), current_user.id))

#Modelo 
class upadate_product_consumption(osv.osv):

	#Descripcion 
	_description = 'update_product'

	#Nombre del Modelo
	_name = 'update.product.internal.consumption'

	def create(self, cr, uid, values, context=None):
		register = False
		cr.execute(
			"""
			DELETE FROM update_product_internal_consumption
			""",)
		items = []
		for dic in values.values():
			for tup in dic:
				product_id = tup[2].get("product_id")
				department_id = tup[2].get("department_id")
				quantity = tup[2].get("quantity")
				cr.execute(
					"""
			          SELECT stock, name
			          FROM products_internal_consumption
			          WHERE id = %s
			        """,(product_id,))
				product = cr.fetchone()
				if product[0] >= quantity:
					stock = product[0] - quantity
					cr.execute(
						"""
				          SELECT quantity
				          FROM stock_departments_internal_consumption
				          WHERE department_id = %s
				          AND product_id = %s
				        """,(department_id, product_id,))
					stock_dep = cr.fetchone()
					if stock_dep:
						stock_dep = stock_dep[0] + quantity
						register = True
					else:
						stock_dep = quantity
					if register:
						cr.execute(
				            """
				            UPDATE stock_departments_internal_consumption SET quantity = %s
				            WHERE product_id = %s
				            AND department_id = %s
				            """,(stock_dep, product_id, department_id,))
						create_log(self, cr, uid, department_id, product_id, stock_dep)
					else:
						cr.execute(
							"""
							INSERT INTO stock_departments_internal_consumption 
							(department_id, product_id, quantity, date_register) 
							VALUES (%s, %s, %s, %s)
							""",(department_id, product_id, stock_dep, datetime.now()))
						create_log(self, cr, uid, department_id, product_id, stock_dep)

					cr.execute(
			            """
			            UPDATE products_internal_consumption SET stock = %s
			            WHERE id = %s
			            """,(stock, product_id,))
					#dic.remove(tup)
					items.append(tup)
				else:
					raise osv.except_osv(_( 'Warning' ),_( 'You have not enough products' ) )

			for item in items:
				dic.remove(item)
		return super(upadate_product_consumption, self).create(cr, uid, values, context=context)

	_columns = {
		'stock_o2m_ids': fields.one2many('stock.departments.internal.consumption', 'update_m2o_id', 'Stock product'),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {

  	}

  	def get_product():
  		print "LLLLLLLLLLL"

 
upadate_product_consumption()
