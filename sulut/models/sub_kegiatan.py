from odoo import _, api, fields, models


class SubKegiatan(models.Model):
    _name = 'sub.kegiatan'
    _description = 'Master Data Sub Kegiatan'
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
    kegiatan_id = fields.Many2one('kegiatan', string='Kegiatan')
