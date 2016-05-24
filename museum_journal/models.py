# coding=utf-8 #
from openerp import models, api, fields

MUSEUMS = [
    ('1', u'Первый музей'),
    ('2', u'Второй музей'),
    ('3', u'Третий музей'),
]


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


class Organization(models.Model):
    _name = 'museum.journal.organization'
    _rec_name = 'name'

    name = fields.Char(string=u'Наименование', required=True, size=300)
    history = fields.One2many(string=u'История', compute='_get_history', comodel_name='museum.journal.event')

    @api.one
    def _get_history(self):
        event_ids = self.env['museum.journal.event'].search([('organization', '=', self.id)])
        if event_ids:
            self.history = event_ids[-20:]
        else:
            self.history = None


class Event(models.Model):
    _name = 'museum.journal.event'
    _rec_name = 'name'

    name = fields.Char(string=u'Экскурсия', required=True, size=400)
    museum_address = fields.Selection(selection=MUSEUMS, default='1', string=u'Музей')
    worker = fields.Many2one(string=u'Экскурсовод', required=True, comodel_name='museum.journal.worker')
    organization = fields.Many2one(string=u'Организация', comodel_name='museum.journal.organization')
    amount = fields.Integer(string=u'Кол-во', default=0)
    validity_from = fields.Datetime(string=u'Срок действия с')
    validity_to = fields.Datetime(string=u'Срок действия до')
    comment = fields.Text(string=u'Примечание')
