# coding=utf-8 #
from openerp import models, api, fields
from dateutil.relativedelta import relativedelta


class Client(models.Model):
    _name = 'gcap.fix.client'
    _rec_name = 'full_name'
    last_name = fields.Char(string=u'Фамилия', required=True, index=True, size=100)
    first_name = fields.Char(string=u'Имя', required=True, size=100)
    middle_name = fields.Char(string=u'Отчество', required=True, size=100)
    organization = fields.Char(string=u'Организация', required=False, size=100)
    full_name = fields.Char(string=u'ФИО', compute="_full_name", search="_search_full_name")
    order = fields.One2many(string=u'Заказы', comodel_name='gcap.fix.order', inverse_name='client', ondelete='restrict')
    tel_number = fields.Char(string=u'Номер телефона', required=False, size=50)
    address = fields.Char(string=u'Адрес', required=False, size=100)

    #кнопочку сформировать логин/пароль для клиента

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

class DeviceModel(models.Model):
    _name = 'gcap.fix.devmod'
    _rec_name = 'full_name'
    manufacturer = fields.Char(string=u'Производитель', required=True, index=True, size=100)
    model = fields.Char(string=u'Модель', required=True, size=100)
    generation = fields.Selection(selection=[
    ('1', u'1gn'),
    ('2', u'2gn'),
    ('3', u'3gn'),
    ('4', u'4gn'),
    ('5', u'5gn'),
    ('6', u'6gn'),
    ('7', u'7gn'),
    ('6', u'8gn'),
    ('7', u'9gn'),
    ('6', u'10gn'),
], string=u'Поколение')
    full_name = fields.Char(string=u'Полное название', compute="_full_name", search='_search_full_name')
    order = fields.One2many(string=u'Заказы', comodel_name='gcap.fix.order', inverse_name='devmod', ondelete='restrict')

    @api.one
    @api.depends('manufacturer', 'model')
    def _full_name(self):
        self.full_name = u'%s %s' % (self.manufacturer, self.model)

    def _search_full_name(self, operator, value):
        if operator == 'like':
            operator = 'ilike'

        return ['|', '|',
                ('manufacturer', operator, value),
                ('model', operator, value),
                ('generation', operator, value),
                ]

