# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
import time
from datetime import datetime
from openerp.exceptions import Warning
from openerp.osv import fields, osv
from openerp.osv.osv import except_osv
from openerp.tools.translate import _

import xlwt


#Modelo 
class schedule_report( osv.osv_memory ) :	

	#Descripcion 
	_description = 'Schedule report'

	#Nombre del Modelo
	_name = 'schedule.report'

	_columns = {    
		'rango_fechas': fields.boolean("By date range"),
		'fecha_inicio': fields.date("Start date", required=True),
		'fecha_fin': fields.date("End date", required=True),
		'location': fields.many2one('location_user', 'Location', required=False),
		}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
		'rango_fechas': True,
		'fecha_inicio': lambda *a: time.strftime('%Y-01-01'),
		'fecha_fin': lambda *a: time.strftime('%Y-12-12'),
	}

	#Reestricciones desde código
	_constraints = [ ]

	#Reestricciones desde BD
	_sql_constraints = [ ]

	def print_report(self, cr, uid, ids,context = { } ) :
		"""
		Metodo para imprimir el reporte
		""" 
		inicio = self.pool.get( self._name ).browse( cr, uid, ids[0] ).fecha_inicio
		fin = self.pool.get( self._name ).browse( cr, uid, ids[0] ).fecha_fin
		sucursal = self.pool.get( self._name ).browse( cr, uid, ids[0] ).location

		if sucursal:
			cr.execute(
			"""
	          SELECT employee, location_m2o_id, date_register, start_time, start_food, end_food, end_time, total_hours
	          FROM time_control
	          WHERE location_m2o_id = %s and date_register BETWEEN %s and %s
	        """,(sucursal.id, inicio, fin,))
		else:
			cr.execute(
			"""
	          SELECT employee, location_m2o_id, date_register, start_time, start_food, end_food, end_time, total_hours
	          FROM time_control
	          WHERE date_register BETWEEN %s and %s
	        """,(inicio, fin,))

		report = cr.fetchall()

		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True; align: vert centre;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')

		if report:

			ws.write(0, 0, "Empleado", style)
			ws.write(0, 1, "Sucursal", style)
			ws.write(0, 2, "Fecha", style)
			ws.write(0, 3, "Hora inicio", style)
			ws.write(0, 4, "Hora inicio de comida", style)
			ws.write(0, 5, "Hora fin de comida", style)
			ws.write(0, 6, "Hora fin", style)
			ws.write(0, 7, "Total de tiempo", style)
			ws.write(0, 8, "Tiempo extra", style)

			for i in range(len(report)):
				for j in range(len(report[i])):
					if j == 0:
						cr.execute(
							"""
					          SELECT name, first_name, second_name
					          FROM schedule_users
					          WHERE employee_number = %s
					        """,(report[i][j],))
						name = cr.fetchone()
						name = name[0] + " " + name[1] + " " + name[2]
						ws.write(i+1, j, name)
					if j == 1:
						cr.execute(
							"""
					          SELECT sucursal
					          FROM location_user
					          WHERE id = %s
					        """,(report[i][j],))
						sucursal = cr.fetchone()
						ws.write(i+1, j, sucursal)
					if j > 2 and j < 7:
						hour = report[i][j]
						if hour:
							hour = str(hour).split(' ')
							print hour[1]
							ws.write(i+1, j, hour[1])
						else:
							ws.write(i+1, j, hour)
						
					if j == 7:
						if report[i][j] == "0:0":
							ws.write(i+1, j, report[i][j], style0)
						else:
							ws.write(i+1, j, report[i][j])
							time = report[i][j].split(':')
							if int(time[0]) >7:
								hour = int(time[0])-8
								minute = time[1]
								tim_ext = str(hour) + ":" + minute
								ws.write(i+1, j+1, tim_ext)
					if j == 2:
						ws.write(i+1, j, report[i][j])
			#raise Warning(_('Reporte generado.'))
		#else:
			#raise Warning(_('No se encontraron resultados.'))
		return wb.save('/tmp/report.xls')
		
schedule_report()

