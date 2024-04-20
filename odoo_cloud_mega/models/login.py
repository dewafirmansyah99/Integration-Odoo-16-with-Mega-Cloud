from odoo import models, fields
from odoo.exceptions import ValidationError
from mega import Mega
import datetime
import humanize


class LoginUser(models.Model):
    _name = 'login.user'
    _description = 'Login User'

    email = fields.Char('Email')
    password = fields.Char('Password')
    username = fields.Char('Username')
    last_login = fields.Datetime('Last Created')
    total_file = fields.Integer('Total File')
    total_folder = fields.Integer('Total Folder')
    used_storage = fields.Char('Used Storage')
    state = fields.Selection([
        ('not_active', 'Not Active'),
        ('active', 'Active')
    ], string='State', default="not_active")

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s' % (rec.email)))
        return res

    def action_login(self):
        mega = Mega()
        mega.login(self.email, self.password)
        user = mega.get_user()
        files = mega.get_files()
        limit_data = mega.get_storage_space()
        file_sizes = []
        folder_sizes = []
        for x in files:
            if files[x]['t'] == 0:
                file_name = files[x]['a']['n']
                file_size = files[x]['s']
                file_sizes.append((file_name))
            if files[x]['t'] == 1:
                folder_name = files[x]['a']['n']
                folder_sizes.append((folder_name))
        for rec in self:
            print(rec.password, "="*10)
            rec.username = user['name']
            rec.last_login = datetime.datetime.fromtimestamp(user['since'])
            rec.total_file = len(file_sizes)
            rec.total_folder = len(folder_sizes)
            rec.used_storage = humanize.naturalsize(limit_data['used'])
            rec.write({'state': 'active'})

    def action_logout(self):
        for x in self:
            x.username = False
            x.last_login = False
            x.total_file = False
            x.used_storage = False
            x.write({'state': 'not_active'})

    def scan_folder(self):
        mega = Mega()
        mega.login(self.email, self.password)
        files = mega.get_files()

        folder_names = []
        folder_id = []
        folder_item = []
        folder_item_count = []
        dict_data = {}

        for data in files:
            if files[data]['t'] == 1:
                folder_names.append(files[data]['a']['n'])
                folder_id.append(files[data]['h'])
            else:
                raise ValidationError('Folder Not Found or Already Exists')
        for data_names in folder_id:
            file_name = mega.get_files_in_node(data_names)
            folder_item.clear()
            for name_file in file_name:
                folder_item.append(file_name[name_file]['a']['n'])
            print(folder_item, "1"*10)
            print(len(folder_item), "|"*10)
            folder_item_count.append(len(folder_item))
        data_data = self.env['folder.name']
        for idx in range(len(folder_names)):
            existing_record = data_data.search([
                ('name', '=', folder_names[idx]),
            ])

            if existing_record:
                existing_record.unlink()
                data_data.create({
                    'name': folder_names[idx],
                    'total_file': folder_item_count[idx],
                    'account_id': self.id,
                    'is_created_folder': True
                })

            if not existing_record:
                data_data.create({
                    'name': folder_names[idx],
                    'total_file': folder_item_count[idx],
                    'account_id': self.id,
                    'is_created_folder': True
                })

    def action_empty_trash(self):
        mega = Mega()
        mega.login(self.email, self.password)
        mega.empty_trash()
