# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
from pytz import timezone
from datetime import datetime, timedelta
from osv import fields, osv

#Librerias para mostrar mensajes en pantalla
from openerp.tools.translate import _
from openerp.exceptions import Warning

#Función que recibe el id de un producto y retorna el numero total de ese producto
def get_stock(self, cr, uid, ids, product_id):
	cr.execute(
		"""
		with stockmovements as (
		select sm.location_dest_id as location_id, sl.complete_name, sm.product_qty, pt.standard_price, sl.usage, sm.product_id,
		case pu.uom_type
			when 'reference' then sm.product_qty
			when 'bigger' then round((sm.product_qty / pu.factor),2)
			when 'smaller' then round((sm.product_qty * pu.factor),2)
		end as real_qty
		from stock_move sm, product_template pt, stock_location sl, product_uom pu
		where pt.id = sm.product_id and sm.product_id = %s and sm.state = 'done' and sl.id = sm.location_dest_id and sm.product_uom = pu.id
		union all
		select sm.location_id as location_id, sl.complete_name, sm.product_qty*-1, pt.standard_price, sl.usage, sm.product_id,
		case pu.uom_type
			when 'reference' then sm.product_qty*-1
			when 'bigger' then round((sm.product_qty / pu.factor),2)*-1
			when 'smaller' then round((sm.product_qty * pu.factor),2)*-1
		end as real_qty
		from stock_move sm, product_template pt, stock_location sl, product_uom pu
		where pt.id = sm.product_id and sm.product_id = %s and sm.state = 'done' and sl.id = sm.location_id and sm.product_uom = pu.id
		)
		select  
		sum(case pu.uom_type
			when 'reference' then round(stkmvs.real_qty,3)
			when 'bigger' then round((stkmvs.real_qty * pu.factor),3)
			when 'smaller' then round((stkmvs.real_qty / pu.factor),3)
		end) as quantity
		from stockmovements stkmvs, product_template pt, product_uom pu
		where stkmvs.product_id = pt.id and pt.uom_id = pu.id
		group by usage
		having sum(stkmvs.real_qty) <> 0 and usage='internal'
		""",(product_id, product_id,))
	return cr.fetchone()

#Función que recibe numero de sucursal y código ean13 
#de un producto y retorna el producto de esa sucursal 
def get_db_data(self, cr, uid, ids, branch, ean13):
	cr.execute(
        """
          SELECT id, month0_4, month5_8,
          month9_12, expired, over_12,
          shop_is_m2o, ean13, name, db_num
          FROM product_list_expired
          WHERE shop_is_m2o = %s
          AND ean13 = %s
        """,(branch, ean13))
	db_expired = cr.fetchall()
	if db_expired:
		db_expired = db_expired[0]
	return db_expired

#Actualiza el numero de productos mayores a 12 meses
def update_data(self, cr, uid, ids, over12, id_product):
	cr.execute(
		"""
		UPDATE product_list_expired SET over_12 = %s
		WHERE id = %s
		""",(over12, id_product))

