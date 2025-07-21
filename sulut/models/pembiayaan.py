from odoo import _, api, fields, models
from odoo.addons.base_field_big_int.field import BigInt

class Pembiayaan(models.Model):
    _name = 'pembiayaan'
    _description = 'Data Pembiayaan'

    name = fields.Char(string='')
    tahun = fields.Char('Tahun')
    sub_unit_id = fields.Many2one('sub.unit', string='Sub Unit')
    rekening_id = fields.Many2one('rekening', string='Rekening')
    pagu_char = fields.Char('Pagu Char')
    pagu = fields.Float('Pagu', compute='_compute_pagu', store=True)
    tipe_pembiayaan = fields.Selection([
        ('ranwal_rkpd', 'Ranwal RKPD'),
        ('penetapan', 'Penetapan'),
        ('pergeseran_1', 'Pergeseran 1'),
        ('pergeseran_1_setelah_perubahan_apbd', 'Pergeseran 1 setelah Perubahan APBD'),
        ('pergeseran_2', 'Pergeseran 2'),
        ('ranhir', 'Ranhir RKPD'),
        ('penetapan_rkpd', 'Penetapan RKPD'),
        ('ranwal_perubahan_kua', 'Ranwal Perubahan KUA'),
        ('ranwal_kua', 'Ranwal KUA PPAS'),
        ('penetapan_kua', 'Penetapan KUA PPAS'),
        ('ranhir_kua', 'Ranhir KUA PPAS'),
        ('ranwal_perubahan_kua', 'Ranwal Perubahan KUA PPAS'),
        ('ranhir_perubahan_kua', 'Ranhir Perubahan KUA PPAS'),
        ('penetapan_perubahan_kua', 'Penetapan Perubahan KUA PPAS'),
        ('rancangan_perubahan_apbd', 'Rancangan Perubahan APBD'),
        ('penetapan_perubahan_apbd', 'Penetapan Perubahan APBD'),
        ('penyempurnaan_perubahan_apbd', 'Penyempurnaan Perubahan APBD'),
        ('ranwal_apbd', 'Ranwal Penetapan APBD'),
        ('rapbd_ke_kemendagri', 'RAPBD ke Kemendagri'),
    ], string='Tahapan Pembiayaan')
    uraian = fields.Char('Uraian')
    keterangan = fields.Char('Keterangan')
    
    @api.depends('pagu_char')
    def _compute_pagu(self):
        for rec in self:
            pagu = float(rec.pagu_char) if rec.pagu_char else 0
            rec.pagu = pagu
    
