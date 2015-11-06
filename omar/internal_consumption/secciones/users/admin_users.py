# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

from openerp.osv import osv,fields

#Modelo 
class users_internal_consumption(osv.osv):

	#Nombre del Modelo
    _name = 'users.internal.consumption'

    _columns = {
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    #Valores por defecto de los elementos del arreglo [_columns]
    _defaults = {
        
    }

users_internal_consumption()