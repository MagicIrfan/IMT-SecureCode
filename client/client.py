import socket

# Configuration du serveur
TCP_IP = '127.0.0.1'  # Adresse IP du serveur
TCP_PORT = 12345  # Port du serveur


# Fonction pour envoyer une demande au serveur et récupérer la réponse
def send_request(request):
    # Création du socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((TCP_IP, TCP_PORT))

    # Envoi de la demande au serveur
    client_socket.send(request.encode())

    # Réception de la réponse du serveur
    response = client_socket.recv(1024).decode()

    # Fermeture du socket client
    client_socket.close()

    # Retour de la réponse
    return response


if __name__ == '__main__':
    while True:
        print("\n--- Network Clock Client ---")
        print("1. Obtenir l'heure actuelle")
        print("2. Définir la date et l'heure système")
        print("3. Quitter")

        choice = input("Choisissez une option : ")

        if choice == "1":
            format_string = input("Veuillez spécifier le format de l'heure (ex: %Y-%m-%d %H:%M:%S) : ")
            request = f"GET_TIME:{format_string}"
            response = send_request(request)
            print("Heure actuelle :", response)

        elif choice == "2":
            new_time = input("Veuillez entrer la nouvelle date et heure (ex: 2023-07-17 12:34:56) : ")
            request = f"SET_TIME:{new_time}"
            response = send_request(request)
            print(response)

        elif choice == "3":
            break

        else:
            print("Option invalide. Veuillez réessayer.")