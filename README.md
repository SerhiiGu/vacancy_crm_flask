# vacancy_crm_flask

# Підготовка:
1) Щоб тестувати пошту, треба додати свої дані в базу(тестувалося на gmail):
INSERT INTO "email_creds" (user_id, email, login, password, pop_server, imap_server, smtp_server, pop_port, imap_port, smtp_port )
VALUES (1, '!!!GMAIL_EMAIL', '!!!GMAIL_EMAIL', '!!!16-digit-password: https://myaccount.google.com/apppasswords ', 'pop.gmail.com' , 'imap.gmail.com', 'smtp.gmail.com', 995, 993, 465)

2) Для тестування mongo треба спочатку перейти на кореневий роут, який створить базу і колекцію:
http://localhost:7000/   # чи http://localhost:5000/ , якщо проєкт запускається локально
