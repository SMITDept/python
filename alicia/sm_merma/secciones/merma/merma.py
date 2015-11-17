# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                      #
#  @creacion    : 2015-10-20 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv
import time
import datetime



#Modulo :: 
class merma( osv.osv ) :
  #--------------------------------------------------------Variables Privadas y Publicas--------------------------------------------------------------
  loc_desechos= [
    ('merma', 'Merma'),
    ('caducado', 'Caducado'),
    ('desperdicio', 'Desperdicio'),
  ]
  
  TIENDA = [
    ('sm1', 'SM1 Merma'),
    ('sm2', 'SM2 Merma'),
    ('sm3', 'SM3 Merma'),
    ('smx', 'Todas'),
  ]
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def accion_confirmar(self, cr, uid, ids, context=None):
    """
    Confirma la lista de productos y escribe su fecha final
    @return: True
    """
    if context is None:
        context = {}
    id_merma = ids[0]
    self.write(cr, uid, ids, {
            'state': 'confirm'
        }, context=context)

    # for inv in self.browse(cr, uid, ids, context=context):
    #     move_ids = []
    #     
    #     move_ids.append(self._inventory_line_hook(cr, uid, line, value))
    #self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
    # self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
    # self.pool.get('stock.move').action_confirm(cr, uid, move_ids, context=context)
    return True
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def _obtenerIdLogueado( self, cr, uid, ids = None, field_name = None, arg = None, context = None ) :
    """
    Función para el campo "Autor"
    * Para OpenERP [field.function( empleado_autor )]
    * Argumentos OpenERP: [cr, uid, ids, field_name, arg, context]
    @return dict
    """
    result = {}
    for record in self.browse( cr, uid, ids, context ) :
      obj_user = self.pool.get( 'res.users' ).browse( cr, 1, uid )
      nombre_empleado=obj_user.partner_id.name
      result[record.id] = nombre_empleado
    #Retornando los resultados evaluados
    return result
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def obtenerProductos( self, cr, uid, ids, context = None ):
    """
    Funcion que obtiene el desecho ingresado en el registro de productos
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @param : (cr, uid, ids, context) 
    @return dic
    """
    obj_merma = self.pool.get( self._name ).browse( cr, uid, ids[0] )
    fecha_mov = obj_merma.fecha_mov
    tienda_alm = obj_merma.almacen_m2o_id.id
    autor_uid = uid
    id_merma = ids[0]
    if obj_merma :
      cr.execute(
      """
      SELECT
      id
      FROM merma_seleccion
      WHERE almacen_m2o_id=%s AND
      TO_CHAR(create_date,'YYYY-MM-DD')=%s
      """,(tienda_alm, fecha_mov,) )
      resultado = cr.fetchall()
      if resultado != None and type( resultado ) in ( list, dict) :
        obj_selec=self.pool.get( 'merma_seleccion' )
        for id_selec in resultado:
          id_select = id_selec[0]
   
          cr.execute(
              """
              INSERT INTO merma_m2m_selec_merma
              (merma_m2o_id, select_merma_m2o_id)
              VALUES (%s, %s)
              """, (id_merma, id_select) )
       
    else :
      return { 'value' : {} }
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                             METODOS ORM                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def create(self, cr, uid, vals, context = None ):
    """   
    Método "create" que se ejecuta justo antes (o al momento) de CREAR un nuevo registro en OpenERP.    
    * Argumentos OpenERP: [cr, uid, vals, context]    
    @param  
    @return bool    
    """
    nuevo_id = None
    #Asgnando id del empleado Logueado
    # vals['usuario_m2o_id'] = self.obtenerIdEmpleadoLogueado
    nuevo_id = super( merma, self ).create( cr, uid, vals, context = context )
    return nuevo_id


  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'merma'
  
  #Nombre de la tabla
  _table = 'merma'
  
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  # _rec_name = 'n_usuario'
  
  #Cláusula SQL "ORDER BY"
  _order = 'id DESC'

  #Columnas y/o campos Tree & Form
  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
    # 'clave' : fields.integer( 'Clave' ),
    'loc_final_dic':fields.selection(loc_desechos, 'Ubicación Final'),
    'tiendas_dic':fields.selection(TIENDA, 'Tienda'),
    'fecha_mov':fields.date("Fecha de Movimiento", required=True),
    'n_usuario': fields.char("Realizo", required=False),
    'state': fields.selection( (('draft', 'Borrador'), ('cancel','Cancelado'), ('confirm','Confirmado'), ('done', 'Realizado')), 'Estado', readonly=True, select=True),
    # 'state': fields.selection([
    #                           ('borrador', 'Borrador'),
    #                           ('confirmado', 'Confirmado'),
    #                           ('realizado', 'Realizado')
    #                         ]),
    # ========================================================  Relaciones [many2many](m2m) ======================================================== #
    'almacen_m2o_id': fields.many2one('stock.warehouse', 'Tienda', required=True),

    'location_id': fields.many2one('stock.location', 'Ubicacion de almacen', select=True),
    
    'selecc_merma_m2m': fields.many2many(
      #Nombre del modelo a relacionar
      'merma_seleccion',
      #Nombre de la tabla a generar
      'merma_m2m_selec_merma',
      #Primero se coloca el campo que contendra el ID del modelo local en la relacion 
      'merma_m2o_id',
      #Luego se coloca el campo que contendra el ID del modelo foraneo en la relacion
      'select_merma_m2o_id',
      #Etiqueta a mostrar al usuario
      'Selector Merma',
    ),
    
    'empleado_autor' : fields.function(
      _obtenerIdLogueado,
      type = 'text',
      method = True,
      string = 'Autor',
      change_default = True,
      store = False,
      readonly = True,
      required = False
    ),

  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    # 'ubicaciones_subquery' : _obtener_ubicaciones_subquery,

  }
  
  #Restricciones de BD (constraints)
  _sql_constraints = []
  
  
  #Restricciones desde codigo
  _constraints = []
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

merma()
