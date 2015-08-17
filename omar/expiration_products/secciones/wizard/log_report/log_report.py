# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
import xlwt
import base64
import tempfile
import time

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
		'end_date': ((datetime.now() + relativedelta(day=1, months=+1, days=-1)).date()).strftime('%Y-%m-%d'),
	}

	#Reestricciones desde código
	_constraints = [ ]

	#Reestricciones desde BD
	_sql_constraints = [ ]

	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		""" 
		start_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).start_date
		end_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).end_date
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).location
		product = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product

		if branch and product:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12, over_12,
	          expired, db_num, date_register
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
	          expired, db_num, date_register
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
	          expired, db_num, date_register
	          FROM product_list_expired_log
	          WHERE shop_is_m2o = %s
	          AND date_register BETWEEN %s and %s
	          ORDER BY product_list_expired_log.date_register
	        """,(branch.id, start_date, end_date,))

	   	if not product and not branch:
	   		raise osv.except_osv(_( 'Warning' ),_( 'You need choose product or branch' ) )

		db_results = cr.fetchall()

		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if db_results:
			ws.write(0, 0, "Sucursal", style)
			ws.write(0, 1, "Ean13", style)
			ws.write(0, 2, "Nombre", style)
			ws.write(0, 3, "0-4 Meses", style)
			ws.write(0, 4, "5-8 Mese", style)
			ws.write(0, 5, "9-12 Meses", style)
			ws.write(0, 6, u"Más de 12 meses", style)
			ws.write(0, 7, "Caduco", style)
			ws.write(0, 8, "Total en la BD", style)
			ws.write(0, 9, "Fecha", style)

		j=1
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
				else:
					if colum == 9:
						date = datetime.strptime(str(result[colum]), "%Y-%m-%d %H:%M:%S.%f") + timedelta(hours=-5)
						date = date.strftime("%Y-%m-%d %H:%M")
						ws.write(j, colum, date)
					else:
						ws.write(j, colum, result[colum])
			j = j+1

		date = datetime.today()+timedelta(hours=-5)
		date = date.strftime("%d-%m-%Y %H:%M")
		repo_name = "Reporte de cambios " + " - " + date +".xls"

		with tempfile.NamedTemporaryFile(delete=False) as fcsv:
			wb.save(fcsv.name)
		with open(fcsv.name, 'r') as fname:
			data1 = fname.read()

		self.write(cr, uid, ids, {
            'state': 'get',
            'report_name': repo_name,
            'report_xls': base64.encodestring(data1),
        }, context=context)
		
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

