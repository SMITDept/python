# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
from openerp.osv import osv,fields

#Modelo 
class departments_internal_consumption(osv.osv):

	#Nombre del Modelo
    _name = 'departments.internal.consumption'

    _columns = {
        'name': fields.char('Department name', size=50, required=True),
    }

    _defaults = {
        
    }

departments_internal_consumption()
