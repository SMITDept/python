# -*- coding: utf-8 -*-

{
  'name': 'SM Expiration Products',
  'version': '0.2.0',
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
    'web',
  ],
  #XML imports
  'data': [
    'menus.xml',
    'secciones/wizard/add_product/expiration_products_view.xml',
    'secciones/wizard/products_report/products_report_view.xml',
    'secciones/wizard/next_expire/next_expire_view.xml',
    'secciones/wizard/log_report/log_report_view.xml',
    'secciones/product_list/product_list_view.xml',
  ],

  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}