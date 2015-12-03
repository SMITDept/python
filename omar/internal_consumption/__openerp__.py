# -*- coding: utf-8 -*-

{
  #Características generales del modulo.
  'name': 'SM Internal Consumption',
  'version': '0.3.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Internal consumption of products',
  #Módulos de los cual les depende su funcionamiento.
  'depends': [
    'base',
    'web',
  ],
  #Importación de las vistas del modulo
  'data': [
    'menus.xml',
    'secciones/order_internal_products/update_product_view.xml',
    'secciones/products/products_view.xml',
    'secciones/departments/departments_view.xml',
    'secciones/register_purchases/register_purchases_view.xml',
    'secciones/stock_departments/stock_departments_view.xml',
    'secciones/products_update/update_stock_view.xml',
    'secciones/log_purchases_report/log_purchases_view.xml',
    'secciones/log_stock_report/log_stock_view.xml',
    'secciones/log_orders_report/log_orders_view.xml',
    'secciones/users/admin_users_view.xml',
  ],
  #Características de la instalación del modulo
  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}
