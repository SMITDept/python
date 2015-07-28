# -*- coding: utf-8 -*-

{
  'name': 'SM Expiration Products',
  'version': '0.1.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Date of Expiration Products',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'board',
    'sale',
  ],
  #XML imports
  'data': [
    'menus.xml',
    'secciones/wizard/report/expiration_products_view.xml',
    'secciones/product_list/product_list_view.xml',
  ],

  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}