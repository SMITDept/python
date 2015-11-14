# -*- coding: utf-8 -*-

{
  #Características generales del modulo.
  'name': 'SM Users Control',
  'version': '0.3.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Users Control.',
  #Módulos de los cual les depende su funcionamiento.
  'depends': [
    'base',
    'board',
  ],
  #Importación de las vistas del modulo
  'data': [
    'menus.xml',
    'secciones/schedule_users/schedule_users_view.xml',
    'secciones/wizard/report/schedule_report_view.xml',
    'secciones/location_user/location_user_view.xml',
  ],
  #Características de la instalación del modulo
  'active': False,
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}