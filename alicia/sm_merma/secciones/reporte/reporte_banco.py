# -*- coding: utf-8 -*-
######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : Alicia Romero                                                                                                                       #
#  @creación    : 2015-11-18                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

import time
from openerp.report import report_sxw
from openerp.osv import osv
from openerp import pooler

class reporte_banco(report_sxw.rml_parse):
  #variable que define al reporte
  _name = "reporte_banco"
  _description = "Reporte Banco de Alimentos"

  #######################################################################################################################
  #                                Metodos Privados (Independientes al API de OpenERP)                                  #
  ####################################################################################################################### 
  #----------------------------------------------------------------------------------------------------------------------
  def __init__( self, cr, uid, name, context = None ) :
    """
    Método "__init__" para instanciar objetos a partir de esta clase y pasar de formato rml a pdf
    * Argumentos OpenERP: [cr, uid, ids, name, context]	
    """
    if context is None:
      context = {}
    super( reporte_banco, self ).__init__( cr, uid, name, context = context )
    self.localcontext.update({
      'time': time,
      # 'get_datos': self.get_datos_etiquetas,
    })
    self.context = context
  #----------------------------------------------------------------------------------------------------------------------
  # def get_datos( self ):
  #   uid=self.uid
  #   self.cr.execute(
  #     """
  #     SELECT cod_barras AS ean13, 
  #     descripcion AS nombre, 
  #     precio AS precio,
  #     ruta_codigo AS ruta,
  #     fecha AS fecha,
  #     precio_str AS precio_s,
  #     fecha_str AS fecha_muestra,
  #     referencia AS ref
  #     FROM listado_codigo
  #     WHERE create_uid=%s
  #     """,(uid,)
  #   )
  #   datos = self.cr.dictfetchall()
  #   return datos
  #----------------------------------------------------------------------------------------------------------------------
  def clave_registro( self, data ) :
    """
    Método que obtiene el nombre del reporte con la clave
    @return (str)
    """        
    clave=''
    if data.get('form', False) and data['form'].get('clave_numer', False):
        clave=int(data['form'].get('clave_numer',False))
        nombre = 'Reporte :' + str(clave) 
    return nombre
  
  
  # ['n_usuario','fecha_mov','loc_final_dic','clave_numer','selecc_merma_m2m',]
  
#########################################################################################################################
#------------------------------------------------------------------------------------------------------------------------
#Nombre del reporte, nombre del modelo,ruta del rml, parser con el nombre de la clase y header el encabezado del reporte
#para emplear el template rml definido
report_sxw.report_sxw('report.reporte_banco',
                      'merma',
                      'addons/sm_merma/secciones/reporte/reporte_banco.rml',
                      parser = reporte_banco,
                      header=False
                      )

