# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

#Librerias para generar archivo excel
import tempfile
import xlwt

#Libreria para leer el archivos en formato csv
import csv
import base64
import StringIO

import time
from datetime import datetime, timedelta, date
from openerp.osv import fields, osv
from openerp.tools.translate import _

#Devuelve la fecha en formato día/mes/año
def get_day(date):
	split = date.split("/")
	day = str(int(split[0])+1)
	date = day + "/" + split[1] + "/" + split[2]
	return date

#Resta un día si la hora de fecha es mayor a "00:00:01"  y menor a "05:59:59"
def date_time(date):
	db_date = date.split(" ")
	hours = db_date[1].split(".")
	hours = hours[0]
	if hours > "00:00:01" and hours < "05:59:59":
		current_date=datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") + timedelta(days=-1)
		current_date.strftime("%Y-%m-%d %H:%M:%S.%f")
		return current_date
	return date
    
#Modelo 
class comparision_tc_vta(osv.TransientModel):

	#Función que retorna el periodo actual.
	def _obtener_periodo( self, cr, uid, ids, context = None ):
	    """
	    Metodo para obtener por defecto el id del periodo anterior dependiendo de la fecha actual
	    * Argumentos OpenERP: [cr, uid, ids, context]
	    @return int
	    """   
	    self.query = ""
	    per_id=''
	    carry=0
	    current_date=date.today()
	    new_month=current_date.month-1
	    if new_month == 0 :
	      new_month=12
	      carry=1
	    current_date=current_date.replace(year=current_date.year-carry, month=new_month, day=1)
	    self.query = str(current_date)
	    cr.execute(
	      """
	      SELECT id
	      FROM account_period
	      WHERE date_start = '"""+ self.query +"""'
	      """)
	    registro = cr.fetchone()
	    if registro != None and type( registro ) in ( list, tuple ):
	      if (len( registro ) > 0 ):
	      #Obteniendo el ID del periodo
	        per_id = registro[0]
	    else:
	      cr.execute(
	      """
	      SELECT id
	      FROM account_period
	      ORDER BY id DESC
	      """)
	      registro = cr.fetchone()
	      per_id = registro[0]
	    return per_id

	#Descripcion del modulo
	_description = 'Comparision TC with VTA'

	#Diccionario de sucursales
	BRANCH = [
      ('1', 'Branch 1 and 2'),
      ('3', 'Branch 3'),
      ('4', 'Branch 4'),
      ('5', 'Branch 5'),
    ]

	#Nombre del Modelo
	_name = 'comparision.report'

	_columns = {
		'period': fields.many2one('account.period', 'Periodo', required=True), 
		'file_csv': fields.binary("File .csv", filters="*.csv", required=True),
		'branch':fields.selection(BRANCH, 'Branch', required=True),
		'state': fields.selection([('choose', 'Choose'),
                                   ('get', 'Get')]),
		'aux_name': fields.char('Filename', size=128,
                                readonly=True, help='This is File name'),
		'aux_xls': fields.binary(
            'File', readonly=True, help='You can export file'),
		'compa_name': fields.char('Filename', size=128,
                                readonly=True, help='This is File name'),
		'compa_xls': fields.binary(
            'File', readonly=True, help='You can export file'),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
    	'period': _obtener_periodo,
    	'state': 'choose',
  	}


  	#Funciones que genera el reporte en formato excel.
	def print_report(self, cr, uid, ids,context = { } ):
		"""
		Metodo para imprimir el reporte
		"""
		#Se obtiene el periodo seleccionado del  wizard.
		period = self.pool.get( self._name ).browse( cr, uid, ids[0] ).period

		#Creación de variables para generar archivo excel.
		wb = xlwt.Workbook(encoding="UTF-8")
		aux = xlwt.Workbook(encoding="UTF-8")

		ws = wb.add_sheet('Concialiacion')
		ax = aux.add_sheet('Auxiliar')

		#Creación de variables con los estilos para el documento.
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True;')
		red = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
		green = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')

		#Nombre de las columnas para el archivo excel.
		ws.write(0, 0, u"ID de Establecimiento", style)
		ws.write(0, 1, u"Moneda", style)
		ws.write(0, 2, u"Número de identificación de la Terminal", style)
		ws.write(0, 3, u"Número de lote", style)
		ws.write(0, 4, u"Fecha de procesamiento", style)
		ws.write(0, 5, u"Tipo de tarjeta", style)
		ws.write(0, 6, u"Número de tarjeta", style)
		ws.write(0, 7, u"Monto de la transacción", style)
		ws.write(0, 8, u"Tipo de transacción", style)
		ws.write(0, 9, u"Fecha de transacción", style)
		ws.write(0, 10, u"Estatus", style)
		ws.write(0, 11, u"Clasificación", style)
		ws.write(0, 12, u"Código de autorización", style)
		ws.write(0, 13, u"Orden de compra", style)
		ws.write_merge(0, 0, 15, 17, 'Auxiliar', style)

		obj=self.pool.get( self._name )
		datos=obj.browse( cr, uid, ids[0] )
		self.query = ""
		periodo=''
		sucursal = ''
		num_order = []

		#Variable con el periodo seleccionado.
		periodo=str(datos.period.id)
		self.query = self.query + "AND aml.period_id = " + periodo

		for line in self.browse(cr, uid, ids):
			branch = line.branch

		#SQL que retorna todas la ventas con tarjeta de crédito.
		if branch == '1':
			sucursal = "SM1 - SM2"
			cr.execute(
            """
              SELECT aml.create_date AS create_d,
              round(aml.debit,2) AS debit,
              aml.name AS name
              FROM account_move_line aml
              WHERE aml.state = 'valid'
              """+ self.query +"""
              AND aml.name LIKE 'POS%'
              AND aml.account_id = '164'
              AND (aml.ref LIKE 'SM1%' OR aml.ref LIKE 'SM2%')
              ORDER BY aml.create_date
            """)
		else:
			sucursal = "SM" + branch
			id_select = "'" + "SM" + branch + "%" + "'" 
			id_branch = "AND aml.ref LIKE " + id_select
			cr.execute(
            """
              SELECT aml.create_date AS create_d,
              round(aml.debit,2) AS debit,
              aml.name AS name
              FROM account_move_line aml
              WHERE aml.state = 'valid'
              """+ self.query +"""
              AND aml.name LIKE 'POS%'
              AND aml.account_id = '164'
              """+ id_branch +"""
              ORDER BY aml.create_date
            """)

		db_results = cr.fetchall()
		
		if db_results:
			for wiz in self.browse(cr, uid, ids, context=context):

				#Decodificación del archivo csv.
				data = base64.b64decode(wiz.file_csv)

		        #Lectura del archivo csv.
		        csv_results = csv.reader(StringIO.StringIO(data))
		        fila = 1

		        #Ciclo que recorre la información del archivo csv.
		        for csv_result in csv_results:
		        	next_csv_date = get_day(csv_result[9])
		        	bandera = False
		        	bandera2 = False
		        	if fila != 0:
			        	for db_result in db_results:
			        		b = False
			        		result = date_time(db_result[0])
			        		lst = list(db_result)
			        		lst[0] = str(result)
			        		db_result = tuple(lst)
			        		datetim = db_result[0].split(" ")
			        		split = datetim[0].split("-")
			        		year = split[0]
			        		db_date1 = split[2] + "/" + split[1] + "/" + year
		        			if csv_result[9] == db_date1 or next_csv_date == db_date1:
		        				price = csv_result[7].find(".")
		        				if price < 0:
		        					price = csv_result[7] + ".0"
		        				else:
		        					price = csv_result[7]
		        				if str(db_result[1]) == price:
		        					bandera = True
					    			if bandera2 != True:
					    				bandera2 = True
					    				for pos in num_order:
					    					if db_result[2] == pos:
					    						b = True
					    				if b == False:
						        			ws.write(fila, 13, db_result[2], style)
						        			current_date=datetime.strptime(db_result[0], "%Y-%m-%d %H:%M:%S.%f")
						        			current_date=current_date.strftime("%d-%m-%Y")
						        			ws.write(fila, 15, current_date, style)
						        			ws.write(fila, 16, db_result[1], style)
						        			ws.write(fila, 17, db_result[2], style)
						        			num_order.append(db_result[2])
						        		else:
						        			bandera2 = False
					for colum in range(len(csv_result)):
						if bandera == True :
							ws.write(fila, colum, csv_result[colum], green)
						else:
							ws.write(fila, colum, csv_result[colum], red)
		        	fila = fila+1

		#Información del archivo csv.
		date = datetime.today()+timedelta(hours=-5)
		date = date.strftime("%d-%m-%Y %H:%M")
		aux_na = "Sobrantes Auxiliar " + sucursal + " - " + date +".xls"
		compa_na = "Conciliacion " + sucursal + " - " + date +".xls"

		#Ciclo que genera el auxiliar de de las ventas de tarjeta de crédito.
		fila = 0
		for db_result in db_results:
			b =False
			result = date_time(db_result[0])
			lst = list(db_result)
			lst[0] = str(result)
			db_result = tuple(lst)
			for pos in num_order:
				if db_result[2] == pos:
					b = True
			if b == False:
				current_date=datetime.strptime(db_result[0], "%Y-%m-%d %H:%M:%S.%f")
				current_date=current_date.strftime("%d-%m-%Y")
				ax.write(fila, 0, current_date)
				ax.write(fila, 1, db_result[1])
				ax.write(fila, 2, db_result[2])
				fila = fila +1

		#Se agrega el nombre de los archivos csv.
		with tempfile.NamedTemporaryFile(delete=False) as fcsv:
			aux.save(fcsv.name)
		with open(fcsv.name, 'r') as fname:
			data1 = fname.read()
		with tempfile.NamedTemporaryFile(delete=False) as fcsv:
			wb.save(fcsv.name)
		with open(fcsv.name, 'r') as fname:
			data2 = fname.read()

		self.write(cr, uid, ids, {
            'state': 'get',
            'aux_name': aux_na,
            'aux_xls': base64.encodestring(data1),
            'compa_name': compa_na,
            'compa_xls': base64.encodestring(data2),
        }, context=context)

		#Se cambia el estado de choose a new para abrir wizard de descarga de archivos.
		this = self.browse(cr, uid, ids)[0]
		return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'res_model': 'comparision.report',
            'target': 'new',
        }
        
comparision_tc_vta()
