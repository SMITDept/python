# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : EHO                                                                                                                                #
#  @creacion    : 2015-02-17 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo, 150 caracteres                                                                                                             #
#  @descripcion : Creacion de la clase correspondiente a los Archivos adjuntos                                                                       #
######################################################################################################################################################

#OpenERP imports
import hashlib
import itertools
import logging
import os
import re
import base64
from openerp import tools
from openerp.osv import fields,osv
from openerp import SUPERUSER_ID

from datetime import datetime, date, timedelta
from pytz import timezone
import time

#Importando funcionalidades misceláneas globales a los modelos de OpenERP en GESTIO (FuncionGlobal, FuncionModelo)
# from gestio.static.general.miscelanea.Miscelanea import *

_logger = logging.getLogger(__name__)

#Modulo :: archivos_adjuntos
class adjuntos( osv.osv ) :
  """
  Los archivos adjuntos se utilizan para vincular archivos binarios a cualquier documento OpenERP. 

     Almacenamiento: Colocación externa 
     ----------------------------------
    
     El campo "datas" de tipo function (_data_get, data_set) implementa los metodos 
     _file_read, _file_write y _file_delete que se pueden reemplazar para 
     implementar otros motores de almacenamiento, el uso de estos métodos ayuda a comprobar
     si existe otra ubicación (ejemplo: hdfs :/ / hadoppserver) 
    
     La implementación por defecto es el file:dirname ubicación que almacena archivos 
     en el sistema de archivos utilizando el nombre local de la base de su hash sha1 
  """
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  #
  _location = 'file:///adjuntos'
    
  ####################################################################################################################################################
  #                                                                                                                                                  #
  #                  Metodos Privados Relacionados al API de OpenERP o a sus procesos (botones, etc). NO FUNCIONALIDAD DE REPORTES                   #
  #                                                                                                                                                  #
  ####################################################################################################################################################
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  @staticmethod
  def obtenerFechaActualMexico() :
    """
    Devuelve la fecha actual en Mexico
    @return Devuelve (date) la fecha actual en Mexico
    """
    return datetime.now( timezone( 'America/Mexico_City' ) ).date()
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _full_path( self, cr, uid, location, path ) :
    """
    Método que se ejecuta cuando se requiere LEER del archivo
    * Argumentos OpenERP: [cr, uid]
    @param location: (string) corresponde al valor del parametro de alojamiento del sistema
    @param path: (string) corresponde a la ruta de ubicacion del archivo dentro de la carpeta de alojamiento
    @return string
    """
    #Se verifica si se tiene el control del directorio de almacenamiento
    assert location.startswith( 'file:' ), "Unhandled filestore location %s" % location
    location = location[5:]
    #Se ajustan los paths (location, path)
    location = re.sub( '[.]', '', location )
    location = location.strip( '/\\' )
    path = re.sub( '[.]', '', path )
    path = path.strip( '/\\' )
    #Se retorna la concatenacion de paths
    return os.path.join( tools.config['root_path'], location, cr.dbname, path )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _file_read( self, cr, uid, location, fname, bin_size = False ) :
    """
    Método que se ejecuta cuando se requiere LEER del archivo
    * Argumentos OpenERP: [cr, uid]
    @param location: (string) corresponde al valor del parametro de alojamiento del sistema
    @param fname: (string) corresponde a la ruta de ubicacion y nombre del archivo dentro de la carpata de alojamiento 
    @param bin_size: (int) corresponde al tamaño del archivo
    @return attachment
    """
    #Se crea el path de ubicacion
    full_path = self._full_path( cr, uid, location, fname )
    attach = ''
    try :
      #Se obtiene el archivo ya sea por su tamaño o ubicacion
      if bin_size :
        attach = os.path.getsize( full_path )
      else :
        attach = open( full_path,'rb' ).read().encode( 'base64' )
    except IOError :
        _logger.error( "_read_file reading %s", full_path )
    return attach
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _file_write( self, cr, uid, location, modelo_padre, tipo_documento, value ) :
    """
    Método que se ejecuta cuando se requiere la CREACION de la estructura de carpetas y la ESCRITURA del archivo
    * Argumentos OpenERP: [cr, uid]
    @param location: (string) corresponde al valor del parametro de alojamiento del sistema
    @param modelo_padre: (string) corresponde al nombre del modelo padre del proceso
    @param tipo_documento: (int) corresponde al id del tipo de documento
    @param value: (binary) corresponde al archivo que se desea almacenar 
    @return string
    """
    #Obtenemos el valor binario
    bin_value = value.decode( 'base64' )
    #Se obtiene el nombre para el archivo utilizando sha1
    fname = hashlib.sha1( bin_value ).hexdigest()
    #Se crea el path en donde se guardara el archivo
    fname = (
      modelo_padre +
      '/' + self._name +
      '/' + str( tipo_documento )  +
      '/' + str( self.obtenerFechaActualMexico().year ) +
      '/' + str( self.obtenerFechaActualMexico().month ) +
      '/' + fname
    )
    #Se concatena la estructura con el directorio de alojamiento
    full_path = self._full_path( cr, uid, location, fname )
    try :
      #Verificamos si existe el directorio
      dirname = os.path.dirname( full_path )
      #Si no existe se crea el directorio
      if not os.path.isdir( dirname ) :
        os.makedirs(dirname)
      #Se guarda el archivo en el directorio
      open( full_path, 'wb' ).write( bin_value )
    except IOError :
      _logger.error( "_file_write writing %s", full_path )
    #Se retorna el path en donde se alojo el archivo
    return fname
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _file_delete( self, cr, uid, location, fname ) :
    """
    Método que se ejecuta cuando se requiere la ELIMINACION del archivo
    * Argumentos OpenERP: [cr, uid]
    @param location: (string) corresponde al valor del parametro de alojamiento del sistema
    @param fname: (string) corresponde a la ruta de ubicacion y nombre del archivo dentro de la carpata de alojamiento 
    @return boolean
    """
    #Se obtiene el numero de registros ligados al archivo
    count = self.search( cr, 1, [ ( 'store_fname', '=', fname ) ], count = True )
    #Se verifica que el archivo este ligado a un solo registro
    if count <= 1 :
      #Obtenemos el path de ubicacion
      full_path = self._full_path( cr, uid, location, fname )
      try :
        #Se realiza la eliminacion del archivo
        os.unlink( full_path )
      except OSError :
        _logger.error( "_file_delete could not unlink %s", full_path )
      except IOError :
      #Mensaje inofensivo, se visualiza en el log del servidor cuando esta en funcionamiento
        _logger.error( "_file_delete could not unlink %s", full_path )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _data_get( self, cr, uid, ids, name, arg, context = None ) :
    """
    Método que se ejecuta cuando se requiere la RECUPERACION O DESCARGA del archivo
    * Argumentos OpenERP: [cr, uid, ids, name, arg, context]
    @return boolean
    """
    if context is None :
      context = {}
    result = {}
    bin_size = context.get( 'bin_size' )
    #Se realiza la busqueda del archivo
    for attach in self.browse( cr, uid, ids, context = context ) :
      #Se realiza la lectura del archivo si la variable del parametro de alojacion no es nula y se tiene el path de ubicacion
      if self._location and attach.store_fname :
        result[attach.id] = self._file_read( cr, uid, self._location, attach.store_fname, bin_size )
      #Si no se busca en la BDD
      else :
        result[attach.id] = attach.db_datas
    return result
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _data_set( self, cr, uid, id, name, value, arg, context = None ) :
    """
    Método que se ejecuta para realizar el GUARDADO el archivo
    * Argumentos OpenERP: [cr, uid, id, name, arg, context]
    @param value: (binary) corresponde al archivo que se desea almacenar 
    @return boolean
    """
    #No se manejan valores nulos, por lo cual si el valor es nulo se retorna un True debido a que no hay nada por asignar
    if not value :
      return True
    if context is None :
      context = {}
    #Se obtiene el tamaño del archivo
    file_size = len( value.decode( 'base64' ) )
    #Verificamos si la variable de alojacion contiene el valor correspondiente al parametro del sistema
    if self._location :
      attach = self.browse( cr, uid, id, context = context )
      #Si es cambio de archivo, se elimina el anterior
      if attach.store_fname :
        self._file_delete( cr, uid, self._location, attach.store_fname )
      #Se necesitan el modelo padre y el tipo de documento para generar la estructura de carpetas
      if attach.modelo_padre and attach.tipo_documento_m2o_id :
        #Se obtiene la ruta en donde se alojara el archivo
        fname = self._file_write( cr, uid, self._location, attach.modelo_padre, attach.tipo_documento_m2o_id.clave, value )
        # SUPERUSER_ID as probably don't have write access, trigger during create
        super(
          adjuntos,
          self
        ).write(
          cr,
          SUPERUSER_ID,
          [id],
          {
            'store_fname' : fname,
            'file_size' : file_size,
            'annio' : str( date.today().year ),
            'mes' : str( date.today().month ),
          },
          context = context
        )
      else:
        raise osv.except_osv( ( 'Error' ), ( 'Tipo de documento y modelo padre no asignados, consulte al administrador.' ) )
    #en caso de no contar con el parametro almacenado en la variable "location" se guardan los archivos en la BDD
    else :
      super(
        adjuntos,
        self
      ).write(
        cr,
        SUPERUSER_ID,
        [id],
        {
          'db_datas' : value,
          'file_size' : file_size,
          'annio' : str( date.today().year ),
          'mes' : str( date.today().month ),
        },
        context = context
      )
    return True
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                       Definicion de OpenERP ORM Methods                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _auto_init( self, cr, context = None ) :
    """
    Verifica si existe un indice para el modelo de archivos adjuntos,
    en caso de no existir lo crea.
    """
    super( adjuntos, self )._auto_init( cr, context )
    cr.execute( 'SELECT indexname FROM pg_indexes WHERE indexname = %s', ( 'adjuntos_res_idx', ) )
    if not cr.fetchone() :
      cr.execute( 'CREATE INDEX adjuntos_res_idx ON adjuntos ( res_model, res_id )' )
      cr.commit()
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def check( self, cr, uid, ids, mode, context = None, values = None ) :
    """
    Restringe el acceso a un ir.attachment, según el modelo contemplado
    En el módulo de "documento", se reemplaza para relajarla, ya que las
    más complejas se aplican en este.
    """
    res_ids = {}
    if ids :
      if isinstance( ids, ( int, long ) ) :
        ids = [ids]
      cr.execute( 'SELECT DISTINCT res_model, res_id FROM adjuntos WHERE id = ANY (%s)', ( ids, ) )
      for rmod, rid in cr.fetchall() :
        if not ( rmod and rid ) :
          continue
        res_ids.setdefault(rmod,set()).add(rid)
    if values:
      if values.get( 'res_model' ) and values.get( 'res_id') :
        res_ids.setdefault(values['res_model'],set()).add(values['res_id'])

    ima = self.pool.get( 'ir.model.access' )
    for model, mids in res_ids.items() :
      # ignore attachments that are not attached to a resource anymore when checking access rights
      # (resource was deleted but attachment was not)
      mids = self.pool.get( model ).exists( cr, uid, mids )
      ima.check( cr, uid, model, mode )
      self.pool.get( model ).check_access_rule( cr, uid, mids, mode, context = context )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _search( self, cr, uid, args, offset = 0, limit = None, order = None, context = None, count = False, access_rights_uid = None ) :
    """
    Metodo que ejecuta una BUSQUEDA de registros en este modelo y devuelve una lista de ids encontrados
    * Argumentos OpenERP [cr, uid, args, offset, limit, order, context, count, access_rights_uid]
    :return list
    """
    ids = super( adjuntos, self )._search( cr, uid, args, offset = offset,
                                                limit = limit, order = order,
                                                context = context, count = False,
                                                access_rights_uid = access_rights_uid )
    if not ids :
      if count :
        return 0
      return []
      
    # Work with a set, as list.remove() is prohibitive for large lists of documents
    # (takes 20+ seconds on a db with 100k docs during search_count()!)
    orig_ids = ids
    ids = set( ids )

    # For attachments, the permissions of the document they are attached to
    # apply, so we must remove attachments for which the user cannot access
    # the linked document.
    # Use pure SQL rather than read() as it is about 50% faster for large dbs (100k+ docs),
    # and the permissions are checked in super() and below anyway.
    cr.execute( """SELECT id, res_model, res_id FROM adjuntos WHERE id = ANY(%s)""", ( list( ids ), ) )
    targets = cr.dictfetchall()
    model_attachments = {}
    for target_dict in targets :
      if not ( target_dict[ 'res_id' ] and target_dict[ 'res_model' ] ) :
        continue
      # model_attachments = { 'model': { 'res_id': [id1,id2] } }
      model_attachments.setdefault(target_dict['res_model'],{}).setdefault(target_dict['res_id'],set()).add(target_dict['id'])

    # To avoid multiple queries for each attachment found, checks are
    # performed in batch as much as possible.
    ima = self.pool.get( 'ir.model.access' )
    for model, targets in model_attachments.iteritems() :
      if not self.pool.get( model ) :
        continue
      if not ima.check( cr, uid, model, 'read', False ) :
        # remove all corresponding attachment ids
        for attach_id in itertools.chain( *targets.values() ) :
          ids.remove( attach_id )
        continue # skip ir.rule processing, these ones are out already

      # filter ids according to what access rules permit
      target_ids = targets.keys()
      allowed_ids = self.pool.get( model).search( cr, uid, [( 'id', 'in', target_ids )], context = context )
      disallowed_ids = set( target_ids ).difference( allowed_ids )
      for res_id in disallowed_ids :
        for attach_id in targets[res_id] :
          ids.remove( attach_id )

    # sort result according to the original sort ordering
    result = [id for id in orig_ids if id in ids]
    return len( result ) if count else list( result )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def read( self, cr, uid, ids, fields_to_read = None, context = None, load = '_classic_read' ) :
    """
    Método "read" que se ejecuta al momento de LEER un registro en OpenERP.
    * Argumentos OpenERP: [cr, uid, ids, fields_to_read, context, load]
    :return bool
    """
    if isinstance( ids, ( int, long ) ) :
      ids = [ids]
    self.check( cr, uid, ids, 'read', context = context )
    return super( adjuntos, self ).read( cr, uid, ids, fields_to_read, context, load )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def write( self, cr, uid, ids, vals, context = None ) :
    """
    Método "write" que se ejecuta al momento de MODIFICAR un registro en OpenERP.
    * Argumentos OpenERP: [cr, uid, ids, vals, context]
    :return bool
    """
    if isinstance( ids, ( int, long ) ) :
      ids = [ids]
    self.check( cr, uid, ids, 'write', context = context, values = vals )
    if 'file_size' in vals :
      del vals['file_size']
    return super( adjuntos, self ).write( cr, uid, ids, vals, context )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def copy( self, cr, uid, id, default = None, context = None ) :
    """
    Método "copy" que se ejecuta al momento de DUPLICAR un registro en OpenERP.
    * Argumentos OpenERP: [cr, uid, id, default, context]
    :return bool
    """
    self.check( cr, uid, [id], 'write', context = context )
    return super( adjuntos, self ).copy( cr, uid, id, default, context )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def unlink( self, cr, uid, ids, context = None ) :
    """
    Método "unlink" que se ejecuta al momento de ELIMINAR un registro en OpenERP.
    * Argumentos OpenERP: [cr, uid, ids, context]
    :return bool
    """
    if isinstance( ids, ( int, long ) ) :
      ids = [ids]
    self.check( cr, uid, ids, 'unlink', context = context )
    if self._location :
      for attach in self.browse( cr, uid, ids, context = context ) :
        if attach.store_fname :
          self._file_delete( cr, uid, self._location, attach.store_fname )
    return super( adjuntos, self ).unlink( cr, uid, ids, context )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def create( self, cr, uid, values, context = None ) :
    """
    Método "create" que se ejecuta al momento de CREAR un nuevo registro en OpenERP.
    * Argumentos OpenERP: [cr, uid, values, context]
    :return int
    """ 
    self.check( cr, uid, [], mode = 'write', context = context, values = values )
    if 'file_size' in values :
      del values['file_size']
    return super( adjuntos, self ).create( cr, uid, values, context )
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def action_get( self, cr, uid, context = None ) :
    """
    Método "action_get" que se ejecuta al momento de INVOCAR una vista o menu en OpenERP.
    * Argumentos OpenERP: [cr, uid, context]
    :return bool
    """
    return self.pool.get( 'ir.actions.act_window' ).for_xml_id( cr, uid, 'hardware_inventory', 'action_adjuntos', context = context )
    
    
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                       Atributos Basicos del Modelo OpenERP                                                   ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'adjuntos'
  
  #Nombre de la tabla a crear en la BD
  _table = 'adjuntos'
  
  #Valor estandar que aparece en el campo de las relaciones m2o, o2m y m2m; al momento de seleccionar algun registro de este modelo
  #Puede modificarse con la funcion [name_get] definida en el ORM Methods de OpenERP, sin embargo este valor siempre debe registrase correctamente
  _rec_name = 'datas_fname'
  
  #Clausula ORDER BY del listado. 
  _order = 'id'
  

  _columns = {
  
    # ========================================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================================= #
    
    'datas_fname' : fields.char( 'File Name', size = 256 ),
    # al: We keep shitty field names for backward compatibility with document
    'datas'       : fields.function( _data_get, fnct_inv = _data_set, string = 'Archivo', type = "binary", nodrop = True, required = True ),
    'store_fname' : fields.char( 'Stored Filename', size = 256 ),
    'db_datas'    : fields.binary( 'Database Data' ),
    'file_size'   : fields.integer( 'File Size' ),
    'res_model'   : fields.char( 'Resource Model', size = 64, readonly = True, help = "The database object this attachment will be attached to" ),
    'res_id'      : fields.integer( 'Resource ID', readonly = True, help = "The record id this is attached to" ),
    'create_date' : fields.datetime( 'Date Created', readonly = True ),
    'create_uid'  :  fields.many2one( 'res.users', 'Owner', readonly = True ),
    'modelo_padre' : fields.char( 'Modelo_padre', size = 64 ),
    'annio' : fields.integer( 'Año' ),
    'mes': fields.integer( 'Mes' ),

    
    # ======================================================  Relaciones OpenERP [many2one](m2o) =================================================== #
    'tipo_documento_m2o_id': fields.many2one(
      'cat_tipo_documento',
      'Tipo de documento',
      required = True
    ),
    
  }
  
  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
    'modelo_padre' : lambda self, cr, uid, context : 'adjuntos',
  }
  
  #Reestricciones desde BD
  _sql_constraints = []
  
  
  #Reestricciones desde código
  _constraints = []
  

adjuntos()
