
from openerp.osv import osv,fields


class departments_internal_consumption(osv.osv):

    _name = 'departments.internal.consumption'

    _columns = {
        'name': fields.char('Department name', size=50, required=True),
    }

    _defaults = {
        
    }

departments_internal_consumption()
