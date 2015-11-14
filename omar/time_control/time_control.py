# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP
from datetime import datetime, date
from pytz import timezone
from openerp.osv import osv,fields
from datetime import date

#Librerías para mostrar mensajes en pantalla
from openerp.exceptions import Warning
from openerp.tools.translate import _

#Obtiene la fecha y hora actual
def get_datetime():
	date = datetime.now(timezone( 'America/Mexico_City' )).strftime('%Y-%m-%d %H:%M:%S')
	return date

#Obtiene la fecha actual
def get_date():
    """
    Devuelve la fecha actual en Mexico
    @return Devuelve (date) la fecha actual en Mexico
    """
    return datetime.now( timezone( 'America/Mexico_City' ) ).date()


def update_schedule(cr, campo, datetime_register):
	cr.execute('UPDATE time_control SET %s = %s', (campo, datetime_register, total_hours))

#Suma las horas para sacar un total
def total_hours(hour_start, hour_end, total_db):
	resta = datetime.strptime(hour_end, '%Y-%m-%d %H:%M:%S') - datetime.strptime(hour_start, '%Y-%m-%d %H:%M:%S')
	suma = datetime.strptime(total_db, '%Y-%m-%d %H:%M:%S') + resta
	return suma

#Modelo 
class time_control(osv.osv):
	#Nombre del Modelo
	_name = 'time_control'

	_columns = {
	    'employee': fields.char("employee number", size=10, required=True),
	    'start_time': fields.datetime("start time", required=True),
	    'start_food': fields.datetime("start of food", required=False),
	    'end_food': fields.datetime("end of food", required=False),
	    'end_time': fields.datetime('end time', required=False),
	    'total_hours': fields.datetime("total hours", required=True),
	    'date_register': fields.date("date", required = True),
	    'user_m2o_id': fields.many2one('schedule_users', 'schedule_users', required=True),
	    'location_m2o_id': fields.many2one('location_user', 'location_user', required=True),
	}

   	_defaults = {
  	}

  	#Registra la hora al momento de checar
	def search_employee(self, cr, uid, employee, context=None):
		#Obtiene fecha y hora actual
		datetime_register = get_datetime()

		#Obtiene fecha actual
		date_register = get_date()

		#Obtiene el numero del empleado
		employee_num = employee[0]

		#Verifica si el numero es de una tarjeta de crédito o de la credencial de empleado
		if employee_num[0] == "%":
			num_card = employee_num.split("&")
			num_card = num_card[0]
			employee_num = num_card[2:17]

		#Realiza una consulta para buscar al empleado
		cr.execute('SELECT employee_number, lunch_time, id, sucursal FROM schedule_users where md5 = %s', (employee_num,))

		employee = cr.fetchall()
		#Verifica si existe el empleado
		if employee:
			employee = employee[0]
			cr.execute('SELECT employee, start_time, start_food, end_food, end_time, total_hours FROM time_control where employee = %s and user_m2o_id = %s and date_register = %s', (employee[0], employee[2], date_register,))
			employee_schedule = cr.fetchall()
			#Verifica si el empleado ya tiene un registro en la fecha actual
			if employee_schedule:
				employee_schedule = employee_schedule[0]
				#Verifica si el empleado tiene horario de comida
				if employee[1]:
					if not employee_schedule[2]:
						#"Inicio de comida"
						total_hour = total_hours(employee_schedule[1], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET start_food = %s, total_hours = %s where employee = %s and user_m2o_id = %s and date_register = %s', (datetime_register, total_hour, employee[0], employee[2], date_register,))
						return"Registro guardado"

					if not employee_schedule[3]:
						#"Termina comida"
						total_hour = total_hours(employee_schedule[2], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET end_food = %s, total_hours = %s where employee = %s and user_m2o_id = %s and date_register = %s', (datetime_register, total_hour, employee[0], employee[2], date_register,))
						return"Registro guardado"

					if employee_schedule[4]:
						return"Ya no puedes realizar mas registros"

					if not employee_schedule[4]:
						#"hora de salida"
						total_hour = total_hours(employee_schedule[3], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET end_time = %s, total_hours = %s where employee = %s and user_m2o_id = %s and date_register = %s', (datetime_register, total_hour, employee[0], employee[2], date_register,))
						return"Registro guardado"

				else:
					if employee_schedule[4]:
						return"Ya no puedes realizar mas registros"
					
					if not employee_schedule[4]:
						#"hora de salida"
						total_hour = total_hours(employee_schedule[1], datetime_register, employee_schedule[5])
						cr.execute('UPDATE time_control SET end_time = %s, total_hours = %s where employee = %s and user_m2o_id = %s and date_register = %s', (datetime_register, total_hour, employee[0], employee[2], date_register,))
						return"Registro guardado"
			else:
				#Crea un nuevo registro si el empleado no tiene un registro de la fecha actual
				user = employee[2]
				cr.execute('INSERT INTO time_control (employee, start_time, total_hours, date_register, user_m2o_id, location_m2o_id) VALUES (%s, %s, %s, %s, %s, %s)', (employee[0], datetime_register, datetime(9999, 01, 01, 00, 00, 00), date_register, user, employee[3]))
				return"Registro guardado"
				
		else:
			return"No existe usuario"
		return context

time_control()