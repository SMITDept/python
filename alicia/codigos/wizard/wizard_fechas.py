# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Supermas-ARC                                                                                             #
#  @creacion : 2015-06-05 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #                                                                           #
#########################################################################################################################

#Importando las clases necesarias
import time
from datetime import datetime
from osv import fields, osv
import pooler
from openerp.tools.translate import _
import barcode

#Modelo
class wizard_fechas(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'obtiene los precios en determinada fecha'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def obtenerEan13( self, cr, uid, ids, context = None ):
    """
    Método para obtener codigos y mandar a imprimir las etiquetas
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @param : () 
    @return 
    """
    # date_init = self.pool.get( self._name ).browse( cr, uid, ids[0] ).fecha_inicial
    # date_end = self.pool.get( self._name ).browse( cr, uid, ids[0] ).fecha_final
    # #usar cuando este la logica total
    # # buscar = self._obtener_precio_productos( cr, uid, date_init, date_end )
    # buscar = True
    # if buscar == True :
    #     #imprimir reporte
    #    if context is None:
    #      context = {}
    #    data = {}
    #    data['ids'] = context.get('active_ids', [])
    #    data['model'] = context.get('active_model', 'ir.ui.menu')
    #    data['form'] = self.read(cr, uid, ids )[0]
    #    #Inicializando la variable datas, con el modelo
    #    datas = {
    #      'ids': [],
    #      'model': 'listado_codigo',
    #      'form': data,
    #    }
    #    
    #    #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml	
    #    return {
    #        'type': 'ir.actions.report.xml',
    #        'report_name': 'sm_etiquetas',
    #        'datas': datas,
    #        'nodestroy': True,
    #    }  
    # else :
    return { 'value' : {} }
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _obtener_precio_ean13( self, cr, uid, date_init, date_end ) :
    """
    Metodo que obtiene la informacion del producto apartir de las fechas
    * Argumentos OpenERP: [cr]
    @param lista:
    @return string
    """
    date_init = date_init.split('/')
    date_end = date_end.split('/')

    #   return True
    # else :
    return False

	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                                       Atributos Básicos del Modelo OpenERP                                      ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'wizard_fechas'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
    'fecha_inicial':fields.date("Fecha inicio", required=False),
    'fecha_final':fields.date("Fecha fin", required=False),

  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #
  
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

wizard_fechas()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
