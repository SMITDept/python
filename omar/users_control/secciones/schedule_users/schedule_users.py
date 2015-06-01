import string
import random

from openerp.osv import osv,fields
from datetime import date

def employee_number_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class schedule_users(osv.osv):
    _name = 'schedule_users'
    _columns = {
        'name': fields.char("Name", size=100, required=True),
        'first_name': fields.char("First name", size=100, required=True),
        'second_name': fields.char("Second name", size=100, required=True),
        'employee_number': fields.char("Employee number", size=10, required=True, readonly=True),
        'photo': fields.binary('Photo of the employee', required=False),
        'lunch_time': fields.boolean('Lunch time'),
        #'schedules': fields.one2many('time_control', 'schedules_m2o_id', 'Schedules of the user'),
        'sucursal': fields.many2one('sucursal', 'Location', required = True),
    }

    _defaults = {
        'employee_number': employee_number_generator(),
    }

schedule_users()