from flask import Flask, request, render_template_string
import socket
import base64

app = Flask(__name__)


html_email = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
    <title>SMTP homemade</title>
</head>
<body>
    <h2>Redactar nuevo email</h2>
    <form method="post">
        Email: <input required type="text" name="username"><br>
        Contraseña: <input required type="password" name="password"><br>
        Asunto: <input type="text" name="subject"><br>
        Destino: <input required type="text" name="destiny"><br>
        Mensaje: <textarea name="message"></textarea><br>
        <button class="submit_button" value="Send Email">Enviar</button>
    </form>
</body>
</html>
"""

html_success="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
    <title>SMTP homemade</title>
</head>
<body>
    <h1>Email enviado!!!</h1>
    <button>Redactar nuevo</button>
</body>
</html>
"""

def send_command(socket, command):
    data = (command + "\r\n").encode()
    socket.send(data)

def receive_response(socket):
    buffer = socket.recv(1024)
    return buffer.decode()

def send_email(server_host, server_port, username, password, subject, destiny, message):
    message_compile = f'Subject: {subject}\r\nFrom: {username}\r\nTo: {destiny}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{message}\r\n.\r\n'
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))
            
            # EHLO command
            send_command(client_socket, "EHLO localhost")
            print("EHLO response:", receive_response(client_socket))
            
            # AUTH LOGIN
            send_command(client_socket, "AUTH LOGIN")
            print("AUTH response:", receive_response(client_socket))
            
            # Send encoded username
            encoded_username = base64.b64encode(username.encode()).decode()
            send_command(client_socket, encoded_username)
            print("Username response:", receive_response(client_socket))
            
            # Send encoded password
            encoded_password = base64.b64encode(password.encode()).decode()
            send_command(client_socket, encoded_password)
            print("Password response:", receive_response(client_socket))
            
            # MAIL FROM command
            send_command(client_socket, f"MAIL FROM:<{username}>")
            print("MAIL FROM response:", receive_response(client_socket))
            
            # RCPT TO command
            send_command(client_socket, f"RCPT TO:<{destiny}>")
            print("RCPT TO response:", receive_response(client_socket))
            
            # DATA command
            send_command(client_socket, "DATA")
            print("DATA response:", receive_response(client_socket))
            
            # Send email content
            send_command(client_socket, message_compile)
            print("Email content response:", receive_response(client_socket))
            
            # End conection
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            
            print("Email sent successfully!")
    except Exception as ex:
        print(f"Error: {ex}")

@app.route('/', methods=['GET', 'POST'])
def send_email_page():
    if request.method == 'POST':
        server_host = request.form.get('server_host', 'localhost')
        server_port = int(request.form.get('server_port', 5000))
        username = request.form['username']
        password = request.form['password']
        subject = request.form['subject']
        destiny = request.form['destiny']
        message = request.form['message']
        send_email(server_host, server_port, username, password, subject, destiny, message)
        return render_template_string(html_success)
    return render_template_string(html_email)

if __name__ == '__main__':
    app.run(debug=True, port=3000)