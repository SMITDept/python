# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

from openerp.osv import osv,fields

#Modelo
class products_internal_consumption(osv.osv):

    #Nombre del Modelo
    _name = 'products.internal.consumption'

    #Diccionario de medidas de los productos
    MEASURE = [
    ('Piezas', 'Piezas'),
    ('Caja', 'Caja'),
    ('Paquete', 'Paquete')
	]

    _columns = {
        'name': fields.char('Product name', size=100, required=True),
        'stock': fields.float("Stock products", digits=(12,3), requred=False),
        'measure': fields.selection(MEASURE, 'Measure', required=True),
    }

    #Valores por defecto de los elementos del arreglo [_columns]
    _defaults = {
        'stock': 0,
    }

products_internal_consumption()
