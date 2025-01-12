from odoo import _, api, fields, models


class Rekening(models.Model):
    _name = 'rekening'
    _description = 'Master Data Rekening'
    # _rec_name = 'code'
    
    @api.depends('name', 'code')
    def name_get(self):
        result = []
        for record in self:
            if record.code:
                name = '[' + record.code + '] ' + record.name
            else:
                name = record.name
            result.append((record.id, name))
        return result

    name = fields.Char(string='Name')
    code = fields.Char('Code')
    pagu = fields.Float('Pagu', compute='compute_pagu', store=True)
    pagu_char = fields.Char('Pagu Char')
    tipe_akun = fields.Selection([
        ('belanja', 'Belanja'),
        ('pendapatan', 'Pendapatan'),
        ('pembiayaan', 'Pembiayaan'),
    ], string='Tipe Akun')
    @api.depends('pagu_char')
    def compute_pagu(self):
        for rec in self:
            rec.pagu = float(rec.pagu_char) if rec.pagu_char else 0
