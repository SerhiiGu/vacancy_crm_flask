import email.message
import smtplib, ssl, poplib, imaplib


poplib._MAXLINE = 20480


class EmailWrapper:
    def __init__(self, user_email, login, password, smtp_server, imap_server, pop_server,
                 smtp_port=465, imap_port=993, pop_port=995):
        self.user_email = user_email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.imap_server = imap_server
        self.pop_server = pop_server
        self.smtp_port = smtp_port
        self.imap_port = imap_port
        self.pop_port = pop_port

    def send_email(self, recipient, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.login, self.password)
            server.sendmail(self.user_email, recipient, message)

    def get_emails(self, messages, protocol='imap'):
        if protocol == 'pop3':
            return self.get_pop3(messages)
        elif protocol == 'imap':
            return self.get_imap(messages)
        else:
            raise ValueError('Unknown protocol')

    def get_pop3(self, messages):
        m = poplib.POP3_SSL(self.pop_server)
        m.port = self.pop_port
        m.user(self.login)
        m.pass_(self.password)
        # print(m.stat())
        result = []
        for number in messages:
            letter = m.retr(number)[1]
            result.append(str(letter))
        m.quit()
        return result

    def get_imap(self, messages):
        m = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        m.login(self.login, self.password)
        # print(m.select())
        m.select()
        result = []
        for number in messages:
            typ, data = m.fetch(str(number), '(RFC822)')
            email_message = email.message_from_bytes(data[0][1])
            result.append(email_message)
        m.close()
        m.logout()
        return result
