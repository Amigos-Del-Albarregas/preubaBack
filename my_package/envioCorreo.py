from email.message import EmailMessage
import ssl
import smtplib

smtp_server = "smtp-relay.sendinblue.com"
port = 587
sender_email = 'proyectoceiabd@gmail.com'
email_receiver = 'adrian.correa.cordero@gmail.com'
em = EmailMessage()
em['From'] = 'proyectoceiabd@gmail.com'
em['To'] = 'adrian.correa.cordero@gmail.com'
em['Subject'] = "Alerta CEIABD"
em.set_content("La ruido ha sobrepasado el umbral definido")

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()
    server.starttls(context=context) # Secure the connection
    server.ehlo()
    server.login(sender_email, 'C6GqRdTX8ZE5cU4g')
    server.sendmail(sender_email, email_receiver, em.as_string())
print('Correo enviado')