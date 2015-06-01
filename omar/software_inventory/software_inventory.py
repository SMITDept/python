from openerp.osv import osv,fields
from datetime import date


ARCHITECTURE = [
    ('32', '32 bits'),
    ('64', '64 bits'),
]

class software(osv.osv):
    _name = 'software'
    _columns = {
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
        'hardware_id': fields.many2one('hardware', 'Hardware', required=True),
	}

software()
