from odoo import _, api, fields, models


class Rekening(models.Model):
    _name = 'rekening'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Master Data Rekening'
    _order = 'code asc'
    _rec_name = 'code'
    
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

    name = fields.Char(string='Name', tracking=True)
    code = fields.Char('Code', tracking=True)
    pagu = fields.Float('Pagu', compute='compute_pagu', store=True)
    pagu_char = fields.Char('Pagu Char')
    tipe_akun = fields.Selection([
        ('belanja', 'Belanja'),
        ('pendapatan', 'Pendapatan'),
        ('pembiayaan', 'Pembiayaan'),
    ], string='Tipe Akun', tracking=True)
    @api.depends('pagu_char')
    def compute_pagu(self):
        for rec in self:
            rec.pagu = float(rec.pagu_char) if rec.pagu_char else 0
