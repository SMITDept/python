# -*- coding: utf-8 -*-
{
    #Características generales del modulo.
    'name': 'SM Time Control',
    'version': '0.2.1',
    'description': """
    Time Control of the users.
    ===================================================
    """,
    'author': 'Omar Pluma Pluma',
    #Módulos de los cual les depende su funcionamiento.
    'depends': ['web', 'users_control'],
    #Importación de las vistas del modulo
    'data': ['time_control_view.xml'],
    'js': ['static/src/js/time_control.js'],
    'qweb': ['static/src/xml/time_control.xml'],
    'css': ['static/src/css/time_control.css'],
    #Características de la instalación del modulo
    'installable': True,
    'active': False,
}
