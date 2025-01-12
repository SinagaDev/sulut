from odoo import _, api, fields, models
from odoo.addons.base_field_big_int.field import BigInt


class DataPenting(models.Model):
    _name = 'data.penting'
    _description = 'Data Penting Barang Diserahkan, Hibah, Bansos, Lain-lain'
    # _rec_name= 'uraian'
    
    uraian = fields.Char('Uraian')
    sk_selesai = fields.Binary('SK Selesai')
    sk_selesai_name = fields.Char('SK Sekesai Name')
    tipe_data_penting = fields.Selection([
        ('barang_diserahkan', 'Barang Diserahkan'),
        ('hibah', 'Hibah'), 
        ('bansos', 'Bansos'),
        ('lain_lain', 'Lain-Lain'),
    ], string='Tipe Data Penting')
    sub_unit_id = fields.Many2one('sub.unit', string='Sub Unit (OPD)')
    pagu_induk_2023 = BigInt('Pagu Induk APBD 2023', compute='_compute_pagu', store=True)
    pagu_induk_2024 = BigInt('Pagu Induk APBD 2024', compute='_compute_pagu', store=True)
    pagu_perubahan_2023 = BigInt('Pagu Perubahan 2023', compute='_compute_pagu', store=True)
    pagu_induk_2023_char = fields.Char('Pagu Induk APBD 2023 Char')
    pagu_induk_2024_char = fields.Char('Pagu Induk APBD 2024 Char')
    pagu_perubahan_2023_char = fields.Char('Pagu Perubahan 2023 Char')
    insentif_fiskal = BigInt('Insentif Fiskal', compute='_compute_pagu', store=True)
    insentif_fiskal_char = fields.Char('Insentif Fiskal Char')
    keterangan = fields.Char('Keterangan')
    file_sk = fields.Binary('File SK', attachment=True)
    filename_sk = fields.Char('Filename SK')
    
    @api.depends('pagu_induk_2023_char','pagu_induk_2024_char','pagu_perubahan_2023_char','insentif_fiskal_char')
    def _compute_pagu(self):
        for rec in self:
            rec.pagu_induk_2023 = float(rec.pagu_induk_2023_char) if rec.pagu_induk_2023_char else 0
            rec.pagu_induk_2024 = float(rec.pagu_induk_2024_char) if rec.pagu_induk_2024_char else 0
            rec.pagu_perubahan_2023 = float(rec.pagu_perubahan_2023_char) if rec.pagu_perubahan_2023_char else 0
            rec.insentif_fiskal = float(rec.insentif_fiskal_char) if rec.insentif_fiskal_char else 0