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

#Modelo 
class log_orders_internal_consumption(osv.TransientModel) :	

	#Descripcion 
	_description = 'orders repost'

	#Nombre del Modelo
	_name = 'log.orders.internal.consumption'

	_columns = {
		'department': fields.many2one('departments.internal.consumption', 'Department'),
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
		'end_date': ((datetime.now(timezone('America/Mexico_City')) + relativedelta(day=1, months=+1, days=-1)).date()).strftime('%Y-%m-%d'),
	}

	#Reestricciones desde código
	_constraints = [ ]

	#Reestricciones desde BD
	_sql_constraints = [ ]

	#Funciones que genera el reporte en formato excel.
	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		"""
		#Se obtiene la información ingresada por el usuario
		start_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).start_date
		end_date = self.pool.get( self._name ).browse( cr, uid, ids[0] ).end_date
		department = self.pool.get( self._name ).browse( cr, uid, ids[0] ).department

		#Se realiza la consulta a la base de datos dependiendo de la información proporcionada
		if department:
			cr.execute(
			"""
	          SELECT department, id, state, 
	          date_register, user_id
	          FROM update_product_internal_consumption
	          WHERE department = %s 
	          AND date_register BETWEEN %s and %s
	          ORDER BY update_product_internal_consumption.date_register
	        """,(department.id, start_date, end_date,))

		else:
			cr.execute(
			"""
	          SELECT department, id, state, 
	          date_register, user_id
	          FROM update_product_internal_consumption
	          WHERE date_register BETWEEN %s and %s
	          ORDER BY update_product_internal_consumption.date_register
	        """,(start_date, end_date,))

		db_results = cr.fetchall()

		#Creación de variables con los estilos para el documento.
		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if db_results:
			#Nombre de las columnas para el archivo excel.
			ws.write(0, 0, "Departamento", style)
			ws.write(0, 1, "Producto", style)
			ws.write(0, 2, "Cantidad", style)
			ws.write(0, 3, "Estado", style)
			ws.write(0, 4, "Fecha de la orden", style)
			ws.write(0, 5, "Usuario", style)

		j=1

		#Se recorren los resultados de la consulta a la base de datos y se escriben en el archivo de excel
		for result in db_results:
			cr.execute(
				"""
				SELECT product_id, quantity
				FROM temporary_orders_internal_consumption 
				WHERE order_m2o_id = %s
				""",(result[1],))
			productos = cr.fetchall()
			for producto in productos:

				cr.execute(
					"""
			          SELECT name
			          FROM products_internal_consumption
			          WHERE id = %s
			        """,(producto[0],))
				name = cr.fetchone()
				ws.write(j, 1, name[0])
				ws.write(j, 2, producto[1])

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

					if colum == 2:
						ws.write(j, 3, result[colum])


					if colum == 3:
						date = datetime.strptime(str(result[colum]), "%Y-%m-%d %H:%M:%S.%f")
						date = date + timedelta(hours=-5)
						date = date.strftime("%d-%m-%Y %H:%M")
						ws.write(j, 4, date)

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
						ws.write(j, 5, user_name)
				j = j+1

		#Nombre del archivo de excel
		date = datetime.now(timezone('America/Mexico_City'))
		date = date.strftime("%d-%m-%Y %H:%M")
		repo_name = "Reporte de ordenes " + " " + date +".xls"

		with tempfile.NamedTemporaryFile(delete=False) as fcsv:
			wb.save(fcsv.name)
		with open(fcsv.name, 'r') as fname:
			data1 = fname.read()

		#Se crea el archivo de excel
		self.write(cr, uid, ids, {
            'state': 'get',
            'report_name': repo_name,
            'report_xls': base64.encodestring(data1),
        }, context=context)
		
		#Se muestra el wizard para la descarga del archivo de excel
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'log.orders.internal.consumption',
            'target': 'new',
        }

			
log_orders_internal_consumption()

