# -*- coding: utf-8 -*-

{
  #Características del modulo generales del modulo.
  'name': 'SM Expiration Products',
  'version': '0.2.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Date of Expiration Products',
  #Módulos de los cual les depende su funcionamiento.
  'depends': [
    'base',
    'board',
    'sale',
    'web',
  ],
  #Importación de las vistas del modulo
  'data': [
    'menus.xml',
    'secciones/wizard/add_product/expiration_products_view.xml',
    'secciones/wizard/products_report/products_report_view.xml',
    'secciones/wizard/next_expire/next_expire_view.xml',
    'secciones/wizard/log_report/log_report_view.xml',
    'secciones/product_list/product_list_view.xml',
  ],
  #Características de la instalación del modulo
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}