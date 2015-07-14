# -*- coding: utf-8 -*-

{
  'name': 'SM Comparison TC VTA',
  'version': '0.1.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Comparison of credit card with sales.',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
    'account',
  ],
  #XML imports
  'data': [
    'menus.xml',
    'secciones/wizard/report/comparision_tc_vta_view.xml',
  ],

  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}