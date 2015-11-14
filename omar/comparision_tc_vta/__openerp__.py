# -*- coding: utf-8 -*-

{
  #Características generales del modulo.
  'name': 'SM Comparison TC VTA',
  'version': '0.2.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Comparison of credit card with sales.',
  #Módulos de los cual les depende su funcionamiento.
  'depends': [
    'base',
    'board',
    'account',
  ],
  #Importación de las vistas del modulo
  'data': [
    'menus.xml',
    'secciones/wizard/report/comparision_tc_vta_view.xml',
  ],

  #Características de la instalación del modulo
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}