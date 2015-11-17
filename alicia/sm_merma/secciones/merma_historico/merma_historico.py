# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-Alicia Romero                                                                                                                       #
#  @creación    : 2015-10-15                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP Imports
from osv import fields, osv
from datetime import datetime, date
import time

#Modulo ::
class merma_historico(osv.osv):
  #--------------------------------------------------------Variables Privadas y Publicas--------------------------------------------------------------
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###


  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'merma_historico'
  #Nombre de la tabla
  _table = 'merma_historico'
 
  _columns = {
    'fecha_captura':fields.date("Fecha de captura", required=False),
    'realizado_por' : fields.char("Realizo", required=False),
    'cod_ean' : fields.char("Codigo", required=False),
    'cod_esc' : fields.char("Codigo escaneado", required=False),
    'producto' : fields.char("Producto", required=False),
    'cantidad_capturada':fields.float('Cantidad', required=False),
    'cantidad capturada':fields.float('Cantidad', required=False),
    'precio':fields.float('Precio', required=False),
    'unidad_med' : fields.char("Unidad", required=False),
    'clase_1':fields.char("Clase", required=False),
    'cant_mermada':fields.float('Cantidad mermada', required=False),
    'fecha_merma':fields.date("Fecha de merma", required=False),
    'clase_2':fields.char("Clase 2", required=False),
    'finalizado_por' : fields.char("Realizo", required=False),
    'referencia':fields.char("Referencia interna", required=False),
    'tienda' : fields.char("Tienda", required=False),
    'localizacion' : fields.char("Localizacion", required=False),
    'destino' : fields.char("Destino", required=False),
    
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
  }

#se cierra la clase
merma_historico() 