#Crea un log de los registros en el sistema
def create_log(self, cr, uid, ids, branch, ean13, name, mon0_4, 
	mon5_8, mon9_12, over12, stock_products, expired, current_user):
	cr.execute(
		"""
		INSERT INTO product_list_expired_log 
		(shop_is_m2o, ean13, name, month0_4, month5_8,
		month9_12, over_12, db_num, expired, date_register,
		user_id) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		""",(branch, ean13, name, mon0_4, mon5_8, 
			mon9_12, over12, stock_products, expired, datetime.now(timezone( 'America/Mexico_City' )),
			current_user))

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
		'mon0_4': fields.float("0-4 Months", digits=(12,3)),
        'mon5_8': fields.float("5-8 Months", digits=(12,3)),
        'mon9_12': fields.float("9-12 Months", digits=(12,3)),
		'expired': fields.float('Expired', digits=(12,3)),
		'state': fields.selection([('branch', 'Branch'),
                                   ('ean13', 'Ean13'),
                                   ('save', 'Save')]),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
    	'state': 'branch',
  	}

  	#Retorna al menú de selección de un producto
  	def back_menu(self, cr, uid, ids,context = { }):
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
		self.write(cr, uid, ids, {
            'branch': branch.id,
            'code_ean13': '',
            'state': 'ean13',
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

    #Obtiene un producto en base al código ean13
  	def get_product(self, cr, uid, ids, ean13):
  		context = ""
  		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
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

			#Crea un nuevo registro de ese producto
			cr.execute(
			"""
			DELETE FROM product_list_expired
			WHERE shop_is_m2o = %s
			AND ean13 = %s
			""",(branch.id, ean13,))

			#Muestra el wizard de registro de cantidades de productos
			if product:
				product = product[0]
				self.write(cr, uid, ids, {
					'product': product[0],
					'image': product[1],
		            'code_ean13': ean13,
		            'mon0_4': 0,
		            'mon5_8': 0,
		            'mon9_12': 0,
		            'expired': 0,
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
				raise Warning(_('El producto no existe'))
		
		#Muestra el wizard de ingreso de ean13
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

	#Crea un registro de las cantidades en existencia del producto
  	def save_product(self, cr, uid, ids,context = { }):
		"""
		Metodo obtener la sucursal
		"""
		#Se obtiene la información del producto
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
		ean13 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).code_ean13
		name = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product
		mon0_4 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).mon0_4
		mon5_8 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).mon5_8
		mon9_12 = self.pool.get( self._name ).browse( cr, uid, ids[0] ).mon9_12
		expired = self.pool.get( self._name ).browse( cr, uid, ids[0] ).expired
		current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)

		#Verifica las cantidades del producto
		cr.execute(
	        """
	          SELECT prod.id
	          FROM product_product prod
	          WHERE ean13 = %s
	        """,(ean13,))
		total_income = mon0_4 + mon5_8 + mon9_12 + expired
		print total_income
		pro = cr.fetchall()
		total = get_stock(self, cr, uid, ids, pro[0])
		if total and total[0] > 0:
			if total_income > total[0]:
				message = "Solo tienes " + str(total[0]) + " productos disponibles"
				raise Warning(_(message))
			else:
				stock_products = total[0]
		else:
			raise Warning(_('No hay producto en existencia'))
		
		#Obtiene el numero de productos
		db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)

		#Verifica si existe información del producto en la base de datos
		if db_expired:

			#Actualiza la información del producto y crea un registro en el log
			cr.execute(
				"""
				UPDATE product_list_expired SET month0_4 = %s,
				month5_8 = %s, month9_12 = %s, expired = %s
				WHERE id = %s
				""",(mon0_4, mon5_8, mon9_12, expired, db_expired[0]))
			db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)
			over12 = stock_products - (db_expired[1] + db_expired[2] + db_expired[3] + db_expired[4])
			update_data(self, cr, uid, ids, over12, db_expired[0])
			db_expired = get_db_data(self, cr, uid, ids, branch.id, ean13)
			create_log(self, cr, uid, ids, db_expired[6], db_expired[7],
				db_expired[8], db_expired[1], db_expired[2],
				db_expired[3], db_expired[5], stock_products, db_expired[4])

		else:

			over12 = stock_products - (mon0_4 + mon5_8 + mon9_12 + expired)

			#Crea el registro de un producto y crea un registro en el log
			cr.execute(
				"""
				INSERT INTO product_list_expired 
				(shop_is_m2o, ean13, name, month0_4, month5_8,
				month9_12, over_12, db_num, expired, date_register, user_id) 
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				""",(branch.id, ean13, name, mon0_4, mon5_8, mon9_12, over12, stock_products, expired, datetime.now(timezone( 'America/Mexico_City' )), current_user.id))
			create_log(self, cr, uid, ids, branch.id, ean13, name, mon0_4, mon5_8,
						mon9_12, over12, stock_products, expired, current_user.id)

		#Muestra el wizard de ingreso de ean13
		self.write(cr, uid, ids, {
            'state': 'ean13',
            'code_ean13': '',
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
