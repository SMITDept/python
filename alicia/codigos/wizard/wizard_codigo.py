# coding: utf-8

#########################################################################################################################
#  @version  : 1.0                                                                                                      #
#  @autor    : Supermas-ARC                                                                                             #
#  @creacion : 2015-05-22 (aaaa/mm/dd)                                                                                  #
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
class wizard_codigo(osv.osv_memory):
 
  #Descripcion tipo consulta
  _description = 'Wizard Codigo'
  
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------------------------------------------------------------------------------------------------  
  def obtenerCodigos( self, cr, uid, ids, context = None ):
    """
    Método para obtener codigos y mandar a imprimir las etiquetas
    * Argumentos OpenERP: [ cr, uid, ids, context ]
    @param : () 
    @return 
    """
    lista = self.pool.get( self._name ).browse( cr, uid, ids[0] ).lista
    if len(lista) < 13 or lista == '\n' :
      raise osv.except_osv(_( 'Aviso' ),_( 'Debe ingresar una lista de códigos' ) )
    buscar = self._obtener_codigos( cr, uid, lista)
    if buscar == True :
        #imprimir reporte
       if context is None:
         context = {}
       data = {}
       data['ids'] = context.get('active_ids', [])
       data['model'] = context.get('active_model', 'ir.ui.menu')
       data['form'] = self.read(cr, uid, ids )[0]
       #Inicializando la variable datas, con el modelo
       datas = {
         'ids': [],
         'model': 'listado_codigo',
         'form': data,
       }
       
       #Return el nombre del reporte que aparece en el service.name y el tipo de datos report.xml	
       return {
           'type': 'ir.actions.report.xml',
           'report_name': 'sm_etiquetas',
           'datas': datas,
           'nodestroy': True,
       }  
    else :
      return { 'value' : {} }
    
  #---------------------------------------------------------------------------------------------------------------------------------------------------
  def _obtener_codigos( self, cr, uid, lista ) :
    """
    Metodo que obtiene la informacion del producto apartir del codigo
    * Argumentos OpenERP: [cr]
    @param lista:
    @return string
    """
    listado = lista.split()
    valores = ' '
    fecha = time.strftime("%y%m%d")
    fecha_imp = time.strftime('%d/%m/%y')
    if ( type( listado ) in ( list, tuple ) ):
      #se eliminan los datos de la tabla listado antes de insertar
      cr.execute(
        """
        DELETE FROM listado_codigo
        """
      )
      #se recorre el listado
      for codigo in listado:
        if codigo.isdigit() == True:
          if len(codigo) != 13:
            nombre_produc ='NO ES EAN-13'
            raise osv.except_osv(_( 'Aviso' ),_( 'El código debe contener 13 números sin espacios entre cada dígito' ) )
          else :
            nombre_produc = 'NO ENCONTRADO'
        else :
          raise osv.except_osv(_( 'Aviso!' ),_( 'El código sólo debe contener números' ) )
        #Crea el codigo de Barras
        ean = barcode.get('ean13', codigo, writer=barcode.writer.ImageWriter())
        # Genera el archivo
        ruta = '/tmp/ean_'+ str(codigo)
        f = open(ruta , 'wb')
        #se crea la imagen y se guarda en la ruta especifica
        almacena = ean.write(f)
        #si no encuentra el producto insertar
        no_encontrado = (nombre_produc, codigo, 0.0, ruta, fecha, '0.00', str(fecha_imp) )
        #se ejecuta la consulta en la tabla productos
        cr.execute(
        """
          SELECT upper(name), ean13, list_price  
          FROM product_template t
          INNER JOIN product_product p
          ON t.id = p.product_tmpl_id
          WHERE ean13 =%s
        """,(codigo,)
        )
        resultado = cr.fetchone()
        valores = (
                    ( resultado[0], resultado[1], (resultado[2]), ruta, fecha, (str(resultado[2])+'0'), str(fecha_imp) )
                    if type( resultado ) in ( list, tuple ) and resultado != None else no_encontrado
                  )
        #se insertan los nuevos datos a la tabla listado_codigo
        cr.execute(
          """
          INSERT INTO listado_codigo
          (descripcion, cod_barras, precio, ruta_codigo, fecha, precio_str, fecha_str )
          VALUES (%s::varchar(24), %s, %s, %s, %s, %s, %s)
          """, valores )
      return True
    else :
      return False

	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
	###                                                                                                                 ###
	###                                       Atributos Básicos del Modelo OpenERP                                      ###
	###                                                                                                                 ###
	### /////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###

  #Nombre del Modelo
  _name = 'wizard_codigo'
  
  _columns = {
    
  # ==========================  Campos OpenERP Básicos (integer, char, text, float, etc...)  ======================== #
   'lista':fields.text("Lista de codigos", store = False, required=True),

  # ======================================  Relaciones OpenERP [one2many](o2m) ====================================== #
  
  }

  #Valores por defecto de los elementos del arreglo [_columns]
  _defaults = {
  }
   
  #Reestricciones desde código
  _constraints = [ ]

  #Reestricciones desde BD
  _sql_constraints = [ ]

wizard_codigo()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
