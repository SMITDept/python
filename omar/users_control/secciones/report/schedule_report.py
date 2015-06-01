# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
import time
import locale

from report import report_sxw
import pooler

from lxml import etree
from osv import osv,fields
from tools.translate import _


#Modelo 
class totales_registros( report_sxw.rml_parse ) :

  _description = "Schedule Report"

  #----------------------------------------------------------------------------------------------------------------------
  def __init__( self, cr, uid, name, context = None ) :
    """
    Método "__init__" para instanciar objetos a partir de esta clase y pasar de formato rml a pdf
    * Argumentos OpenERP: [cr, uid, ids, name, context]	
    """
    if context is None:
      context = {}
    super(totales_registros, self).__init__( cr, uid, name, context = context )
    self.localcontext.update({
      'time': time,
      'locale': locale,
    })
    self.context = context
    
   #--------------------------------------------------------------------------------------------------------------------
  def get_fecha_formato_completo(self,fecha):
    """
    Método que convierte una fecha a formato largo
    @return (str)
    """        
    fecha_texto = ''
    fecha_str=''
    Mes = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anio, mes, dia = [int(d) for d in fecha.split('-')]
    fecha_texto = str(dia) + " de " + str(Mes[mes-1]) + " de " + str(anio)
    return fecha_texto   
    
  #######################################################################################################################
  #                                 Metodos Públicos (Independientes al API de OpenERP)                                 #
  #######################################################################################################################
  
  #----------------------------------------------------------------------------------------------------------------------
  def get_totales_registros( self, data ) :
    """
    Método que obtiene los Totales de registros
    @return (dict)
    """    
    self.query = ""
    
    if data.get('form', False) and data['form'].get('rango_fechas', False) :
      fecha_inicio = data['form'].get('fecha_inicio', False )
      fecha_fin = data['form'].get('fecha_fin', False )
      self.query = self.query + " AND fecha_egreso BETWEEN " + "'" + fecha_inicio + "'" + " AND " + "'" + fecha_fin + "'"
      
    if data.get('form', False) and data['form'].get('employee_number', False ) :
      employee = data['form'].get('employee_number', False)
      
    self.cr.execute(

    ag=self.cr.dictfetchall()
    
    return ag
  
#------------------------------------------------------------------------------------------------------------------------
#Nombre del reporte, nombre del modelo,ruta del rml, parser con el nombre de la clase y header el encabezado del reporte
#para emplear el template rml definido
report_sxw.report_sxw('report.totales_registros',
                      'schedule.report',
                      'supermas_addons/users_control/secciones/report/schedule_report.rml',
                      parser = totales_registros,
                      header = 'horizontal')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

