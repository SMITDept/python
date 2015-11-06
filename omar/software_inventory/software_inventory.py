# coding: utf-8

#Importando las clases necesarias para construir un modelo OpenERP

from openerp.osv import osv,fields
from datetime import datetime, date
from pytz import timezone

#Diccionario de tipo de arquitecturas
ARCHITECTURE = [
    ('32', '32 bits'),
    ('64', '64 bits'),
]

#Modelo 
class software(osv.osv):

    #Nombre del Modelo
    _name = 'software'

    _columns = {
        'hardware_id': fields.many2one('hardware', 'Hardware', required=True),
        'software_o2m_ids': fields.one2many('software.detail', 'detail_m2o_id', 'Software detail'),
	}

    _defaults = {

    }

software()

#Modelo 
class software_detail(osv.osv):

    #Nombre del Modelo
    _name = 'software.detail'
    
    _columns = {
        'detail_m2o_id': fields.many2one('software', 'Update key', required = False),
        'name_software': fields.char("name software", size=150, required=True),
        'architecture': fields.selection(ARCHITECTURE, 'architecture', required=True),
        'license': fields.char("license", size=150, required=False),
        'version': fields.char("version", size=150, required=True),
        'expiration': fields.date("expiration"),
        'used': fields.integer("used", required=True),
        'free': fields.integer("free", required=True),
        'installation': fields.char("installation", size=100, required=True),
        'description': fields.text("description", required=False),
        'cost_software': fields.float("cost software", required=True),
    }

software_detail()
