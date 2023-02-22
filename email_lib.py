import smtplib, ssl, poplib, imaplib


class EmailWrapper:
    def __init__(self, user_email, login, password, smtp_server, port=465):
        self.user_email = user_email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.port = port

    def send_email(self, message, receiver_email):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.login, self.password)
            server.send_message(message, from_addr=self.user_email, to_addrs=receiver_email)


Mailbox = poplib.POP3_SSL('pop.gmail.com')
Mailbox.port = 995
Mailbox.user('gumenyuk.sergey.first@gmail.com')
Mailbox.pass_('sokrjidrqmglpvtv')

print(Mailbox.stat())
