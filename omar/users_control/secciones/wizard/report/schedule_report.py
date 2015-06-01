# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
import time
from datetime import datetime
from openerp.tools.translate import _
from osv import fields, osv
import pooler

#Modelo 
class schedule_report( osv.osv_memory ) :	

	#Descripcion 
	_description = 'Schedule report'

	#Nombre del Modelo
	_name = 'schedule.report'

	_columns = {    
		'rango_fechas': fields.boolean("Por Rango de Fechas"),
		'fecha_inicio': fields.date("Fecha inicio", required=True),
		'fecha_fin': fields.date("Fecha fin", required=True),
		'employee_number': fields.char("Employee Number", size=10),
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
		Metodo para imprimir el reporte en formato PDF
		* Argumentos OpenERP: [cr, uid, ids, context]
		@return dict 
		"""  
		res = {}
		if resultado is None:
				resultado = {}
		data = {}
		data['ids'] = context.get('active_ids', [])
		data['model'] = resultado.get('active_model', 'ir.ui.menu')
		data['form'] = self.read(cr, uid, ids )[0]
		
		#Inicializando la variable datas# -*- coding: utf-8 -*-, con el modelo del catalogo
		datas = {
				'ids': [],
				'model': 'time_control',
				'form': data,
		}
		#Retorna el tipo de reporte, nombre del reporte y los campos de la forma
		return {
           'type': 'ir.actions.report.xml',
           'report_name': 'schedule_report',
           'datas': datas,
           'nodestroy': True,
       	}
		print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"

schedule_report()

