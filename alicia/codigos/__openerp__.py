# -*- coding: utf-8 -*-

{
  'name': 'SM Codigo',
  'version': '1.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo Codigos- Modulo desarrollado para generar las etiquetas automaticamente de cada producto atraves de una lista codigos EAN-13',   
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
