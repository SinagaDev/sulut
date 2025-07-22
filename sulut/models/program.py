from odoo import _, api, fields, models


class Program(models.Model):
    _name = 'program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Master Data Program'
    # _rec_name = 'code'
    _order = 'code asc'
    
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
    bidang_urusan_id = fields.Many2one('bidang.urusan', string='Bidang Urusan', tracking=True)
