# -*- coding: utf-8 -*-

######################################################################################################################################################
#  @version     : 1.0                                                                                                                                #
#  @autor       : SUPERMAS-ARC                                                                                                                       #
#  @creación    : 2015-06-15                                                                                                                         #
#  @linea       : Maximo 150 chars                                                                                                                   #
######################################################################################################################################################

#OpenERP Imports
from osv import fields, osv
# from datetime import datetime, date
from datetime import datetime, timedelta, date

import math

from openerp import tools, SUPERUSER_ID
from openerp.tools.translate import _

from dateutil import parser
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from openerp.service import web_services


import pytz
import re
import time
from operator import itemgetter

#Modulo ::
class maintenance(osv.osv):
  #--------------------------------------------------------Variables Privadas y Publicas--------------------------------------------------------------

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS                                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  #---------------------------------------------------------Metodos Function--------------------------------------------------------------------------
  def _obtener_informe( self, cr, uid, ids, field_name, arg, context ) :
    """
    Función para el campo "Informacion"
    * Para OpenERP [field.function( ... )]
    * Argumentos OpenERP: [cr, uid, ids, field_name, arg, context]
    @return dict
    """
    result = {}
    for record in self.browse( cr, uid, ids, context ) :
      device = ''
      brad = ''
      model = ''
      serial = ''
      if (record.hardware_m2o_id) != 0:
        print record.hardware_m2o_id
        device = str( record.hardware_m2o_id.dispositivo_m2o_id.descripcion)
        brad = str( record.hardware_m2o_id.brad )
        model = str( record.hardware_m2o_id.model )
        serial = str( record.hardware_m2o_id.serial_number)
        # concatenando
        if model==False:
          modelo='\n'
        else :
          modelo= ', \n MODEL: '+ model 
        informe = 'DEVICE:' + device + ', \n BRAD: ' + brad + modelo + ', \n SERIE: ' + serial
        #convirtiendo a mayúsculas
        informe = informe.upper()
        result[record.id] = informe
      #Retornando los resultados evaluados
      return result
  #---------------------------------------------------------Metodos Function--------------------------------------------------------------------------
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS ONCHANGE                                                             ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ### 

  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                                 METODOS ORM                                                                  ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  def onchange_dates(self, cr, uid, ids, start_date, duration=False, end_date=False, allday=False, context=None):
    """Returns duration and/or end date based on values passed
    @param self: The object pointer
    @param cr: the current row, from the database cursor,
    @param uid: the current user's ID for security checks,
    @param ids: List of calendar event's IDs.
    @param start_date: Starting date
    @param duration: Duration between start date and end date
    @param end_date: Ending Datee
    @param context: A standard dictionary for contextual values
    """
    if context is None:
        context = {}

    value = {}
    if not start_date:
        return value
    if not end_date and not duration:
        duration = 1.00
        value['duration'] = duration

    start = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    if allday: # For all day event
        duration = 24.0
        value['duration'] = duration
        # change start_date's time to 00:00:00 in the user's timezone
        user = self.pool.get('res.users').browse(cr, uid, uid)
        tz = pytz.timezone(user.tz) if user.tz else pytz.utc
        start = pytz.utc.localize(start).astimezone(tz)     # convert start in user's timezone
        start = start.replace(hour=0, minute=0, second=0)   # change start's time to 00:00:00
        start = start.astimezone(pytz.utc)                  # convert start back to utc
        start_date = start.strftime("%Y-%m-%d %H:%M:%S")
        value['date'] = start_date

    if end_date and not duration:
        end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        diff = end - start
        duration = float(diff.days)* 24 + (float(diff.seconds) / 3600)
        value['duration'] = round(duration, 2)
    elif not end_date:
        end = start + timedelta(hours=duration)
        value['date_deadline'] = end.strftime("%Y-%m-%d %H:%M:%S")
    elif end_date and duration and not allday:
        # we have both, keep them synchronized:
        # set duration based on end_date (arbitrary decision: this avoid
        # getting dates like 06:31:48 instead of 06:32:00)
        end = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
        diff = end - start
        duration = float(diff.days)* 24 + (float(diff.seconds) / 3600)
        value['duration'] = round(duration, 2)

    return {'value': value}
 #--------------------------------------------------------------------------------------------------------------------------------------------------- 
  def create(self, cr, uid, vals, context = None ):
    """   
    Método "create" que se ejecuta justo antes (o al momento) de CREAR un nuevo registro en OpenERP.    
    * Argumentos OpenERP: [cr, uid, vals, context]    
    @param  
    @return bool    
    """
    nuevo_id = None
    # vals['number_order'] = get_number()
    nuevo_id = super( maintenance, self ).create( cr, uid, vals, context = context )
    return nuevo_id
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  ###                                                                                                                                              ###
  ###                                                  Atributos basicos de un modelo OPENERP                                                      ###
  ###                                                                                                                                              ###
  ### //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// ###
  
  #Nombre del modelo
  _name = 'maintenance'
  #Nombre de la tabla
  _table = 'maintenance'
  #Ordenar la vista
  # _order = ' '
 
  _columns = {
    'number_order' : fields.char("Number", requiered=False),
    #calendar
    'name': fields.char('Description', size=64, required=False ),
    'date': fields.datetime('Maintenance Date'),
    'date_deadline': fields.datetime('Maintenance End Date'),
    'duration': fields.float('Duration'),
    'show_as': fields.selection(
      [
       ('free', 'Free'),
       ('busy', 'Busy')
      ],
      'Show Time as',
    ),
    'allday': fields.boolean('All Day'),
    #----------------------------------------------
    'type_maint' : fields.selection(
      (
        ( 'preventive', 'Preventive' ),
        ( 'corrective', 'Corrective' ),
      ),
      'Type of maintenance',
    ),
    'maintenance_date':fields.date("Maintenance Date", required=False),
    'next_maintenance_date':fields.date("Next Maintenance", required=False),
    'delivery_date':fields.date("Delivery date", required=False),
    'causes':fields.text("Defects according to the user"),
    'diagnostic':fields.text("Diagnostic"),
    'solution':fields.text("Solution"),
    'piece_change':fields.text("Piece to change"),
  # ================================ Relaciones [one2many](o2m) =====================================================================================#
    'hardware_m2o_id': fields.many2one(
      'hardware',
      'Device key',
      required = True
    ),
    'sucursal_m2o_id': fields.many2one(
      'sucursal',
      'New location',
      requiered=False
    ),
    'user_id': fields.many2one('res.users', 'Responsible'),
    # 'responsible_m2o_id': fields.many2one(
    #   'hr.employee',
    #   'Responsible',
    #   requiered=False
    # ),

  # ================================== Campos Function ==============================================================================================#  
    'hardware_brad' : fields.function(
      _obtener_informe,
      type = 'char',
      size = 80,
      method = True,
      string = 'Brad',
      store = False,
      readonly = True,
    ),
  }
    
  #Valores por defecto de los campos del diccionario [_columns]
  _defaults = {
    'user_id': lambda self, cr, uid, c: uid,
    'show_as': 'busy',
    'name' : 'Mantenimiento',
    'allday': False
  }

#se cierra la clase
maintenance() 