class Order(models.Model):
    _inherit = ['ir.needaction_mixin']
    _name = 'gcap.fix.order'

    readydate = fields.Datetime(string=u"Дата\время готовности")
    issuedate = fields.Datetime(string=u"Дата\время выдачи")
    estimatedreadydate = fields.Datetime(default=lambda self: fields.Datetime.to_string(fields.Datetime.from_string(fields.Datetime.now())+relativedelta(days=14)), string=u"Ориентировочная дата\время готовности")
    agreementdate = fields.Datetime(string=u"Дата\время согласования")
    parts_wdate = fields.Datetime(string=u"Дата\время ожидание з\ч")

    serialnumber = fields.Char(string=u'Сер. №', required=False, size=100)
    imei = fields.Char(string=u'IMEI', required=False, size=100)
    problemdesc = fields.Text(string=u'Неисправность со слов клиента')
    workdesc = fields.Text(string=u'Описание выполненых работ')

    create_maker = fields.Many2one(default=lambda self: self.env.user.employee_id ,string=u'Приниматель', comodel_name='gcap.fix.employee')
    ready_maker = fields.Many2one(string=u'Чинитель', comodel_name='gcap.fix.employee')
    issue_maker = fields.Many2one(string=u'Выдаватель', comodel_name='gcap.fix.employee')
    agreement_maker = fields.Many2one(string=u'Согласователь', comodel_name='gcap.fix.employee')
    parts_w_maker = fields.Many2one(string=u'Ожидатель з\ч', comodel_name='gcap.fix.employee')

    executive_engineer = fields.Many2one(string=u'Ответственный инжинер', comodel_name='gcap.fix.employee')

    #сделать вычисляемым + руб
    pre_price = fields.Float(default=0, required=True, string=u'Предварительная стоимость')
    real_price = fields.Float(default=0, string=u'Реальная стоимость')
    comment = fields.Text(string=u'Комментарий')
    condition = fields.Text(string=u'Комплектация и состояние')
    client = fields.Many2one(string=u'Клиент', required=True, comodel_name='gcap.fix.client')
    client_tel_number =fields.Char(related="client.tel_number")
    devmod = fields.Many2one(string=u'Устройство', required=True, comodel_name='gcap.fix.devmod')
    fix_type = fields.Selection([
        ('paid', "Платный"),
        ('warranty', "Гарантийный"),
        ('warranty_confirmation', "Подтверждение гарантии"),
    ], default='paid', string=u'Тип ремонта')
    warranty_period = fields.Selection([
        ('0', "Без гарантии"),
        ('1', "1 мес."),
        ('2', "2 мес."),
        ('3', "3 мес."),
    ], default='1', string=u'Гарантия')
    state = fields.Selection([
        ('received', "Принят"),
        ('agreement', "Согласование"),
        ('parts_w', "Ожидание з\ч"),
        ('done', "Готов"),
        ('issuedwf', "Выдан без ремонта"),
        ('issued', "Выдан"),
    ], default='received', string=u'Статус')

    @api.multi
    def action_received(self):
        self.state = 'received'
        self.create_maker=self.env.user.employee_id

        self.readydate=''
        self.ready_maker=''
        self.issuedate=''
        self.issue_maker=''
        self.parts_wdate=''
        self.parts_w_maker=''
        self.agreementdate=''
        self.agreement_maker=''

    @api.multi
    def action_agreement(self):
        self.state = 'agreement'
        self.agreementdate=fields.Datetime.now()
        self.agreement_maker=self.env.user.employee_id

    @api.multi
    def action_parts_w(self):
        self.state = 'parts_w'
        self.parts_wdate=fields.Datetime.now()
        self.parts_w_maker=self.env.user.employee_id

    @api.multi
    def action_done(self):
        self.state = 'done'
        self.readydate=fields.Datetime.now()
        self.ready_maker=self.env.user.employee_id

    @api.multi
    def action_issuedwf(self):
        self.state = 'issuedwf'
        self.issuedate=fields.Datetime.now()
        self.issue_maker=self.env.user.employee_id

    @api.multi
    def action_issued(self):
        self.state = 'issued'
        self.issuedate=fields.Datetime.now()
        self.issue_maker=self.env.user.employee_id

    @api.model
    def _needaction_domain_get(self):
        return [('state', '=', 'received')]


class Employee(models.Model):
    _name = 'gcap.fix.employee'
    _rec_name = 'full_name'
    last_name = fields.Char(string=u'Фамилия', required=True, index=True, size=200)
    first_name = fields.Char(string=u'Имя', required=True, size=100)
    middle_name = fields.Char(string=u'Отчество', required=True, size=100)
    full_name = fields.Char(string=u'ФИО', compute="_full_name", search='_search_full_name')
    position = fields.Selection(selection=[
        ('acceptor', u'Приемщик'),
        ('master', u'Мастер'),
        ('admin', u'Администратор'),
    ], default='master',  required=True, string=u'Должность')

    create_order = fields.One2many(comodel_name='gcap.fix.order', inverse_name='create_maker', ondelete='restrict')
    ready_order_maker = fields.One2many(comodel_name='gcap.fix.order', inverse_name='ready_maker', ondelete='restrict')
    create_order_maker = fields.One2many(comodel_name='gcap.fix.order', inverse_name='create_maker', ondelete='restrict')
    agreement_order_maker = fields.One2many(comodel_name='gcap.fix.order', inverse_name='create_maker', ondelete='restrict')
    parts_w_order_maker = fields.One2many(comodel_name='gcap.fix.order', inverse_name='create_maker', ondelete='restrict')

    order_executive_engineer = fields.One2many(string=u'Заказы', comodel_name='gcap.fix.order', inverse_name='executive_engineer', ondelete='restrict')


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

class User(models.Model):
    _inherit = 'res.users'

#    _sql_constraints = [
#        ('gcap.fix.employee', 'unique(employee_id)', u"Уникальный сотрудник"),
#    ]
    employee_id = fields.Many2one(string=u'Сотрудник', comodel_name='gcap.fix.employee', ondelete='set null', required=False, groups="gcap_fix.group_gcap_fix_superuser")