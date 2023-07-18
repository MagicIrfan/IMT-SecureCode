import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
    format_string = "%Y-%m-%d %H:%M:%S"
    request = f"GET_TIME:{format_string}"
    response = send_request(request)
    if response:
        time_label.config(text="Heure actuelle : " + response)


def set_time():
    year = year_var.get()
    month = month_var.get()
    day = day_var.get()
    hour = hour_var.get()
    minute = minute_var.get()
    second = second_var.get()

    new_time = f"{year}-{month}-{day}-12-12-12"
    request = f"SET_TIME:{new_time}"
    response = send_request(request)
    if response:
        messagebox.showinfo("Changement d'heure", response)


if __name__ == '__main__':
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Horloge réseau")

    # Création des widgets
    year_var = tk.StringVar()
    month_var = tk.StringVar()
    day_var = tk.StringVar()
    hour_var = tk.StringVar()
    minute_var = tk.StringVar()
    second_var = tk.StringVar()

    year_label = tk.Label(root, text="Année :")
    year_entry = ttk.Combobox(root, textvariable=year_var, values=list(range(2000, 2101)))

    month_label = tk.Label(root, text="Mois :")
    month_entry = ttk.Combobox(root, textvariable=month_var, values=list(range(1, 13)))

    day_label = tk.Label(root, text="Jour :")
    day_entry = ttk.Combobox(root, textvariable=day_var, values=list(range(1, 32)))

    hour_label = tk.Label(root, text="Heure :")
    hour_entry = ttk.Combobox(root, textvariable=hour_var, values=list(range(24)))

    minute_label = tk.Label(root, text="Minutes :")
    minute_entry = ttk.Combobox(root, textvariable=minute_var, values=list(range(60)))

    second_label = tk.Label(root, text="Secondes :")
    second_entry = ttk.Combobox(root, textvariable=second_var, values=list(range(60)))

    get_time_button = tk.Button(root, text="Obtenir l'heure actuelle", command=get_time)
    set_time_button = tk.Button(root, text="Définir la date et l'heure système", command=set_time)

    time_label = tk.Label(root, text="Heure actuelle :")
    time_label.config(font=("Arial", 14, "bold"))

    # Placement des widgets dans la fenêtre
    year_label.grid(row=0, column=0, padx=10, pady=5)
    year_entry.grid(row=0, column=1, padx=10, pady=5)

    month_label.grid(row=0, column=2, padx=10, pady=5)
    month_entry.grid(row=0, column=3, padx=10, pady=5)

    day_label.grid(row=0, column=4, padx=10, pady=5)
    day_entry.grid(row=0, column=5, padx=10, pady=5)

    hour_label.grid(row=1, column=0, padx=10, pady=5)
    hour_entry.grid(row=1, column=1, padx=10, pady=5)

    minute_label.grid(row=1, column=2, padx=10, pady=5)
    minute_entry.grid(row=1, column=3, padx=10, pady=5)

    second_label.grid(row=1, column=4, padx=10, pady=5)
    second_entry.grid(row=1, column=5, padx=10, pady=5)

    get_time_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
    set_time_button.grid(row=2, column=3, columnspan=3, padx=10, pady=5)

    time_label.grid(row=3, column=0, columnspan=6, padx=10, pady=5)

    # Boucle principale de la fenêtre
    root.mainloop()
