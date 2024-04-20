from odoo import models, fields
from mega import Mega
from pathlib import Path
import base64
import os


class UploadFile(models.TransientModel):
    _name = 'upload.file'
    _description = 'Upload a file to Mega'

    account_id = fields.Many2one('login.user', string='Upload to Account')
    upload_line = fields.One2many('upload.line', 'upload_id', string='Upload')
    folder_id = fields.Many2one('folder.name', string='Folder Name')

    def action_confirm_upload(self):
        mega = Mega()
        mega.login(self.account_id.email, self.account_id.password)
        for rec in self:
            if rec.folder_id:
                for res in rec.upload_line:
                    doc = base64.b64decode(res.upload_file)
                    path_file = Path(res.filename)
                    with open(path_file, 'wb') as f:
                        f.write(doc)
                    folder = mega.find(rec.folder_id.name)
                    mega.upload(path_file, folder[0])
                    os.remove(path_file)
            else:
                for res in rec.upload_line:
                    doc = base64.b64decode(res.upload_file)
                    path_file = Path(res.filename)
                    with open(path_file, 'wb') as f:
                        f.write(doc)
                    mega.upload(path_file)
                    os.remove(path_file)


class UploadLine(models.TransientModel):
    _name = 'upload.line'

    upload_id = fields.Many2one('upload.file', string='Upload')
    upload_file = fields.Binary('File')
    filename = fields.Char('Filename')
