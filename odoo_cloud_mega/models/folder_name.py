from odoo import models, fields
from mega import Mega
from odoo.exceptions import ValidationError

class FolderName(models.Model):
    _name = 'folder.name'

    name = fields.Char('Folder Name')
    renamed_folder_name = fields.Char('New Folder Name')
    total_file = fields.Integer('Total File')
    account_id = fields.Many2one('login.user', string='Account ID')
    is_created_folder = fields.Boolean('is created folder')

    def action_rename(self):
        for rec in self:
            if rec.account_id:
                mega = Mega()
                mega.login(rec.account_id.email, rec.account_id.password)
                export_link = mega.find(rec.name)
                rec.name = rec.renamed_folder_name
                mega.rename(export_link, rec.renamed_folder_name)
                rec.renamed_folder_name = False


class FolderSetting(models.TransientModel):
    _name = 'folder.setting'

    account_id = fields.Many2one('login.user', string='Account ID')
    folder_setting_line = fields.One2many('folder.setting.line', 'folder_setting_id', string='Folder Setting')
    category = fields.Selection([
        ('add', 'Add'),
        ('delete', 'Delete'),
    ], string='Category', default='add')

    def action_add_folder(self):
        for x in self:
            if x.account_id:
                for y in x.folder_setting_line:
                    if y.name:
                        mega = Mega()
                        mega.login(x.account_id.email, x.account_id.password)
                        mega.create_folder(y.name)
                        self.env['folder.name'].create({
                            'name': y.name,
                            'account_id': self.account_id.id,
                            'is_created_folder': True
                        })
            else:
                raise ValidationError('Please Select Account')

    def action_delete_folder(self):
        for rec in self:
            if rec.account_id:
                for line in rec.folder_setting_line:
                    if line.folder_id:
                        mega = Mega()
                        mega.login(rec.account_id.email, rec.account_id.password)
                        export_link = mega.find(line.folder_id.name)
                        mega.delete(export_link[0])
                        self.env['folder.name'].search([('name', '=', line.folder_id.name)]).unlink()


class FolderSettingLine(models.TransientModel):
    _name = 'folder.setting.line'

    folder_setting_id = fields.Many2one('folder.setting', 'Folder')
    folder_id = fields.Many2one('folder.name', string='Folder Name')
    name = fields.Char('Folder Name')
    total_file = fields.Integer('Total File', related='folder_id.total_file')
