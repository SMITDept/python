# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                      #
#  @creacion    : 2015-10-22 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
#  @descripcion: Modelo para almacenamiento de datos capturados en wizard de registro de Productos                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv

#Modulo :: Lista de Registro de Productos
class merma_seleccion( osv.osv ) :

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'merma_seleccion'
  
  #Nombre de la tabla
  _table = 'merma_seleccion'
  
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  # _rec_name = 'producto'
  
  #Cláusula SQL "ORDER BY"
  _order = 'id DESC'

  #Columnas y/o campos Tree & Form
  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
    'contador_product' : fields.integer( 'Numero' ),
    'clave_ide' : fields.char( 'Clave' ),
    'ide_wizard' : fields.integer( 'ID Registro' ),
    # 'elegir':fields.boolean('Seleccionar'),
    'fecha_creacion':fields.date("Fecha", required=False),
    # 'fecha_realizo_mov' : fields.char("Fecha realizo", required=False),
    'name_login' : fields.char("Empleado", required=False),
    'name_move' : fields.char("Movimiento", required=False),
    'ean13':fields.char("Codigo EAN13", required=False),
    'producto':fields.char("Producto", required=False),
    'cantidad':fields.float('Cantidad', required=False),
    'unidad_med':fields.char("Unidad de Medida", required=False),
    'precio_prod':fields.float('Precio', required=False),
    # 'nombre_localidad':fields.char("Localizacion", required=False),
    # 'nombre_destino':fields.char("Destino", required=False),
    'estado':fields.char("Estado del movimiento", required=False),
    # ========================================================  Relaciones [many2many](m2m) ======================================================== #
    'usuario_m2o_id': fields.many2one(
      'res.users',
      'Usuario'
    ),
    'producto_s_m2o_id': fields.many2one(
      'product.product',
      'Producto'
    ),
    'product_m2o_med_id': fields.many2one('product.uom', 'Unidad de Medida'),
    
    'location_id': fields.many2one('stock.location', 'Ubicacion origen', select=True),
    'destino_id': fields.many2one('stock.location', 'Ubicacion Destino', select=True),

    'almacen_m2o_id': fields.many2one(
      'stock.warehouse',
      'Tienda'
    ),
    
    # 'merma_m2o_id': fields.many2one(
    #   'merma',
    #   'Merma'
    # ),
    
  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
  # 'elegir' : True,
  }

merma_seleccion()
