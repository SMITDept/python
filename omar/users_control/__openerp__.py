# -*- coding: utf-8 -*-

{
  'name': 'SM Users Control',
  'version': '0.1',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Time Control of the users.',
  #This model depends of BASE OpenERP model...
  'depends': [
    #'web',
    'base',
    'board',
    'hardware_inventory',
  ],
  #XML imports
  'data': [
    #Archivo principal de menús
    'menus.xml',
    #'secciones/time_control/time_control_view.xml',
    'secciones/schedule_users/schedule_users_view.xml',
    'secciones/wizard/report/schedule_report_view.xml',
  ],
  #'js': ['secciones/timerol/static/src/js/time_control.js'],
  #'qweb': ['secciones/time_control/static/src/xml/time_control.xml'],
  #'css': ['secciones/time_control/static/src/css/time_control.css'],
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}