# -*- coding: utf-8 -*-

{
  'name': 'SM Equipment',
  'version': '1.0',
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
    'hardware_inventory',
  ],
  #XML imports
  'data': [
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: XML PARA MODELOS DEL SISTEMA ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    
    #Archivo principal de menús
    'menus.xml',
     'secciones/administracion/catalogos/cat_tipo_equipo/cat_equipo.xml',
     'secciones/inventory_equip/equipo_views.xml',
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