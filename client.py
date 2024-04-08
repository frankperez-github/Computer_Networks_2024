import socket


def main():
    askForData()
    
def askForData():
    #Ask for user and password
    try:
        # Config SMTP server details (smtp4dev)
        server_host = "localhost"  # Change to smtp4dev location
        server_port = 5000
        username = input('Introduce tu correo:\n')
        password = input('Introduce tu contraseña:\n')
        subject = input('Introduce el asunto:\n')
        destiny = input('A qué dirección desea enviar el correo?\n')
        message = input('Introduce el mensaje:\n')
        message_complile = 'Subject: ' + subject + """\r\n
            From:""" + username + """\r\n
            To: """ + destiny + '\r\n' + """
            Content-Type: text/plain; charset=utf-8\r\n
            \r\n
            """ + message + """\r\n
            \r\n.\r\n"""
        
        # Set conection to server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_host, server_port))
            
            # Initial server response
            response = receive_response(client_socket)
            print("Respuesta del servidor:", response)

            # Command EHLO to start conversation
            send_command(client_socket, "EHLO localhost")

            # Get response from server
            response = receive_response(client_socket)
            print("Respuesta del servidor:", response)

            # Authentication
            auth_command = "AUTH LOGIN\r\n"
            client_socket.send(auth_command.encode())
            response = receive_response(client_socket)
            print("Respuesta del servidor:", response)

            # Send username (codified)
            encoded_username = base64.b64encode(username.encode()).decode()
            client_socket.send(encoded_username.encode() + b"\r\n")
            response = receive_response(client_socket)
            print("Respuesta del servidor:", response)

            # Send password (codified)
            encoded_password = base64.b64encode(password.encode()).decode()
            client_socket.send(encoded_password.encode() + b"\r\n")
            response = receive_response(client_socket)
            print("Respuesta del servidor:", response)

            

    except Exception as ex:
        print("Error:", ex)

def send_command(socket, command):
    data = (command + "\r\n").encode()
    socket.send(data)

def receive_response(socket):
    buffer = socket.recv(1024)
    return buffer.decode()


