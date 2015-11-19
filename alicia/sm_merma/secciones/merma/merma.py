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
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def accion_confirmar(self, cr, uid, ids, context=None):
    """
    Confirma la lista de productos y escribe su fecha final
    @return: True
    """
    if context is None:
        context = {}
    id_merma = ids[0]
    self.write(cr, uid, ids, { 'state': 'confirm'}, context=context)

    # for inv in self.browse(cr, uid, ids, context=context):
    #     move_ids = []
    #     
    #     move_ids.append(self._inventory_line_hook(cr, uid, line, value))
    #self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
    # self.write(cr, uid, [inv.id], {'state': 'confirm', 'move_ids': [(6, 0, move_ids)]})
    # self.pool.get('stock.move').action_confirm(cr, uid, move_ids, context=context)
    return True
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def accion_realizar(self, cr, uid, ids, context=None):
    """
    Finaliza el inventario
    @return: True
    """
    if context is None:
        context = {}
    id_merma = ids[0]
    self.write(cr, uid, ids, { 'state': 'done'}, context=context)

    return True
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def accion_cancelar_borrador(self, cr, uid, ids, context=None):
    """ Cancela el stock de movimiento y el estado de modificación de listado para redactar.
    @return: True
    """
    if context is None:
      context = {}
    # for inv in self.browse(cr, uid, ids, context=context):
    #     self.pool.get('stock.move').action_cancel(cr, uid, [x.id for x in inv.move_ids], context=context)
    self.write(cr, uid, ids, {'state':'draft'}, context=context)
    return True
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def accion_cancelar_movimiento(self, cr, uid, ids, context=None):
        """ Cancela el stock move y el listado
        @return: True
        """
        # move_obj = self.pool.get('stock.move')
        # account_move_obj = self.pool.get('account.move')
        # for inv in self.browse(cr, uid, ids, context=context):
        #     move_obj.action_cancel(cr, uid, [x.id for x in inv.move_ids], context=context)
        #     for move in inv.move_ids:
        #          account_move_ids = account_move_obj.search(cr, uid, [('name', '=', move.name)])
        #          if account_move_ids:
        #              account_move_data_l = account_move_obj.read(cr, uid, account_move_ids, ['state'], context=context)
        #              for account_move in account_move_data_l:
        #                  if account_move['state'] == 'posted':
        #                      raise osv.except_osv(_('User Error!'),
        #                                           _('In order to cancel this inventory, you must first unpost related journal entries.'))
        #                  account_move_obj.unlink(cr, uid, [account_move['id']], context=context)
        #     self.write(cr, uid, [inv.id], {'state': 'cancel'}, context=context)
        self.write(cr, uid, ids, {'state':'cancel'}, context=context)
        return True
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

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
    destino = obj_merma.loc_final_dic
    id_merma = ids[0] 
    autor_uid = uid
    if obj_merma :
      cr.execute(
      """
      SELECT
      id
      FROM merma_seleccion
      WHERE almacen_m2o_id=%s
      AND
      TO_CHAR(create_date,'YYYY-MM-DD')= %s
      AND
      nombre_destino like %s
      """,(tienda_alm, fecha_mov, destino,) )
      resultado = cr.fetchall()
      if resultado != None and type( resultado ) in ( list, dict) :
        self.write(cr, uid, ids, {
                'consultado': True,   
        }, context=context)
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
  #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def _obtenerIdLogueado( self, cr, uid ) :
    """
    Metodo para obtener el nombre del usuario que realizo el control de merma
    * Argumentos OpenERP: [cr, uid]
    @return string
    """
    result = {}
    obj_user = self.pool.get( 'res.users' ).browse( cr, uid, uid )
    nombre_empleado=obj_user.partner_id.name
    #Retornando
    return nombre_empleado  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def obtenerNumero(self, cr, uid, almacen, destino ) :
    """
    Metodo que obtiene el numero siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """
    #Consultando cuál sería el nuevo numero
    cr.execute( """
               SELECT ( MAX( c_numero ) + 1 ) AS next_number
               FROM merma
               WHERE almacen_m2o_id = %s and loc_final_dic = %s
               """ ,(almacen, destino,) )
    registro_consultado = cr.fetchone()
    numero = (1) if (registro_consultado is None) else ( 1 if ( registro_consultado[0] is None ) else ( int( registro_consultado[0] ) ))	 
    #Retornando el nuevo folio
    return numero
  #----------------------------------------------------------------------------------------------------------------------
  def obtenerClave(self, cr, uid, almacen, destino, numero ) :
    """
    Metodo que obtiene la clave siguiente
    * Para OpenERP [field.function]
    * Argumentos OpenERP: [cr, tabla,nombre_campo]
    :return dict
    """
    #Se crea clave
    fecha_realizo = time.strftime("%d%m%y")
    obj_almacen = self.pool.get('stock.warehouse')
    tienda_nombre=obj_almacen.browse(cr, uid, almacen).name
    nombre_sep = tienda_nombre.split()
    n_tienda = nombre_sep[2] 
    clave = 'SM'+ n_tienda + destino[:3].upper()+str(numero)+'/'+fecha_realizo
    #Retornando el nuevo folio
    return clave
  #----------------------------------------------------------------------------------------------------------------------
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
    almacen=vals['almacen_m2o_id']
    destino=vals['loc_final_dic']
    vals['c_numero'] = self.obtenerNumero( cr, uid, almacen, destino )
    numero=vals['c_numero']
    vals['clave_numer'] = self.obtenerClave( cr, uid, almacen, destino, numero )
    vals['n_usuario'] = self._obtenerIdLogueado( cr, uid)
  
    nuevo_id = super( merma, self ).create( cr, uid, vals, context = context )
    return nuevo_id
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def write( self, cr, uid, ids, vals, context = None) :
    """
    Método "write" se ejecuta antes de modificar el registro..
    * Argumentos OpenERP: [cr, uid, ids, vals, context]
    @return bool
    """
    datos=self.pool.get( self._name ).browse( cr, uid, ids[0] )
    almacen=datos.almacen_m2o_id.id
    destino=datos.loc_final_dic
    numero=self.obtenerNumero( cr, uid, almacen, destino )
    clave = self.obtenerClave( cr, uid, almacen, destino, numero )
    vals.update({'clave_numer': clave})
    proceso = super( merma, self ).write( cr, uid, ids, vals, context = context )
    #Retornando proceso,
    return proceso
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  
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
  _rec_name = 'clave_numer'
  
  #Cláusula SQL "ORDER BY"
  _order = 'id DESC'

  #Columnas y/o campos Tree & Form
  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
    'c_numero' : fields.integer( 'Clave Numero' ),
    'consultado':fields.boolean('Consultado'),
    'clave_numer' : fields.char( 'Clave' ),
    'loc_final_dic':fields.selection(loc_desechos, 'Ubicación Final', required=True),
    # 'tiendas_dic':fields.selection(TIENDA, 'Tienda'),
    'fecha_mov':fields.date("Fecha de Movimiento", required=True),
    'n_usuario': fields.char("Realizo", required=False),
    'state': fields.selection(  ( ('draft', 'Borrador'),
                                  ('cancel','Cancelado'),
                                  ('confirm','Confirmado'),
                                  ('done', 'Realizado')
                                ),
                              'Estado', readonly=True,
                              select=True
                              ),
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
    
    # 'empleado_autor' : fields.function(
    #   _obtenerIdLogueado,
    #   type = 'text',
    #   method = True,
    #   string = 'Autor',
    #   change_default = True,
    #   store = False,
    #   readonly = True,
    #   required = False
    # ),

  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'state': 'draft',
    # 'ubicaciones_subquery' : _obtener_ubicaciones_subquery,

  }
  
  #Restricciones de BD (constraints)
  _sql_constraints = []
  
  
  #Restricciones desde codigo
  _constraints = []


	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                 Definicion de Funcion para "Imprimir Reporte"                                                   ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  def imprimir_reporte_banco(self, cr, uid, ids ,context={}):
    """
    Metodo para imprimir el reporte en formato PDF
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @return dict 
    """
    
    #imprimir reporte
    if context is None:
      context = {}
    data = {}
    data['ids'] = context.get('active_ids', [])
    data['model'] = context.get('active_model', 'ir.ui.menu')
    data['form'] = self.read(cr, uid, ids,['n_usuario','fecha_mov','loc_final_dic','clave_numer','selecc_merma_m2m',], )[0]
    #Inicializando la variable datas, con el modelo
    datas = {
      'ids': [],
      'model': 'merma',
      'form': data,
    }

    
    #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml	
    return {
        'type': 'ir.actions.report.xml',
        'report_name': 'reporte_banco',
        'datas': datas,
        'nodestroy': True,
    }  
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

merma()
