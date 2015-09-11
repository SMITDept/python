import hashlib

from openerp.osv import osv,fields
from datetime import date


class users_internal_consumption(osv.osv):


    _name = 'users.internal.consumption'
    _columns = {
        'user_id': fields.many2one('res.users',"User", required=True, help="User who registered the measurement"),
    }

    _defaults = {
        
    }

users_internal_consumption()