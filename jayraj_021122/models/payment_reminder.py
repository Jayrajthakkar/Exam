from odoo import api, fields, models, _, tools
from datetime import date,timedelta
from ast import literal_eval

class PaymentReminderConfigs(models.Model):
	_name = "payment.reminder.configs"
	_description = "This Table Store Payment Reminder Data"


	def _default_template_id(self):
		return self.env.ref('jayraj_021122.payment_reminder_template_id').id

	name = fields.Char(string='Payment Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
	sale_domain = fields.Char(string="Sale Domain", default=[('state','=','sale')])
	mail_template_id = fields.Many2one(string="Mail Template", comodel_name="mail.template", default=_default_template_id)
	sale_order_ids = fields.One2many(string="Sale Order", comodel_name="sale.order", inverse_name="payment_reminder_id")
	deadline_days = fields.Integer(string="Deadline Days")
	user_id = fields.Many2one(string='User', comodel_name='res.users')
	partner_id = fields.Many2one(string='Partner', comodel_name='res.partner')
	mail_date = fields.Date(string='Mail Date', compute="date_mail_sent", store=True)

	#This Method IS Create Sequence
	@api.model
	def create(self,vals):
		vals['name'] = self.env['ir.sequence'].next_by_code(
	   'payment.reminder.configs') or _('New')
		return super(PaymentReminderConfigs,self).create(vals)

			 
	def _sale_domain(self):
		for sale_rec in self:
			domain = literal_eval(sale_rec.sale_domain or '[]')
			sale_record = self.env['sale.order'].search(domain)

			print('sale_order===============',sale_record)

	#This Method IS Create Mail For Cron Job
	def action_cron_sent_mail(self):
		template_id = self.env.ref('jayraj_021122.payment_reminder_template_id').id.send_mail(self.id,force_send=True)

	#This Method IS Display Formatted Name
	def name_get(self):
		result = []
		for payment_record in self:
			result.append((payment_record.id, "{} (Expire in {} days)".format(payment_record.name, payment_record.deadline_days)))

		return result

	#This Method Is Create Mail Sent Date
	def date_mail_sent(self):
		self.mail_date = date.today()

	
	#This Method IS Create Cron Job
	def sent_mail_cron(self):
		payment_record = self.env['payment.reminder.configs'].search([])
		for payment_rec in payment_record: 
			payment_rec.action_cron_sent_mail()
			due_date = payment_rec.mail_date + timedelta(days=7)
			print('due_date------',due_date )
			if  date.today() > due_date: 
				if payment_rec.sale_order_ids.invoice_status != "invoiced":
					payment_rec.sale_order_ids.action_cancel()
	




class SaleOrder(models.Model):
	_inherit="sale.order"

	payment_reminder_id = fields.Many2one(string="Parent Reminder", comodel_name="payment.reminder.configs", readonly=True)