# coding=utf-8 #
from openerp import models, api, fields


class Worker(models.Model):
    _name = 'museum.journal.worker'
    _rec_name = 'full_name'

    last_name = fields.Char(string=u'Фамилия', required=True, index=True, size=100)
    first_name = fields.Char(string=u'Имя', required=True, size=100)
    middle_name = fields.Char(string=u'Отчество', required=True, size=100)
    full_name = fields.Char(string=u'ФИО', compute="_full_name", search="_search_full_name")
    phone_number = fields.Char(string=u'Номер телефона', required=False, size=50)

    @api.one
    @api.depends('last_name', 'first_name', 'middle_name')
    def _full_name(self):
        self.full_name = u'%s %s %s' % (self.last_name, self.first_name, self.middle_name)

    def _search_full_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'

        return ['|', '|',
                ('last_name', operator, value),
                ('first_name', operator, value),
                ('middle_name', operator, value),
                ]
