# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                      #
#  @creacion    : 2015-08-22 (aaaa/mm/dd)                                                                                                            #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP imports
from osv import fields, osv

# :::::::::::::::::::::::::::::::::::::::::::::::::::: REFERENCIAS A SOBREESCRIBIR [COMIENZAN] ::::::::::::::::::::::::::::::::::::::::::::::::::::: # 
# :::::::::::::::::::::::::::::::::::::::::::::::::::: REFERENCIAS A SOBREESCRIBIR [TERMINAN] :::::::::::::::::::::::::::::::::::::::::::::::::::::: #

#Modulo :: 
class cat_tipo_documento( osv.osv ) :

  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'cat_tipo_documento'
  
  #Nombre de la tabla
  _table = 'cat_tipo_documento'
  
  #Nombre de la descripcion al usuario en las relaciones m2o hacia este módulo
  _rec_name = 'descripcion'
  
  #Cláusula SQL "ORDER BY"
  _order = 'descripcion DESC'

  #Columnas y/o campos Tree & Form
  _columns = {
    
    # =========================================  OpenERP Campos Basicos (integer, char, text, float, etc...)  ====================================== #
    'clave' : fields.integer( 'Clave' ),
    'descripcion' : fields.char( 'Tipo de documento', size = 255, required = True ),
    'activo' : fields.boolean( 'Activo' ),
    
    # ========================================================  Relaciones [many2many](m2m) ======================================================== #
    'openerp_model_m2m': fields.many2many(
      #Nombre del modelo a relacionar
      'ir.model',
      #Nombre de la tabla a generar
      'cat_tipo_documento_m2m_ir_model',
      #Primero se coloca el campo que contendra el ID del modelo local en la relacion 
      'tipo_documento_m2o_id',
      #Luego se coloca el campo que contendra el ID del modelo foraneo en la relacion
      'openerp_model_m2o_id',
      #Etiqueta a mostrar al usuario
      'Modelos',
    ),

  }
  
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'activo' : True,
  }
  
  #Restricciones de BD (constraints)
  _sql_constraints = []
  
  
  #Restricciones desde codigo
  _constraints = []
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

cat_tipo_documento()
