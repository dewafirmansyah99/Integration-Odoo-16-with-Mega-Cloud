from odoo import models, fields
from odoo.exceptions import *
from mega import Mega
from pathlib import Path
import datetime
import base64
import os
import humanize


class CheckFiles(models.Model):
    _name = 'check.files'
    _description = 'Check Files in From Mega in Oddo 16'

    name = fields.Char('Name')
    check_line = fields.One2many('check.line', 'check_id', string='Files')
    account_id = fields.Many2one('login.user', string='Account')
    download_file = fields.Binary('Download', readonly=True)

    def name_get(self):
        res = []
        for rec in self:
            total_file = []
            for line in rec.check_line:
                total_file.append(line.number)
            res.append((rec.id, '%s [Total File : %s]' % (rec.account_id.username, len(total_file))))
        return res

    def action_get_file(self):
        mega = Mega()
        mega.login(self.account_id.email, self.account_id.password)
        user =  mega.get_user()
        files = mega.get_files()
        i = 0
        for rec in self:
            lines = []
            rec.check_line.unlink()
            for line in self.account_id:
                sum_total = []
                for x in files:
                    if files[x]['t'] == 0:
                        file_name = files[x]['a']['n']
                        file_size = int(files[x]['s'])
                        file_time = files[x]['ts']
                        datetime_now = datetime.datetime.fromtimestamp(file_time)
                        export_file = mega.export(file_name)
                        dir_path = os.path.dirname(os.path.realpath(__file__))
                        mega.download_url(export_file, dest_path=dir_path)
                        final_path = dir_path + '/' + file_name
                        i += 1
                        vals = {
                            'name': file_name,
                            'size': str(humanize.naturalsize(file_size)),
                            'size_of_byte': file_size,
                            'last_modified': datetime_now,
                            'filename': file_name,
                            'number': str(i)
                        }
                        lines.append((0, 0, vals))
                        sum_total.append(files[x]['s'])
            rec.check_line = lines
            for res in rec.check_line:
                res.attachment_file()


class CheckLine(models.Model):
    _name = 'check.line'

    check_id = fields.Many2one('check.files', string='Files')
    name = fields.Char('Name', readonly=True)
    size = fields.Char('Size', readonly=True)
    last_modified = fields.Datetime('Last Modified', readonly=True)
    download_file = fields.Binary('Download', readonly=True)
    filename = fields.Char('filename')
    number = fields.Char('No', readonly=True)
    size_of_byte = fields.Integer('Size Of Byte', readonly=True)

    def attachment_file(self):
        for rec in self:
            path_to_file = Path(os.path.dirname(os.path.realpath(__file__)) + '/' + rec.filename)
            with open(path_to_file, 'rb+') as cf:
                cd = cf.read()
                io = base64.b64encode(cd)
            rec.write({'download_file': io})
            os.remove(path_to_file)

    def delete_line(self):
        mega = Mega()
        mega.login(self.check_id.account_id.email, self.check_id.account_id.password)
        for rec in self:
            export_link = mega.export(rec.name)
            mega.delete_url(export_link)
            # mega.empty_trash()
            rec.unlink()
