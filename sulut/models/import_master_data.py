from odoo import models, fields, api
from odoo.exceptions import UserError
import openpyxl
import binascii
import tempfile
import logging

_logger = logging.getLogger(__name__)

class ImportMasterData(models.TransientModel):
    _name = 'import.master.data'
    _description = 'Import Master Data'

    excel_file = fields.Binary('Excel File', required=True)
    file_name = fields.Char('File Name')
    tipe_import = fields.Selection([
        ('kegiatan', 'Kegiatan'),
        ('sub_kegiatan', 'Sub Kegiatan'),
        ('rekening', 'Rekening'),
        ('sumber_dana', 'Sumber Dana'),
        ('program', 'Program'),
    ], string='Import', required=True)

    def import_data(self):
        if not self.excel_file:
            _logger.warning("No Excel file uploaded.")
            raise UserError("Please upload an Excel file.")

        _logger.info("Starting import for type: %s", self.tipe_import)

        # Decode the Excel file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as fp:
            fp.write(binascii.a2b_base64(self.excel_file))
            fp.seek(0)
            _logger.info("Temporary Excel file created at: %s", fp.name)

            try:
                wb = openpyxl.load_workbook(fp.name, data_only=True)
                sheet = wb.active
            except Exception as e:
                _logger.exception("Failed to read Excel file.")
                raise UserError("Failed to read the uploaded Excel file.")

            for row_no, row in enumerate(sheet.iter_rows(values_only=True), start=1):
                if row_no == 1:
                    _logger.info("Skipping header row.")
                    continue

                try:
                    line = [str(val).strip() if val is not None else '' for val in row]
                    _logger.info("Row %d data: %s", row_no, line)

                    code = line[0]
                    name = line[1]
                    values = {'code': code, 'name': name}

                    if self.tipe_import == 'kegiatan':
                        self._process_record('kegiatan', values)
                    elif self.tipe_import == 'sub_kegiatan':
                        self._process_record('sub.kegiatan', values)
                    elif self.tipe_import == 'rekening':
                        values['tipe_akun'] = line[2] if len(line) > 2 else ''
                        self._process_record('rekening', values)
                    elif self.tipe_import == 'sumber_dana':
                        self._process_record('sumber.dana', values)
                    elif self.tipe_import == 'program':
                        self._process_record('program', values)
                    else:
                        _logger.error("Invalid import type: %s", self.tipe_import)
                        raise UserError("Invalid Import Type.")

                    _logger.info("Processed row %d for import type %s", row_no, self.tipe_import)

                except Exception as e:
                    _logger.exception("Error processing row %d: %s", row_no, e)
                    raise UserError(f"Error processing row {row_no + 1}: {e}")

    def _process_record(self, model_name, values):
        _logger.info("Starting to process record for model '%s' with values: %s", model_name, values)
        model = self.env[model_name]

        try:
            existing_record = model.search([('code', '=', values['code'])], limit=1)
            if existing_record:
                _logger.info("Record found by code [%s] in model [%s]. Updating name to '%s'.", values['code'], model_name, values['name'])
                existing_record.write({'name': values['name']})
            else:
                new_record = model.create(values)
                _logger.info("Created new record in model [%s]: ID=%s, Values=%s", model_name, new_record.id, values)
        except Exception as e:
            _logger.exception("Error processing record in model [%s] with values: %s", model_name, values)
