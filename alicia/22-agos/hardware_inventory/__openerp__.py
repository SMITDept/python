# -*- coding: utf-8 -*-

{
  'name': 'SM Equipment',
  'version': '3.0',
  'category': 'SUPERMAS',
  'author': 'SUPERMAS',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Módulo SM Inventory - Modulo para el Inventario de Equipo y Mantenimiento',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
    'hr',
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
      #catalogos
     'secciones/administracion/sucursal/sucursal.xml',
     'secciones/administracion/catalogos/cat_dispositivos/cat_dispositivos.xml',
     'secciones/administracion/catalogos/cat_equipo/cat_equipo.xml',
     'secciones/administracion/catalogos/cat_tipo_documento/cat_tipo_documento.xml',
     'secciones/administracion/adjuntos/adjuntos_view.xml',
     #
     'secciones/hardware/hardware_views.xml',
     'secciones/maintenance/maintenance_view.xml',
     'secciones/equipo/equipo_views.xml',
     'secciones/maintenance_equip/maintenance_equip.xml',

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