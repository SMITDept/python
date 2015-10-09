# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
import xlwt
import time
import base64
import tempfile

from pytz import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
from osv import fields, osv
#Modelo

def comparision_dates(date_register):
	date = datetime.now(timezone( 'America/Mexico_City' )).strftime("%d-%m-%Y %H:%M")
	date = date.split(" ")
	date = date[0].split("-")
	month1 = int(date[1])

	db_date = date_register.split(" ")
	date = db_date[0].split("-")
	month2 = int(date[1])

	register = month1 - month2
	return register


class next_expire_report(osv.TransientModel) :	

	#Descripcion 
	_description = 'Next products to expire'

	#Nombre del Modelo
	_name = 'next.expire.report'

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

	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		"""
		branch = self.pool.get( self._name ).browse( cr, uid, ids[0] ).branch
		choose_branch = "Todas las sucursales"
		print branch
		if branch:
			cr.execute(
			"""
	          SELECT db_num, ean13, name, date_register,
	          shop_is_m2o, month0_4, month5_8,
	          month9_12, over_12, expired, user_id
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
	          SELECT db_num, ean13, name, date_register, 
	          shop_is_m2o, month0_4, month5_8, month9_12,
	          over_12, expired, user_id
	          FROM product_list_expired
	        """,(branch.id,))

			data_db = cr.fetchall()

		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if data_db:
			ws.write(0, 0, "Caduco", style)
			ws.write(0, 1, "1 Mes", style)
			ws.write(0, 2, "2 Meses", style)
			ws.write(0, 3, "3 Meses", style)
			ws.write(0, 4, "4 Meses", style)
			ws.write(0, 5, "5 Meses", style)
			ws.write(0, 6, "6 Meses", style)
			ws.write(0, 7, "7 Meses", style)
			ws.write(0, 8, "8 Meses", style)
			ws.write(0, 9, "9 Meses", style)
			ws.write(0, 10, "10 Meses", style)
			ws.write(0, 11, "11 Meses", style)
			ws.write(0, 12, "12 Meses", style)
			ws.write(0, 13, u"Más de 12 meses", style)

			ws.write(0, 14, "Total en la BD", style)
			ws.write(0, 15, "Ean13", style)
			ws.write(0, 16, "Nombre", style)
			ws.write(0, 17, "Fecha de registro", style)
			ws.write(0, 18, "Sucursal", style)
			ws.write(0, 19, "Usuario", style)
			j=1
			for data in data_db:
				busy = []
			 	mon1 = 1
			 	mon2 = 5
			 	mon3 = 9
			 	mon4 = 13
				db_date = data[3]
				expired = 0
				for colum in range(len(data)):
					if colum == 4:
						cr.execute(
							"""
					          SELECT name
					          FROM sale_shop
					          WHERE id = %s
					        """,(data[4],))
						branch_name = cr.fetchone()
						branch_name = branch_name[0]
						ws.write(j, 18, branch_name)
					if colum == 5:
						result = comparision_dates(db_date)
						col = mon1 - result
						if col <= 0:
							expired = expired + data[colum]
						else:
							ws.write(j, col, data[colum])
						busy.append(col)

					if colum == 6:
						result = comparision_dates(db_date)
						col = mon2 - result
						if col <= 0:
							expired = expired + data[colum]
						else:
							ws.write(j, col, data[colum])
						busy.append(col)

					if colum == 7:
						result = comparision_dates(db_date)
						col = mon3 - result
						if col <= 0:
							expired = expired + data[colum]
						else:
							ws.write(j, col, data[colum])
						busy.append(col)

					if colum == 8:
						result = comparision_dates(db_date)
						col = mon4 - result
						if col <= 0:
							expired = expired + data[colum]
						else:
							ws.write(j, col, data[colum])
						busy.append(col)

					if colum == 9:
							expired = expired + data[colum]
							ws.write(j, 0, expired)
							busy.append(0)
					if colum == 10:
						cr.execute(
							"""
					          SELECT pa.name
					          FROM res_users us
					          INNER JOIN res_partner pa
					          ON us.partner_id = pa.id
					          WHERE us.id = %s
					        """,(data[colum],))
						user_name = cr.fetchone()
						user_name = user_name[0]
						ws.write(j, 19, user_name)

					if colum >= 0 and colum < 4:
						if colum == 3:
							current_date=datetime.strptime(data[colum], "%Y-%m-%d %H:%M:%S.%f")
							dt = current_date.strftime("%d-%m-%Y %H:%M")
							ws.write(j, 14+colum, dt)
						else:
							ws.write(j, 14+colum, data[colum])

				for x in range(1, 14):
					ban = False
					for co in busy:
						if co == x:
							ban = True
					if ban == False:
						ws.write(j, x, 0)
					
				#ws.write(j, 0, expired)

				j = j+1

		date = datetime.now(timezone( 'America/Mexico_City' )).strftime("%d-%m-%Y %H:%M")
		repo_name = u"Próximos a caducar " + choose_branch + " " + date +".xls"

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
            'res_model': 'next.expire.report',
            'target': 'new',
        }

next_expire_report()

