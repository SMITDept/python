# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
import xlwt
import base64
import StringIO
import time
import csv

from datetime import date
from datetime import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _

#Modelo 
class comparision_tc_vta( osv.osv_memory ):

	def _obtener_periodo( self, cr, uid, ids, context = None ):
	    """
	    Metodo para obtener por defecto el id del periodo anterior dependiendo de la fecha actual
	    * Argumentos OpenERP: [cr, uid, ids, context]
	    @return int
	    """   
	    
	    self.query = ""
	    per_id=''
	    current_date=date.today()
	    # current_date=date(2014,03,01)
	    carry, new_month=divmod(current_date.month-1+1, 12)
	    new_month+=-1
	    current_date=current_date.replace(year=current_date.year+carry, month=new_month, day=1)
	    self.query = str(current_date)
	    cr.execute(
	      """
	      SELECT id
	      FROM account_period
	      WHERE date_start = '"""+ self.query +"""'
	      """)
	    registro = cr.fetchone()
	    if registro:
	      #Obteniendo el ID del periodo
	      per_id = (( registro[0] ) if ( len( registro ) > 0 ) else ( None ))
	      return per_id
	    else:
	      cr.execute(
	      """
	      SELECT id
	      FROM account_period
	      ORDER BY id DESC
	      """)
	      registro = cr.fetchone()
	      per_id_ultimo = (( registro[0] ) if ( len( registro ) > 0 ) else ( None ))
	      return per_id_ultimo

	#Descripcion 
	_description = 'Comparision TC with VTA'

	#Sucursal
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
		'file_csv': fields.binary("File .csv", filters="*.csv", requires=True),
		'branch':fields.selection(BRANCH, 'Branch', required =True),
	}

	#Valores por defecto de los elementos del arreglo [_columns]
	_defaults = {
    	'period': _obtener_periodo,
  	}

	def print_report(self, cr, uid, ids,context = { } ):
		"""
		Metodo para imprimir el reporte
		""" 
		period = self.pool.get( self._name ).browse( cr, uid, ids[0] ).period

		wb = xlwt.Workbook()
		style = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                              'font: colour white, bold True;')
		red = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
		green = xlwt.easyxf('pattern: pattern solid, fore_colour green;')
		style0 = xlwt.easyxf('font: name Arial, color-index red, bold on', num_format_str='#,##0.00')
		xlwt.easyxf('font: name Arial')
		ws = wb.add_sheet('A Test Sheet')
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

		obj=self.pool.get( self._name )
		datos=obj.browse( cr, uid, ids[0] )
		self.query = ""
		periodo=''

		periodo=str(datos.period.id)
		self.query = self.query + " AND aml.period_id = " + periodo

		for line in self.browse(cr, uid, ids):
			branch = line.branch

		if branch == '1':
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
				# Decode the file data
				data = base64.b64decode(wiz.file_csv)
		        # Read the file
		        csv_results = csv.reader(StringIO.StringIO(data))
		        fila = 1
		        for csv_result in csv_results:
		        	bandera = False
		        	bandera2 = False
		        	if fila != 0:
			        	for db_result in db_results:
			        		datetime = db_result[0].split(" ")
			        		split = datetime[0].split("-")
			        		year = split[0]
			        		next_day = str(int(split[2]) +1)
			        		db_date1 = split[2] + "/" + split[1] + "/" + year
			        		#db_date2 = next_day + "/" + split[1] + "/" + year
		        			if csv_result[9] == db_date1 or csv_result[4] == db_date1:
		        				#print csv_result[9], csv_result[4]
		        				check_price = str(db_result[1]).split(".")
		        				db_price = ""
		        				if len(check_price[1]) < 2:
		        					db_price = check_price[0] + "." +check_price[1] + "0"
		        				else:
		        					db_price = str(db_result[1])
		        				#print db_price, "==", csv_result[7]
		        				if db_price == csv_result[7]:
		        					#print repor[2]
		        					bandera = True
					    			if bandera2 != True:
					    				bandera2 = True
					        			ws.write(fila, 13, db_result[2], style)
					for colum in range(len(csv_result)):
						if bandera == True:
							ws.write(fila, colum, csv_result[colum], green)
						else:
							ws.write(fila, colum, csv_result[colum], red)
		        	fila = fila+1

		wb.save('/tmp/comparision.xls')
comparision_tc_vta()
