from djmail import template_mail


class MessageTemplateEmail(template_mail.TemplateMail):
    name = "message"
