
from datetime import datetime, date
from pytz import timezone
from openerp.osv import osv,fields
from datetime import date
from openerp.tools.translate import _

def get_datetime():
	date = datetime.now(timezone( 'America/Mexico_City' )).strftime('%d/%m/%y %H:%M')
	return date

def get_date():
    """
    Devuelve la fecha actual en Mexico
    @return Devuelve (date) la fecha actual en Mexico
    """
    return datetime.now( timezone( 'America/Mexico_City' ) ).date()

#def compare date():


def update_schedule(cr, campo, datetime_register):
	cr.execute('UPDATE time_control SET %s = %s', (campo, datetime_register, total_hours))

def total_hours(hour_start, hour_end, total_db):
	hour_s = hour_start.split(' ')
	hour_s = hour_s[1]
	hour_s= hour_s.split(':')
	hour_start = hour_s[0]
	minutes_start = hour_s[1]

	hour_e = hour_end.split(' ')
	hour_e = hour_e[1]
	hour_e= hour_e.split(':')
	hour_end = hour_e[0]
	minutes_end = hour_e[1]

	total_hour = int(hour_end) - int(hour_start) 
	total_minutes = int(minutes_end) - int(minutes_start)
	if total_minutes < 0:
		total_minutes = total_minutes + 60
		if total_hour > 0:
			total_hour = total_hour -1

	hour_split= total_db.split(':')
	hour_db = hour_split[0]
	minutes_db = hour_split[1]

	total_hour = total_hour + int(hour_db)
	total_minutes = total_minutes + int(minutes_db)
	total = str(total_hour) + ":" + str(total_minutes)

	return total



class time_control(osv.osv):
	_name = 'time_control'
	_columns = {
	    'employee': fields.char("employee number", size=10, required=False),
	    'start_time': fields.datetime("start time", required=False),
	    'start_food': fields.datetime("start of food", required=False),
	    'end_food': fields.datetime("end of food", required=False),
	    'end_time': fields.datetime('end time', required=False),
	    'total_hours': fields.char("total hours", required=False),
	    'date_register': fields.date("date", required = False),
	    'user_m2o_id': fields.many2one('schedule_users', 'schedule_users', required=False),
	}

   	_defaults = {
  	}

	def search_employee(self, cr, uid, employee, context=None):
		print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
		employee_num = employee[0]
		
		datetime_register = get_datetime()
		date_register = get_date()

		cr.execute('SELECT employee_number, lunch_time, id FROM schedule_users where employee_number = %s', (employee_num,))
		employee = cr.fetchall()
		if employee:
			employee = employee[0]
			get_schedule = cr.execute('SELECT employee, start_time, start_food, end_food, end_time, total_hours FROM time_control where employee = %s and date_register = %s', (employee_num, date_register))
			employee_schedule = cr.fetchall()
			if employee_schedule:
				employee_schedule = employee_schedule[0]
				if employee[1]:
					if not employee_schedule[2]:
						#"Inicio de comida"
						total_hour = total_hours(employee_schedule[1], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET start_food = %s, total_hours = %s where employee = %s', (datetime_register, total_hour, employee_num,))
						return context

					if not employee_schedule[3]:
						#"Termina comida"
						total_hour = total_hours(employee_schedule[2], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET end_food = %s, total_hours = %s where employee = %s', (datetime_register, total_hour, employee_num,))
						return context

					if not employee_schedule[4]:
						#"hora de salida"
						total_hour = total_hours(employee_schedule[3], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET end_time = %s, total_hours = %s where employee = %s', (datetime_register, total_hour, employee_num,))
						return context

				else:
					if not employee_schedule[4]:
						#"hora de salida"
						total_hour = total_hours(employee_schedule[1], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET end_time = %s, total_hours = %s where employee = %s', (datetime_register, total_hour, employee_num,))
						return context
			else:
				user = employee[2]
				cr.execute('INSERT INTO time_control (employee, start_time, total_hours, date_register, user_m2o_id) VALUES (%s, %s, %s, %s, %s)', (employee_num, datetime_register, "0:00", date_register, user,))
				
		else:
			print"No existe usuario"	
		#raise osv.except_osv(_('Warning!'),_("error"))
		print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
		return context

time_control()