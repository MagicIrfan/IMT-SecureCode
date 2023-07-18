import tkinter as tk
from tkinter import messagebox
import socket

# Configuration du serveur
TCP_IP = '127.0.0.1'  # Adresse IP du serveur
TCP_PORT = 12345  # Port du serveur


# Fonction pour envoyer une demande au serveur et récupérer la réponse
def send_request(request):
    try:
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
    except ConnectionRefusedError:
        messagebox.showerror("Erreur de connexion", "Impossible de se connecter au serveur.")
        return None


def get_time():
    format_string = format_entry.get()
    print(format_string)
    if format_string:
        request = f"GET_TIME:{format_string}"
        response = send_request(request)
        print(response)
        if response:
            time_label.config(text="Heure actuelle : " + response)


def set_time():
    new_time = new_time_entry.get()
    if new_time:
        request = f"SET_TIME:{new_time}"
        response = send_request(request)
        print(response)
        if response:
            messagebox.showinfo("Changement d'heure", response)


if __name__ == '__main__':
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Horloge réseau")

    # Création des widgets
    format_label = tk.Label(root, text="Format de l'heure (ex: %Y-%m-%d %H:%M:%S) :")
    format_entry = tk.Entry(root, width=30)
    get_time_button = tk.Button(root, text="Obtenir l'heure actuelle", command=get_time)

    new_time_label = tk.Label(root, text="Nouvelle date et heure (ex: 2023-07-17 12:34:56) :")
    new_time_entry = tk.Entry(root, width=30)
    set_time_button = tk.Button(root, text="Définir la date et l'heure système", command=set_time)

    time_label = tk.Label(root, text="Heure actuelle :")
    time_label.config(font=("Arial", 14, "bold"))

    # Placement des widgets dans la fenêtre
    format_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    format_entry.grid(row=0, column=1, padx=10, pady=5)
    get_time_button.grid(row=0, column=2, padx=10, pady=5)

    new_time_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    new_time_entry.grid(row=1, column=1, padx=10, pady=5)
    set_time_button.grid(row=1, column=2, padx=10, pady=5)

    time_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

    # Boucle principale de la fenêtre
    root.mainloop()
