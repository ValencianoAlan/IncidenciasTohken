import smtplib
from email.mime.text import MIMEText
from flask import current_app

def enviar_correo_escalacion(destinatarios, asunto, cuerpo_html):
    """
    Envía notificaciones de correo usando el servidor SMTP de Tohken.
    Soporta un string único o una lista de correos.
    """
    try:
        mensaje = MIMEText(cuerpo_html, 'html')
        mensaje["Subject"] = asunto
        mensaje["From"] = current_app.config["MAIL_USERNAME"]
        
        # Si llega una lista de correos, los junta separados por coma
        if isinstance(destinatarios, list):
            mensaje["To"] = ", ".join(destinatarios)
            lista_envio = destinatarios
        else:
            mensaje["To"] = destinatarios
            lista_envio = [destinatarios]

        with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"]) as server:
            server.starttls()
            server.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
            server.sendmail(current_app.config["MAIL_USERNAME"], lista_envio, mensaje.as_string())
        return True
    except Exception as e:
        print(f"Error crítico al enviar correo SMTP: {e}")
        return False