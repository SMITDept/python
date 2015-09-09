# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : ARC                                                                                                                                #
#  @creacion    : 2015-08-26 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv

#Modulo :: Modelo de archivos adjuntos correspondiente a las facturas del mantenimiento
class adjuntos_maintenance( osv.osv ) :
  
  ####################################################################################################################################################
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def obtenerTipoDocumento(self, cr, uid, ids ) :
    """
    Retorna el Id del tipo de documento mediante la clave
    * Argumentos OpenERP: [cr, uid]
    @param obj: (Object) Es el objeto self del módulo que esté ejecutando esta función
    @param clave_tipo_documento : (int) Es la clave del tipo de documento
    @return int
    """
    #tipo documento factura
    clave_tipo_documento = 12
    tipo_documento_id = self.pool.get(
      'cat_tipo_documento'
    ).search(
      cr,
      uid,
      [ ( 'clave', '=', clave_tipo_documento ) ],
      context = None
    )
    if ( tipo_documento_id ) :
      try :
        return tipo_documento_id[0]
      except :
        return False
    
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                          OPENERP Metodos ORM                                                                 ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def create( self, cr, uid, vals, context = None ) : 
    """   
    Método "create" que se ejecuta justo antes (o al momento) de CREAR un nuevo registro en OpenERP.    
    * Argumentos OpenERP: [cr, uid, vals, context]    
    @param  
    @return bool    
    """
    
    return super( adjuntos_maintenance, self ).create( cr, uid, vals, context = context )
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def write( self, cr, uid, ids, vals, context = None ) : 
    """   
    Método "write" se ejecuta antes de modificar el registro..    
    * Argumentos OpenERP: [cr, uid, ids, vals, context]   
    @param  
    @return bool    
    """
    
    return super( adjuntos_maintenance, self ).write( cr, uid, ids, vals, context = context )

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'adjuntos_maintenance'
  
  #Nombre de la tabla
  _table = 'adjuntos_maintenance'
  
  _inherit = 'adjuntos'
  
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  _rec_name = 'id'
  
  #Cláusula SQL "ORDER BY"
  _order = 'id DESC'

  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #

    # ========================================================  Relaciones [many2one](m2o) ========================================================= #
    'adjuntos_maintenance_m2o_id' : fields.many2one(
      'maintenance_equip',
      'Maintenance'
    ),
    
    
  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'modelo_padre' : lambda self, cr, uid, context : 'maintenance_equip',
    'tipo_documento_m2o_id' : obtenerTipoDocumento,
  }
  
  #Restricciones de BD (constraints)
  _sql_constraints = []
  

  
  #Restricciones desde codigo
  _constraints = []


adjuntos_maintenance()
