from odoo import _, api, fields, models
from odoo.addons.base_field_big_int.field import BigInt

class TransaksiDataPenting(models.Model):
    _name = 'sk.berjalan'
    _description = 'SK Data Penting Berproses'
    # _rec_name = 'judul_sk'
    
    def act_submit(self):
        for rec in self:
            for data in rec.uraian_ids:
                data.file_sk = rec.file_sk
                data.filename_sk = rec.filename_sk
                data.sk_selesai = rec.x_studio_sk_selesai
                data.filename_sk = rec.sk_selesai_name
            rec.state = 'submit'
            
    def create(self, vals):
        if 'your_amount_field' in vals:
            vals['jumlah_realisasi_char'] = '{:,}'.format(int(vals['jumlah_realisasi_char'].replace(',', '')))
        return super(TransaksiDataPenting, self).create(vals)

            
    @api.depends('jumlah_alokasi_char','jumlah_realisasi_char')
    def _get_number(self):
        for rec in self:
            rec.jumlah_realisasi = int(rec.jumlah_realisasi_char)
            rec.jumlah_alokasi = int(rec.jumlah_alokasi_char)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
    ], string='state', default='draft')
    x_studio_sk_selesai = fields.Binary('SK Selesai')
    sk_selesai_name = fields.Char('SK Sekesai Name')
    judul_sk = fields.Char('Judul SK')
    sub_unit_id = fields.Many2one('sub.unit', string='Sub Unit')
    data_penting_id = fields.Many2one('data.penting', string='Uraian')
    uraian_ids = fields.Many2many('data.penting', string='Uraian')
    tahun = fields.Char('Tahun')
    nominal = BigInt('Nominal')
    jumlah_realisasi = BigInt('Jumlah Realisasi', compute='_get_number', store=True)
    jumlah_alokasi = BigInt('Jumlah Alokasi', compute='_get_number', store=True)
    jumlah_realisasi_char = fields.Char('Jumlah Realisasi (Rp.)')
    jumlah_alokasi_char = fields.Char('Jumlah Alokasi (Rp.)')
    keterangan = fields.Char('Keterangan')
    file_sk = fields.Binary('File SK', attachment=True)
    filename_sk = fields.Char('Filename SK')
    tipe_data_penting = fields.Selection([
        ('barang_diserahkan', 'Barang Diserahkan'),
        ('hibah', 'Hibah'), 
        ('bansos', 'Bansos'),
        ('lain_lain', 'Lain-Lain'),
    ], string='Tipe Data Penting')
    tipe_pergeseran = fields.Selection([
        ('1', ' Pergeseran Anggaran 1'),
        ('2', ' Pergeseran Anggaran 2')
    ], string='Pergeseran Anggaran')
    tipe_sk = fields.Selection([
        ('data_penting', 'Data Penting'),
        ('pergeseran_anggaran', 'Pergeseran Anggaran'),
        ('lainnya', 'Lainnya'),
    ], string='Tipe SK')