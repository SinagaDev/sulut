# -*- coding: utf-8 -*-
{
    'name': "sulut",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/urusan_views.xml',
        'views/program_views.xml',
        'views/sub_unit_views.xml',
        'views/skpd_views.xml',
        'views/bidang_urusan_views.xml',
        'views/kegiatan_views.xml',
        'views/sumber_dana_views.xml',
        'views/rekening_views.xml',
        'views/sub_kegiatan_views.xml',
        'views/belanja_views.xml',
        'views/data_penting_views.xml',
        'views/sk_berjalan_views.xml',
        'views/pendapatan_views.xml',
        'views/sk_pergeseran_anggaran_views.xml',
        'views/sk_lainnya_views.xml',
        'views/import_master_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'sulut/static/src/css/style.css',
        ],
    },
}

