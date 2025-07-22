from odoo import _, api, fields, models


class SubUnit(models.Model):
    _name = 'sub.unit'
    _description = 'Master Data Sub Unit'
    # # _rec_name = 'code'
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

    name = fields.Char(string='Name')
    code = fields.Char('Code')
