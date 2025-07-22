from odoo import _, api, fields, models


class BidangUrusan(models.Model):
    _name = 'bidang.urusan'
    _description = 'Master Data Bidang Urusan'
    # # _rec_name = 'code'
    
    
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
    urusan_id = fields.Many2one('urusan', string='Urusan')
