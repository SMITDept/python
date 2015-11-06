# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

#Librerias para generar archivo excel
import xlwt
import base64
import tempfile

import time
from pytz import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from osv import fields, osv

#Modelo 
class products_report(osv.TransientModel) :	

	#Descripcion 
	_description = 'Report of the products'

	#Nombre del Modelo
	_name = 'products.report'

	_columns = {    
		'branch': fields.many2one('sale.shop', 'Branch'),
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
	}

	#Reestricciones desde código
	_constraints = [ ]

	#Reestricciones desde BD
	_sql_constraints = [ ]

	#Genera el archivo excel
	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		"""
		#Obtiene la sucursal ingresada por el usuario
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
		choose_branch = "Todas las sucursales"

		#Obtiene los productos en base a la sucursal
		if branch:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12,
	          over_12, expired, db_num, user_id
	          FROM product_list_expired
	          WHERE shop_is_m2o = %s
	        """,(branch.id,))

			data_db = cr.fetchall()

			cr.execute(
				"""
		          SELECT name
		          FROM sale_shop
		          WHERE id = %s
		        """,(branch.id,))
			choose_branch = cr.fetchone()
			choose_branch = choose_branch[0]
		else:
			cr.execute(
			"""
	          SELECT shop_is_m2o, ean13, name,
	          month0_4, month5_8, month9_12,
	          over_12, expired, db_num, user_id
	          FROM product_list_expired
	        """,(branch.id,))

			data_db = cr.fetchall()

		#Estilos para el archivo de excel
		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if data_db:
			#Se ingresa el nombre de las columnas del archivo de excel
			ws.write(0, 0, "Sucursal", style)
			ws.write(0, 1, "Ean13", style)
			ws.write(0, 2, "Nombre", style)
			ws.write(0, 3, "1-4 Meses", style)
			ws.write(0, 4, "5-8 Mese", style)
			ws.write(0, 5, "9-12 Meses", style)
			ws.write(0, 6, u"Más de 12 meses", style)
			ws.write(0, 7, "Caduco", style)
			ws.write(0, 8, "Total en la BD", style)
			ws.write(0, 9, "Usuario", style)
			j=1

			#Recorre los productos encontrados y escribe la información en el archivo de excel
			for data in data_db:
				for colum in range(len(data)):
					if colum == 0:
						cr.execute(
							"""
					          SELECT name
					          FROM sale_shop
					          WHERE id = %s
					        """,(data[0],))
						branch_name = cr.fetchone()
						branch_name = branch_name[0]
						ws.write(j, colum, branch_name)
					if colum == 9:
						cr.execute(
							"""
					          SELECT pa.name
					          FROM res_users us
					          INNER JOIN res_partner pa
					          ON us.partner_id = pa.id
					          WHERE us.id = %s
					        """,(data[9],))
						user_name = cr.fetchone()
						user_name = user_name[0]
						ws.write(j, colum, user_name)

					if colum > 0 and colum < 9:
						ws.write(j, colum, data[colum])
				j = j+1

		#Nombre del archivo excel
		date = datetime.now(timezone( 'America/Mexico_City' )).strftime("%d-%m-%Y %H:%M")
		repo_name = "Reporte de caducidades " + choose_branch + " " + date +".xls"

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
		
		#Muestra el wizard del descarga del archivo
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'products.report',
            'target': 'new',
        }

products_report()

