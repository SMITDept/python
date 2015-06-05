# -*- coding: utf-8 -*-

{
  'name': 'SM Códigos',
  'version': '1.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': """
      Modulo: SM Codigos - Generador de Etiquetas.
      ====================================
      
      Modulo desarrollado para generar las etiquetas automaticamente de cada producto a traves de una lista codigos EAN-13 contiene las siguientes
      secciones:
      --------------------------------------------
          * Generador de codigos - Wizard que genera las etiquetas a partir de la insercion de una lista de codigos en el área de texto.
          * Listado de codigos - Muestra los datos relacionados con los códigos previamente insertados en el generador de codigos.
         
      
      El modulo requiere de la instalación especial de la libreria:
      --------------------------------------------------
          * pyBarcode
          
      Crea el codigo de barras como imagen, Se puede consultar para su instalacion el siguiente Link: https://pypi.python.org/pypi/pyBarcode/0.7
    """,
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
     'listado_codigo/listado_codigo_view.xml',
     'wizard/wizard_codigo_view.xml',
  ],
  'demo_xml': [
               ],
  'update_xml': [
                  ],
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}
