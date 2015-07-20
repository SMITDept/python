# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Alicia Romero                                                                                            #
#  @creacion : 2015-06-24 (aaaa/mm/dd)                                                                                  #
#  @linea    : Máximo, 121 caracteres                                                                                   #
#  @descripcion: auxiliar de contabilidad                                                                               #
#########################################################################################################################

#Importando las clases necesarias
import time
from datetime import date
from osv import fields, osv
from openerp.tools.translate import _
#para crear la hoja de calculo
import xlwt

#Modelo
class auxiliar_contable(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'auxiliar de contabilidad'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  def _obtener_periodo( self, cr, uid, ids, context = None ):
    """
    Metodo para obtener por defecto el id del periodo anterior dependiendo de la fecha actual
    * Argumentos OpenERP: [cr, uid, ids, context]
    @return int
    """   
    
    self.query = ""
    per_id=''
    current_date=date.today()
    # current_date=date(2014,03,01)
    carry, new_month=divmod(current_date.month-1+1, 12)
    new_month+=-1
    current_date=current_date.replace(year=current_date.year+carry, month=new_month, day=1)
    self.query = str(current_date)
    cr.execute(
      """
      SELECT id
      FROM account_period
      WHERE date_start = '"""+ self.query +"""'
      """)
    registro = cr.fetchone()
    if (len( registro ) > 0 ):
      #Obteniendo el ID del periodo
      per_id = registro[0]
    else:
      cr.execute(
      """
      SELECT id
      FROM account_period
      ORDER BY id DESC
      """)
      registro = cr.fetchone()
      per_id = registro[0]
    return per_id
  #---------------------------------------------------------------------------------------------------------------------------------------------------     
  def obtenerXlwt( self, cr, uid, ids, context = None ):
    """
    Metodo para imprimir el reporte en formato .xlsx hojas de cálculo
    * Argumentos OpenERP: [cr, uid, ids, context]
    @return dict 
    """
    #style
    style_title = xlwt.easyxf('pattern: pattern solid, fore_colour red; '
                              'font: colour white, bold True; align: vert centre;')
    style0 = xlwt.easyxf('font: name Arial, color-index black', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='DD-MM-YY')
    styleNo = xlwt.easyxf('font: name Arial, color-index red', num_format_str='#,##0.00')
    #objeto que crea el libro de trabajo con el constructor Workbook()
    workbook = xlwt.Workbook()
    #El objeto de libro llama al método add_sheet() para agregar una nueva hoja de cálculo
    worksheet = workbook.add_sheet('Auxiliar por cuenta')
    #Se crean los nombres de las columnas
    worksheet.write(0,0,'CREACION', style_title)
    worksheet.write(0,1,'FECHA', style_title)
    worksheet.write(0,2,'DEBITO', style_title)
    worksheet.write(0,3,'CREDITO', style_title)
    worksheet.write(0,4,'NOMBRE', style_title)
    worksheet.write(0,5,'DESCRIPCION', style_title)
    worksheet.col(0).width = 30 * 256
    worksheet.col(5).width = 50 * 256
    #objeto del modelo
    obj=self.pool.get( self._name )
    datos=obj.browse( cr, uid, ids[0] )
    self.query = ""
    cuenta=''
    periodo=''
    bandera=False
    path='/tmp/Auxiliar.xls'
    if datos.account_id != 0:
      cuenta=str(datos.account_id.id)
      self.query = "AND aml.account_id = " + cuenta
      
      if datos.por_periodo == True :
        periodo=str(datos.period_id.id)
        self.query = self.query + " AND aml.period_id = " + periodo
        bandera=True
      else:  
        if datos.rango_fechas == True :
          inicio = datos.fecha_inicio
          fin = datos.fecha_fin
          self.query = self.query + " AND aml.create_date BETWEEN " + "'" + inicio + " 06:00:01"+ "'" + " AND " + "'" + fin + " 05:59:59"+ "'"
          bandera=True
        
      if bandera == True: 
        cr.execute(
            """
              SELECT aml.create_date AS create_d,
              aml.date AS date,
              aml.debit AS debit,
              aml.credit AS credit,
              aml.name AS name,
              acc.name AS nombre
              FROM account_move_line aml
              INNER JOIN account_account acc
              ON aml.account_id = acc.id
              WHERE  aml.state = 'valid'
              """+ self.query +"""
              AND aml.name LIKE 'POS%'
              ORDER BY aml.create_date
            """)
        aux = cr.fetchall()
        if type( aux ) in ( list, dict) :
          if ( len( aux ) > 0 ) :
            row = 1
            col = 0
            titul=''
            for create_d, date, debit, credit, name, nombre in (aux):
              worksheet.write(row, col, create_d, style0)
              worksheet.write(row, col + 1, date, style1)
              worksheet.write(row, col + 2, debit, style0)
              worksheet.write(row, col + 3, credit, style0)
              worksheet.write(row, col + 4, name, style0)
              worksheet.write(row, col + 5, nombre.title(), style0)
              row += 1
              titul=nombre
              
            titul=titul.split()
            path='/tmp/Auxiliar_'+str(titul[0]).capitalize()+'.xls'  
          else:
              worksheet.write(1, 0, '* No se encontraron datos en la busqueda *', styleNo)
      else:
        raise osv.except_osv(_( 'Aviso' ),_( 'Por favor de seleccionar una de las opciones de búsqueda: Por Periodo ó Por Rango de Fechas' ) )
    print path  
    # guarda el archivo en la ruta especificada      
    return workbook.save(path)
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_periodo( self, cr, uid, ids, por_periodo) :
    """
    Evento OnChange del campo "por_periodo" con etiqueta "Por periodo" 
    que regresa False al campo rango_fechas
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids, por_periodo, rango_fechas ]
    @param key: (string) por_periodo
    @return dict
    """
    if por_periodo == True:
      return {
        'value' : {
          'rango_fechas' : False,
        }
      }
    return { 'value' : {} }
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def onchange_rango( self, cr, uid, ids, rango_fechas) :
    """
    Evento OnChange del campo 'rango_fechas' con etiqueta 'Por Rango de fechas'
    que regresa False al campo por_periodo
    * Para OpenERP [onchange]
    * Argumentos OpenERP: [cr, uid, ids, por_periodo, rango_fechas ]
    @param key: (string) rango_fechas
    @return dict
    """
    if rango_fechas == True:
      return {
        'value' : {
          'por_periodo' : False ,
        }
      }
    return { 'value' : {} }
  ### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                 ###
  ###                                       Atributos Básicos del Modelo OpenERP                                      ###
  ###                                                                                                                 ###
  ### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'auxiliar_contable'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
    'rango_fechas': fields.boolean("Por Rango de Fechas"),
    'por_periodo': fields.boolean("Por Periodo"),
    'fecha_inicio':fields.date("Fecha inicio", required=True),
    'fecha_fin':fields.date("Fecha fin", required=True),
  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #
    'period_id': fields.many2one('account.period', 'Periodo', required=True),
    'account_id': fields.many2one('account.account', 'Cuenta', required=True),
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
    'period_id': _obtener_periodo,
    'fecha_inicio': lambda *a: time.strftime('%Y-%m-01'),
    'fecha_fin': lambda *a: time.strftime('%Y-%m-%d'),
  }
auxiliar_contable()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: