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
class log_stock_internal_consumption(osv.TransientModel) :	

	#Descripcion 
	_description = 'Server changes'

	#Nombre del Modelo
	_name = 'log.stock.internal.consumption'

	_columns = {
		'department': fields.many2one('departments.internal.consumption', 'Department'),
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
		'end_date': ((datetime.now() + relativedelta(day=1, months=+1, days=-1)).date()).strftime('%Y-%m-%d'),
	}


	#Reestricciones desde BD
	_sql_constraints = [ ]

	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		""" 
		start_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).start_date
		end_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).end_date
		department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department
		product = self.pool.get( self._name ).browse( cr, uid, ids[0] ).product

		if department and product:
			cr.execute(
			"""
	          SELECT department_id, product_id, quantity,
	          date_register, user_id
	          FROM log_stock_departments_internal_consumption
	          WHERE department_id = %s
	          AND product_id = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY log_stock_departments_internal_consumption.date_register
	        """,(department.id, product.id, start_date, end_date,))

		if product and not department:
			cr.execute(
			"""
	          SELECT department_id, product_id, quantity,
	          date_register, user_id
	          FROM log_stock_departments_internal_consumption
	          WHERE product_id = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY log_stock_departments_internal_consumption.date_register
	        """,(product.id, start_date, end_date,))

		if department and not product:
			cr.execute(
			"""
	          SELECT department_id, product_id, quantity,
	          date_register, user_id
	          FROM log_stock_departments_internal_consumption
	          WHERE department_id = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY log_stock_departments_internal_consumption.date_register
	        """,(department.id, start_date, end_date,))

	   	if not product and not department:
			cr.execute(
			"""
	          SELECT department_id, product_id, quantity,
	          date_register, user_id
	          FROM log_stock_departments_internal_consumption
	          WHERE date_register BETWEEN %s and %s
	          ORDER BY log_stock_departments_internal_consumption.date_register
	        """,(start_date, end_date,))

		db_results = cr.fetchall()

		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if db_results:
			ws.write(0, 0, "Departamento", style)
			ws.write(0, 1, "Producto", style)
			ws.write(0, 2, "Cantidad", style)
			ws.write(0, 3, "Fecha de registro", style)
			ws.write(0, 4, "Usuario", style)

		j=1
		for result in db_results:
			for colum in range(len(result)):
				if colum == 0:
					cr.execute(
						"""
				          SELECT name
				          FROM departments_internal_consumption
				          WHERE id = %s
				        """,(result[colum],))
					name = cr.fetchone()
					ws.write(j, colum, name[0])

				if colum == 1:
					cr.execute(
						"""
				          SELECT name
				          FROM products_internal_consumption
				          WHERE id = %s
				        """,(result[colum],))
					name = cr.fetchone()
					ws.write(j, colum, name[0])

				if colum == 2:
					ws.write(j, colum, result[colum])

				if colum == 3:
					date = datetime.strptime(str(result[colum]), "%Y-%m-%d %H:%M:%S.%f")
					date = date.strftime("%d-%m-%Y %H:%M")
					ws.write(j, colum, date)

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
					ws.write(j, colum, user_name[0])

			j = j+1

		date = datetime.today()+timedelta(hours=-5)
		date = date.strftime("%d-%m-%Y %H:%M")
		repo_name = "Cambios en stock " + " - " + date +".xls"

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
            'res_model': 'log.stock.internal.consumption',
            'target': 'new',
        }

			
log_stock_internal_consumption()

