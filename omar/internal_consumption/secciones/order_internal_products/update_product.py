# coding: utf-8

from datetime import datetime, timedelta
from pytz import timezone
from osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import Warning

def create_log(self, cr, uid, department, product, stock, context=None):
	current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
	cr.execute(
		"""
		INSERT INTO log_stock_departments_internal_consumption 
		(department_id, product_id, quantity, date_register, user_id) 
		VALUES (%s, %s, %s, %s, %s)
		""",(department, product, stock, datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5), current_user.id))

#Modelo 
class upadate_product_consumption(osv.osv):

	#Descripcion 
	_description = 'update_product'

	#Nombre del Modelo
	_name = 'update.product.internal.consumption'

	def current_user(self, cr, uid, ids, context = None):
		current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
		return current_user.id

	def validate_order(self, cr, uid, ids, context=None):
		current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
		cr.execute(
			"""
	          SELECT user_id
	          FROM users_internal_consumption
	          WHERE user_id = %s
	        """,(current_user.id,))
		user = cr.fetchone()

		if user:
			id_order = self.pool.get( self._name ).browse( cr, uid, ids[0] ).id
			department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department
			bandera = True

			cr.execute(
				"""
		          SELECT product_id, quantity
		          FROM temporary_orders_internal_consumption
		          WHERE order_m2o_id = %s
		        """,(id_order,))
			products = cr.fetchall()

			if products:
				for product in products:
					cr.execute(
					"""
			          SELECT stock, name
			          FROM products_internal_consumption
			          WHERE id = %s
			        """,(product[0],))
					quantity = cr.fetchone()
					if product[1] > quantity[0]:
						bandera = False
						answer = "You do not have enough products (" + quantity[1] + " cant.(" + str(quantity[0]) + ")" +")" 
						raise Warning(_(answer))
			if bandera and products:
				for product in products:
					cr.execute(
						"""
				          SELECT product_id, quantity
				          FROM stock_departments_internal_consumption
				          WHERE department_id = %s
				          AND product_id = %s
				        """,(department.id, product[0]))
					stock_dep = cr.fetchone()
					if stock_dep:
						new_stock = product[1] + stock_dep[1]
						cr.execute(
				            """
				            UPDATE stock_departments_internal_consumption SET quantity = %s,
				            date_register = %s
				            WHERE product_id = %s
				            AND department_id = %s
				            """,(new_stock, datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5), product[0], department.id,))
						create_log(self, cr, uid, department.id, product[0], new_stock)
					else:
						cr.execute(
							"""
							INSERT INTO stock_departments_internal_consumption 
							(department_id, product_id, quantity, date_register) 
							VALUES (%s, %s, %s, %s)
							""",(department.id, product[0], product[1], datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5)))
						create_log(self, cr, uid, department.id, product[0], product[1])

					cr.execute(
					"""
			          SELECT stock
			          FROM products_internal_consumption
			          WHERE id = %s
			        """,(product[0],))
					quantity = cr.fetchone()

					update_stock = quantity[0] - product[1]

					cr.execute(
			            """
			            UPDATE products_internal_consumption SET stock = %s
			            WHERE id = %s
			            """,(update_stock, product[0],))

				self.write(cr, uid, ids, {
		            'state': 'approved',
		        }, context=context)
		else:
			raise Warning(_('You do not have permissions to validate the order'))


	_columns = {
		'department': fields.many2one('departments.internal.consumption', 'Department', required=True),
		'date_register': fields.datetime('Registration date', required=True),
		'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
		'stock_o2m_ids': fields.one2many('temporary.orders.internal.consumption', 'order_m2o_id', 'Stock product'),
		'state': fields.selection([('draft', 'New'),
                                   ('cancel', 'Cancelled'),
                                   ('approved', 'approved')], 'State'),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
		'date_register': datetime.now(timezone('America/Mexico_City')) + timedelta(hours=5),
        'user_id': current_user,
        'state': 'draft',
  	}

 
upadate_product_consumption()
