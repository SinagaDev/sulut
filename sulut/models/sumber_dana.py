from odoo import _, api, fields, models


class SumberDana(models.Model):
    _name = 'sumber.dana'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Sumber Dana'
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
