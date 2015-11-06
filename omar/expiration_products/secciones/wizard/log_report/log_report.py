# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

#Librerias para generar archivo excel
import xlwt
import base64
import tempfile

import time
from pytz import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from osv import fields, osv
from openerp.tools.translate import _

#Modelo 
class log_expired_report(osv.TransientModel) :	

	#Descripcion 
	_description = 'Server changes'

	#Nombre del Modelo
	_name = 'log.expired.report'

	_columns = {
		'location': fields.many2one('sale.shop', 'Branch'),
		'product': fields.many2one('product.product', 'Product'),
		'start_date': fields.date("Start date"),
		'end_date': fields.date("End date"),
		'state': fields.selection([('choose', 'Choose'),
                                   ('get', 'Get')]),
		'report_name': fields.char('File name', size=128,
                                readonly=True, help='This is File name'),
		'report_xls': fields.binary(
            'File', readonly=True, help='You can export file'),
		}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
		'state': 'choose',
		'start_date': lambda *a: time.strftime('%Y-%m-01'),
		'end_date': ((datetime.now(timezone( 'America/Mexico_City' )) + relativedelta(day=1, months=+1, days=-1)).date()).strftime('%Y-%m-%d'),
	}

	#Reestricciones desde código
	_constraints = [ ]

	#Reestricciones desde BD
	_sql_constraints = [ ]

	#Genera el reporte en formato de excel
	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		""" 
		#Obtiene los datos ingresados para crear el reporte
		start_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).start_date
		end_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).end_date
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).location
		product = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product

		#Obtiene la información del producto en base a los datos ingresados por el usuario
		if branch and product:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12, over_12,
	          expired, db_num, date_register, user_id
	          FROM product_list_expired_log
	          WHERE shop_is_m2o = %s
	          AND ean13 = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY product_list_expired_log.date_register
	        """,(branch.id, product.ean13, start_date, end_date,))

		if product and not branch:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12, over_12,
	          expired, db_num, date_register, user_id
	          FROM product_list_expired_log
	          WHERE ean13 = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY product_list_expired_log.date_register
	        """,(product.ean13, start_date, end_date,))

		if branch and not product:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12, over_12,
	          expired, db_num, date_register, user_id
	          FROM product_list_expired_log
	          WHERE shop_is_m2o = %s
	          AND date_register BETWEEN %s and %s
	          ORDER BY product_list_expired_log.date_register
	        """,(branch.id, start_date, end_date,))

	   	if not product and not branch:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12, over_12,
	          expired, db_num, date_register, user_id
	          FROM product_list_expired_log
	          WHERE date_register BETWEEN %s and %s
	          ORDER BY product_list_expired_log.date_register
	        """,(start_date, end_date,))

		db_results = cr.fetchall()

		#Se agrega formato par el archivo de excel
		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if db_results:
			#Se agrega cabeceras para el archivo de excel
			ws.write(0, 0, "Sucursal", style)
			ws.write(0, 1, "Ean13", style)
			ws.write(0, 2, "Nombre", style)
			ws.write(0, 3, "1-4 Meses", style)
			ws.write(0, 4, "5-8 Mese", style)
			ws.write(0, 5, "9-12 Meses", style)
			ws.write(0, 6, u"Más de 12 meses", style)
			ws.write(0, 7, "Caduco", style)
			ws.write(0, 8, "Total en la BD", style)
			ws.write(0, 9, "Fecha", style)
			ws.write(0, 10, "Usuario", style)

		j=1
		#Recorre los resultados del la base de datos y escribe el archivo de excel
		for result in db_results:
			for colum in range(len(result)):
				if colum == 0:
					cr.execute(
						"""
				          SELECT name
				          FROM sale_shop
				          WHERE id = %s
				        """,(result[0],))
					branch_name = cr.fetchone()
					branch_name = branch_name[0]
					ws.write(j, colum, branch_name)

				if colum > 0 and colum < 9:
					ws.write(j, colum, result[colum])

				if colum == 9:
					date = datetime.strptime(str(result[colum]), "%Y-%m-%d %H:%M:%S.%f")
					date = date.strftime("%d-%m-%Y %H:%M")
					ws.write(j, colum, date)

				if colum == 10:
					cr.execute(
						"""
				          SELECT pa.name
				          FROM res_users us
				          INNER JOIN res_partner pa
				          ON us.partner_id = pa.id
				          WHERE us.id = %s
				        """,(result[10],))
					user_name = cr.fetchone()
					user_name = user_name[0]
					ws.write(j, colum, user_name)

			j = j+1

		#Información para el nombre el archivo de excel
		date = datetime.now(timezone( 'America/Mexico_City' )).strftime("%d-%m-%Y %H:%M")
		repo_name = "Reporte de cambios " + " " + date +".xls"

		with tempfile.NamedTemporaryFile(delete=False) as fcsv:
			wb.save(fcsv.name)
		with open(fcsv.name, 'r') as fname:
			data1 = fname.read()

		#Genera el archivo de excel
		self.write(cr, uid, ids, {
            'state': 'get',
            'report_name': repo_name,
            'report_xls': base64.encodestring(data1),
        }, context=context)
		
		#Muestra el wizard de descarga de los archivos
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'log.expired.report',
            'target': 'new',
        }

			
log_expired_report()

