# -*- coding: utf-8 -*-

{
  'name': 'SM Users Control',
  'version': '0.2.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Users Control.',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
  ],
  #XML imports
  'data': [
    'menus.xml',
    'secciones/schedule_users/schedule_users_view.xml',
    'secciones/wizard/report/schedule_report_view.xml',
    'secciones/location_user/location_user_view.xml',
  ],

  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}