from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import xlrd
import binascii
import tempfile
from datetime import datetime

class ImportMasterData(models.TransientModel):
    _name = 'import.master.data'
    _description = 'Import Master Data'
    
    excel_file = fields.Binary('Excel File')
    file_name = fields.Char('File Name')
    tipe_import = fields.Selection([
        ('kegiatan', 'Kegiatan'),
        ('sub_kegiatan', 'Sub Kegiatan'),
        ('rekening', 'Rekening'),
    ], string='Import', required=True)

    def import_kegiatan(self):
        excel_file = self.excel_file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as fp:
            fp.write(binascii.a2b_base64(excel_file))
            fp.seek(0)
            wb = xlrd.open_workbook(fp.name)
            sheet = wb.sheet_by_index(0)

            for row_no in range(sheet.nrows):
                if row_no == 0:
                    continue  # Skip header row

                line = list(map(lambda row: isinstance(row.value, bytes) and row.value.decode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                code = str(line[0])
                name = str(line[1])
                values = {
                    'code': code,
                    'name': name,
                }
                if self.tipe_import == 'kegiatan':
                    kegiatan_obj = self.env['kegiatan'].search([('code', '=', code)], limit=1)
                    if not kegiatan_obj:
                        self.create_kegiatan(values)
                elif self.tipe_import == 'sub_kegiatan':
                    sub_kegiatan_obj = self.env['sub.kegiatan'].search([('code', '=', code)], limit=1)
                    if not sub_kegiatan_obj:
                        self.create_sub_kegiatan(values)
                elif self.tipe_import == 'rekening':
                    values.update({
                        'tipe_akun': line[2],
                    })
                    rekening_obj = self.env['rekening'].search([('code', '=', code)], limit=1)
                    if not rekening_obj:
                        self.create_rekening(values)
                else:
                    raise UserError("Tipe Import Tidak Valid")

    def create_kegiatan(self, values):
        kegiatan_obj = self.env['kegiatan']
        progres = kegiatan_obj.create({
            'name': values.get('name'),
            'code': values.get('code'),
        })
        return progres
    
    def create_sub_kegiatan(self, values):
        sub_kegiatan_obj = self.env['sub.kegiatan']
        progres = sub_kegiatan_obj.create({
            'name': values.get('name'),
            'code': values.get('code'),
        })
        return progres
    
    def create_rekening(self, values):
        rekening_obj = self.env['rekening']
        progres = rekening_obj.create({
            'name': values.get('name'),
            'code': values.get('code'),
            'tipe_akun': values.get('tipe_akun'),
        })
        return progres
