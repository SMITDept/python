# -*- coding: utf-8 -*-

#OpenERP imports
from openerp.osv import osv,fields

#Modulo :: 
class location_user( osv.osv ) :
		
	#Nombre del modelo
	_name = 'location_user'

	_rec_name = 'sucursal'
	
	#Nombre de la tabla
	_table = 'location_user'
	
	_columns = {
	# =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
	'sucursal' : fields.char( 'Branch', size = 80, required = True ),
	}

	#Valores por defecto de los campos del diccionario [_columns]
	_defaults = {

	}
	#Restricciones de BD (constraints)
	_sql_constraints = []
	#Restricciones desde codigo
	_constraints = []
	

location_user()
