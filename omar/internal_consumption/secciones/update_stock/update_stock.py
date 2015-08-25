# coding: utf-8

from datetime import datetime, timedelta
from osv import fields, osv
from openerp.tools.translate import _

def create_log(self, cr, uid, ids, department, product, stock, context=None):
	current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
	cr.execute(
		"""
		INSERT INTO log_stock_departments_internal_consumption 
		(department_id, product_id, quantity, date_register, user_id) 
		VALUES (%s, %s, %s, %s, %s)
		""",(department, product, stock, datetime.now(), current_user.id))
#Modelo 
class update_stock_internal_consumption(osv.TransientModel):

	#Descripcion 
	_description = 'Update stock'

	#Nombre del Modelo
	_name = 'update.stock.internal.consumption'

	_columns = {
		'department': fields.many2one('departments.internal.consumption', 'Department', required=True),
		'product': fields.many2one('products.internal.consumption', 'Product'),
		'quantity': fields.float("Quantity", digits=(12,3)),
		'state': fields.selection([('dep', 'departmenta'),
                                   ('pro', 'product'),
                                   ('save', 'Save')]),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
    	'state': 'dep',
  	}

  	def back_menu(self, cr, uid, ids,context = { }):
		department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department
		self.write(cr, uid, ids, {
            'department': department.id,
            'product': '',
            'quantity': '',
            'state': 'pro',
        }, context=context)
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'update.stock.internal.consumption',
            'target': 'new',
            }


  	def save_product(self, cr, uid, ids,context = { }):
		department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department
		product = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product
		quantity = self.pool.get( self._name ).browse( cr, uid, ids[0] ).quantity

		cr.execute(
	        """
	          SELECT quantity, product_id, department_id
	          FROM stock_departments_internal_consumption
	          WHERE product_id = %s
	          AND department_id = %s
	        """,(product.id, department.id,))
		products = cr.fetchone()
		if product and products[0] >= quantity:
			cr.execute(
				"""
				UPDATE stock_departments_internal_consumption SET quantity = %s,
				date_register = %s
				WHERE product_id = %s
				AND department_id = %s
				""",(quantity, datetime.now(), product.id, department.id,))
			create_log(self, cr, uid, ids, department.id, product.id, quantity)
		else:
			raise osv.except_osv(_( 'Warning' ),_( 'The product does not exist or ' ) )

		self.write(cr, uid, ids, {
            'department': 0,
    		'product': 0,
    		'quantity': 0,
            'state': 'dep',
        }, context=context)
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'update.stock.internal.consumption',
            'target': 'new',
         }


  	def get_product(self, cr, uid, ids, product):
  		context = ""
  		department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department
  		product = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product
		"""
		Metodo obtener el producto
		"""
		cr.execute(
        """
          SELECT quantity, product_id, department_id
          FROM stock_departments_internal_consumption
          WHERE product_id = %s
          AND department_id = %s
        """,(product.id, department.id,))
		product = cr.fetchone()

		if product:
			self.write(cr, uid, ids, {
				'product_id': product[1],
				'department_id': product[2],
	            'quantity': product[0],
	            'state': 'save',
	        }, context=context)

			this = self.browse(cr, uid, ids)[0]
			return {
	            'type': 'ir.actions.act_window',
	            'view_type': 'form',
	            'view_mode': 'form',
	            'res_id': this.id,
	            'views': [(False, 'form')],
	            'res_model': 'update.stock.internal.consumption',
	            'target': 'new',
	         }
		else:
			raise osv.except_osv(_( 'Warning' ),_( 'The product does not exist' ) )

  	def get_department(self, cr, uid, ids,context = { }):
		"""
		Metodo obtener el departamento
		"""
		department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department

		self.write(cr, uid, ids, {
            'department': department.id,
            'state': 'pro',
        }, context=context)
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'update.stock.internal.consumption',
            'target': 'new',
            }

update_stock_internal_consumption()
