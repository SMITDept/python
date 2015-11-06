# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

#Librería para generar md5 del numero de empleado
import hashlib

from openerp.osv import osv,fields
from datetime import date
    
#Modelo 
class schedule_users(osv.osv):

    #Diccionario de las formas de pago 
    PAYROLL = [
      ('Q', 'Fortnight'),
      ('S', 'Weekly'),
    ]

    #Genera el md5 con el numero de empleado y la forma de pago
    def md5_number(self, cr, uid, ids, fields, arg, context):
      m = hashlib.md5()
      em = {}
      for line in self.browse(cr, uid, ids):
          num = line.employee_number + line.payroll
          m.update(num)
          m = m.hexdigest()
          m = m[:-16]
          em[line.id] = m
      return em

    #Convierte el nombre a mayúsculas cuando existe un cambio en la caja de texto
    def onchange_name( self, cr, uid, ids, name ) :
        if name :
          return {
            'value' : {
              'name' : name.upper()
            }
          }
        return { 'value' : {} }

    #Convierte el nombre a mayúsculas cuando existe un cambio en la caja de texto
    def onchange_first_name( self, cr, uid, ids, first_name ) :
        if first_name :
          return {
            'value' : {
              'first_name' : first_name.upper()
            }
          }
        return { 'value' : {} }

    #Convierte el nombre a mayúsculas cuando existe un cambio en la caja de texto
    def onchange_second_name( self, cr, uid, ids, second_name ) :
        if second_name :
          return {
            'value' : {
              'second_name' : second_name.upper()
            }
          }
        return { 'value' : {} }

    #Convierte el nombre a mayúsculas cuando existe un cambio en la caja de texto
    def onchange_employee_number( self, cr, uid, ids, employee_number ) :
        if employee_number:
          if len(employee_number) < 2:
            employee_number = "0" + employee_number
            return {
              'value' : {
                'employee_number' : employee_number
              }
            }
          else:
            return {
              'value': {
                'employee_number': employee_number
              }
            }
        return { 'value' : {} }

    #Nombre del Modelo
    _name = 'schedule_users'

    _columns = {
        'name': fields.char("Name", size=100, required=True),
        'first_name': fields.char("First name", size=100, required=True),
        'second_name': fields.char("Second name", size=100, required=True),
        'employee_number': fields.char("Employee number", size=2, required=True),
        'md5': fields.function(md5_number, method=True, store=True, string="MD5", size=50, type='char', required=False, readonly=True),
        'photo': fields.binary('Photo of the employee', required=False),
        'lunch_time': fields.boolean('Lunch time'),
        'payroll':fields.selection(PAYROLL, 'Payroll', required =True),
        'sucursal': fields.many2one('location_user', 'Location', required=True),
    }

    _defaults = {
        
    }

    #Restricciones de BD (constraints)
    _sql_constraints = [
      ('md5_unique', 'unique(md5)', 'MD5 already exists!')
    ]

schedule_users()