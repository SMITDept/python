# coding: utf-8

from datetime import datetime, timedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _

def get_db_data(self, cr, uid, ids, branch, ean13):
	cr.execute(
        """
          SELECT id, month0_4, month5_8,
          month9_12, expired, over_12
          FROM product_list_expired
          WHERE shop_is_m2o = %s
          AND ean13 = %s
        """,(branch, ean13))
	db_expired = cr.fetchall()
	return db_expired

#Modelo 
class expiration_product(osv.TransientModel):

	#Descripcion 
	_description = 'expiration_product'

	#Nombre del Modelo
	_name = 'expiration.product'

	_columns = {
		'branch': fields.many2one('sale.shop', 'Branch', required=True),
		'code_ean13': fields.char('Ean13', size=13, help='The Ean13 of the product'),
		'product': fields.char('Product name', size=70, readonly=True),
		'image': fields.binary(
            'Image', readonly=True, help='photo'),
		'mon0_4': fields.boolean('0-4 months'),
		'mon5_8': fields.boolean('5-8 months'),
		'mon9_12': fields.boolean('9-12 months'),
		'expired': fields.boolean('Expired'),
		'state': fields.selection([('branch', 'Branch'),
                                   ('ean13', 'Ean13'),
                                   ('save', 'Save')]),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
    	'state': 'branch',
  	}

  	def get_product(self, cr, uid, ids, ean13):
  		context = ""
  		if len(ean13) == 13:
			"""
			Metodo obtener la sucursal
			"""
			cr.execute(
	        """
	          SELECT prod.name_template,
	          prod.image_small
	          FROM product_product prod
	          WHERE ean13 = %s
	        """,(ean13,))
			product = cr.fetchall()
			if product:
				product = product[0]
				self.write(cr, uid, ids, {
					'product': product[0],
					'image': product[1],
		            'code_ean13': ean13,
		            'state': 'save',
		        }, context=context)
				this = self.browse(cr, uid, ids)[0]
				return {
		            'type': 'ir.actions.act_window',
		            'view_type': 'form',
		            'view_mode': 'form',
		            'res_id': this.id,
		            'views': [(False, 'form')],
		            'res_model': 'expiration.product',
		            'target': 'new',
		         }
			else:
				raise osv.except_osv(_( 'Warning' ),_( 'The product does not exist' ) )
				
		else:
			this = self.browse(cr, uid, ids)[0]
			return {
	            'type': 'ir.actions.act_window',
	            'view_type': 'form',
	            'view_mode': 'form',
	            'res_id': this.id,
	            'views': [(False, 'form')],
	            'res_model': 'expiration.product',
	            'target': 'new',
	         }

  	def save_product(self, cr, uid, ids,context = { }):
		"""
		Metodo obtener la sucursal
		"""
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
		ean13 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).code_ean13
		name = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product
		mon0_4 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).mon0_4
		mon5_8 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).mon5_8
		mon9_12 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).mon9_12
		expired = self.pool.get( self._name ).browse( cr, uid, ids[0] ).expired

		#cr.execute(
	    #    """
	    #      SELECT prod.name_template,
	    #      FROM product_product prod
	    #      WHERE ean13 = %s
	    #    """,(ean13,))
		stock_products = 50

		db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)

		if db_expired:
			db_expired = db_expired[0]
			if mon0_4 == True:
				new_number = db_expired[1] +1
				cr.execute(
					"""
					UPDATE product_list_expired SET month0_4 = %s
					WHERE id = %s
					""",(new_number, db_expired[0]))
				db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)
				db_expired = db_expired[0]
				over12 = stock_products - (db_expired[1] + db_expired[2] + db_expired[3] + db_expired[4])
				cr.execute(
					"""
					UPDATE product_list_expired SET over_12 = %s
					WHERE id = %s
					""",(over12, db_expired[0]))

			if mon5_8 == True:
				new_number = db_expired[2] +1
				cr.execute(
					"""
					UPDATE product_list_expired SET month5_8 = %s
					WHERE id = %s
					""",(new_number, db_expired[0]))
				db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)
				db_expired = db_expired[0]
				over12 = stock_products - (db_expired[1] + db_expired[2] + db_expired[3] + db_expired[4])
				cr.execute(
					"""
					UPDATE product_list_expired SET over_12 = %s
					WHERE id = %s
					""",(over12, db_expired[0]))
			if mon9_12 == True:
				new_number = db_expired[3] +1
				cr.execute(
					"""
					UPDATE product_list_expired SET month9_12 = %s
					WHERE id = %s
					""",(new_number, db_expired[0]))
				db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)
				db_expired = db_expired[0]
				over12 = stock_products - (db_expired[1] + db_expired[2] + db_expired[3] + db_expired[4])
				cr.execute(
					"""
					UPDATE product_list_expired SET over_12 = %s
					WHERE id = %s
					""",(over12, db_expired[0]))
			if expired == True:
				new_number = db_expired[4] +1
				cr.execute(
					"""
					UPDATE product_list_expired SET expired = %s
					WHERE id = %s
					""",(new_number, db_expired[0]))
				db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)
				db_expired = db_expired[0]
				over12 = stock_products - (db_expired[1] + db_expired[2] + db_expired[3] + db_expired[4])
				cr.execute(
					"""
					UPDATE product_list_expired SET over_12 = %s
					WHERE id = %s
					""",(over12, db_expired[0]))
		else:
			if mon0_4 == True:
				mon0_4 = 1
			else:
				mon0_4 = 0
			if mon5_8 == True:
				mon5_8 = 1
			else:
				mon5_8 = 0
			if mon9_12 == True:
				mon9_12 = 1
			else:
				mon9_12 = 0
			if expired == True:
				expired = 1
			else:
				expired = 0

			over12 = stock_products - (mon0_4 + mon5_8 + mon9_12 + expired)

			cr.execute(
				"""
				INSERT INTO product_list_expired 
				(shop_is_m2o, ean13, name, month0_4, month5_8,
				month9_12, over_12, db_num, expired) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
				""",(branch.id, ean13, name, mon0_4, mon5_8, mon9_12, over12, stock_products, expired))

			cr.execute(
				"""
				INSERT INTO product_list_expired_log 
				(shop_is_m2o, ean13, name, month0_4, month5_8,
				month9_12, over_12, db_num, expired, date_register) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				""",(branch.id, ean13, name, mon0_4, mon5_8, mon9_12, over12, stock_products, expired, datetime.now()))

		self.write(cr, uid, ids, {
            'state': 'ean13',
            'code_ean13': '',
            'mon0_4': False,
            'mon5_8': False,
            'mon9_12': False,
            'expired': False,
        }, context=context)
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'expiration.product',
            'target': 'new',
         }

  	def get_branch(self, cr, uid, ids,context = { }):
		"""
		Metodo obtener la sucursal
		"""
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
		self.write(cr, uid, ids, {
            'branch': branch.id,
            'state': 'ean13',
        }, context=context)
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'expiration.product',
            'target': 'new',
        }
expiration_product()
