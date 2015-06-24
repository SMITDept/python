import hashlib

from openerp.osv import osv,fields
from datetime import date


class schedule_users(osv.osv):

    PAYROLL = [
      ('Q', 'Fortnight'),
      ('S', 'Weekly'),
    ]

    def md5_number(self, cr, uid, ids, fields, arg, context):
      m = hashlib.md5()
      em = {}
      pay = {}
      for line in self.browse(cr, uid, ids):
          num = line.employee_number + line.payroll
          m.update(num)
          print m
          em[line.id] = m.hexdigest()

      print em
      print pay
      return em

    def onchange_name( self, cr, uid, ids, name ) :
        if name :
          return {
            'value' : {
              'name' : name.upper()
            }
          }
        return { 'value' : {} }

    def onchange_first_name( self, cr, uid, ids, first_name ) :
        if first_name :
          return {
            'value' : {
              'first_name' : first_name.upper()
            }
          }
        return { 'value' : {} }

    def onchange_second_name( self, cr, uid, ids, second_name ) :
        if second_name :
          return {
            'value' : {
              'second_name' : second_name.upper()
            }
          }
        return { 'value' : {} }


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

schedule_users()