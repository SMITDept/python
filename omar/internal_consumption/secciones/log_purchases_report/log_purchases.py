# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
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
class log_purchases_internal_consumption(osv.TransientModel) :	

	#Descripcion 
	_description = 'Changes in the register of purchases'

	#Nombre del Modelo
	_name = 'log.purchases.internal.consumption'

	_columns = {
		'product': fields.many2one('products.internal.consumption', 'Product'),
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
		'end_date': ((datetime.now(timezone('America/Mexico_City'))+ relativedelta(day=1, months=+1, days=-1)).date()).strftime('%Y-%m-%d'),
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
		product = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product

		if product:
			cr.execute(
			"""
	          SELECT product_id, pieces, price, 
	          date_register, user_id
	          FROM purchases_internal_consumption
	          WHERE product_id = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY purchases_internal_consumption.date_register
	        """,(product.id, start_date, end_date,))

		else:
			cr.execute(
			"""
	          SELECT product_id, pieces, price, 
	          date_register, user_id
	          FROM purchases_internal_consumption
	          WHERE date_register BETWEEN %s and %s
	          ORDER BY purchases_internal_consumption.date_register
	        """,(start_date, end_date,))

		db_results = cr.fetchall()

		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if db_results:
			ws.write(0, 0, "Producto", style)
			ws.write(0, 1, "Piezas", style)
			ws.write(0, 2, "Precio por pieza", style)
			ws.write(0, 3, "Unidad de medida", style)
			ws.write(0, 4, "Fecha de la compra", style)
			ws.write(0, 5, "Usuario", style)
			ws.write(0, 6, "Total de la compra", style)

		j=1
		for result in db_results:
			for colum in range(len(result)):

				if colum == 0:
					cr.execute(
						"""
				          SELECT name
				          FROM products_internal_consumption
				          WHERE id = %s
				        """,(result[colum],))
					name = cr.fetchone()
					ws.write(j, colum, name[0])

				if colum == 3:
					date = datetime.strptime(str(result[colum]), "%Y-%m-%d %H:%M:%S.%f")
					date = date + timedelta(hours=-5)
					date = date.strftime("%d-%m-%Y %H:%M")
					ws.write(j, colum+1, date)

				if colum == 4:
					cr.execute(
						"""
				          SELECT pa.name
				          FROM res_users us
				          INNER JOIN res_partner pa
				          ON us.partner_id = pa.id
				          WHERE us.id = %s
				        """,(result[colum],))
					user_name = cr.fetchone()
					user_name = user_name[0]
					ws.write(j, colum+1, user_name)

				if colum > 0 and colum <= 2:
					ws.write(j, colum, result[colum])

			total_buy = result[1] * result[2]
			ws.write(j, 6, total_buy)

			cr.execute(
			"""
	          SELECT measure
	          FROM products_internal_consumption
	          WHERE id = %s
	        """,(result[0],))
			name = cr.fetchone()
			ws.write(j, 3, name[0])
			j = j+1

		date = datetime.now(timezone('America/Mexico_City'))
		date = date.strftime("%d-%m-%Y %H:%M")
		repo_name = "Reporte de compras " + " " + date +".xls"

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
            'res_model': 'log.purchases.internal.consumption',
            'target': 'new',
        }

			
log_purchases_internal_consumption()

