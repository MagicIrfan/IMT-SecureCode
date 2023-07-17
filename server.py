import socketserver
from NetworkClockRequestHandler import NetworkClockRequestHandler

if __name__ == '__main__':
    # Configuration du port d'écoute
    TCP_IP = '127.0.0.1'  # Adresse IP locale
    TCP_PORT = 12345  # Port d'écoute

    # Création du serveur
    server = socketserver.TCPServer((TCP_IP, TCP_PORT), NetworkClockRequestHandler)

    print("Network Clock application is running.")

    # Démarrage du serveur
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.shutdown()
    server.server_close()