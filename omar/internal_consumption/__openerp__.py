# -*- coding: utf-8 -*-

{
  'name': 'SM Internal Consumption',
  'version': '0.2.0',
  'category': 'SUPERMAS',
  'author': 'Omar Pluma Pluma',
  'maintainer': 'SUPERMAS',
  'website': 'http://www.supermas.mx',
  'installable': True, 
  'active': False,
  'description': 'Internal consumption of products',
  #This model depends of BASE OpenERP model...
  'depends': [
    'base',
    'web',
  ],
  #XML imports
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

  'active': False,
  'application': True,
  'installable': True,
  'auto_install': False,
}
