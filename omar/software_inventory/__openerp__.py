# -*- coding: utf-8 -*-
{
    #Características generales del modulo.
    'name': 'SM Software Inventory',
    'version': '0.2.0',
    'description': """
    Software Inventory.
    ===================================================
    """,
    'author': 'Omar Pluma Pluma',
    #Módulos de los cual les depende su funcionamiento.
    'depends': ['hardware_inventory'],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    #Importación de las vistas del modulo
    'data': [
	'software_inventory.xml'
    ],
    #Características de la instalación del modulo
    'installable': True,
    'active': False,
}
