import string
import random
import hashlib

from openerp.osv import osv,fields
from datetime import date

def employee_number_generator(self, cr ,uid, context=None):
    size=6
    chars=string.ascii_uppercase + string.digits
    emplo_num = ''.join(random.choice(chars) for _ in range(size))
    cr.execute(
            """
              SELECT employee_number
              FROM schedule_users
              WHERE employee_number = %s
            """,(emplo_num,))
    num = cr.fetchall()
    if num:
        employee_number_generator
    else:
       return emplo_num

def md5_number_generator(self, cr ,uid, context=None):
    m = hashlib.md5()
    size=6
    chars=string.ascii_uppercase + string.digits
    md5_num = ''.join(random.choice(chars) for _ in range(size))
    cr.execute(
            """
              SELECT md5
              FROM schedule_users
              WHERE md5 = %s
            """,(md5_num,))
    md5 = cr.fetchall()
    if md5:
        md5_number_generator
    else:
        m.update(md5_num)
        return m.hexdigest()


class schedule_users(osv.osv):

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
        'employee_number': fields.char("Employee number", size=10, required=True, readonly=True),
        'md5': fields.char("MD5", size=50, required=True, readonly=True),
        'photo': fields.binary('Photo of the employee', required=False),
        'lunch_time': fields.boolean('Lunch time'),
        'sucursal': fields.many2one('location_user', 'Location', required=True),
    }

    _defaults = {
        'employee_number': employee_number_generator,
        'md5': md5_number_generator,
    }

schedule_users()