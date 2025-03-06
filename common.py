class InvalidAction(Exception):
    """Exception levée lorsqu'une action invalide est jouée."""
    def __init__(self, action=None):
        self.action = action

class Player:
    """Interface pour un joueur d'Avalam."""
    def play(self, percepts, max_height, step, time_left):
        """Joue un coup et retourne une action.

        Arguments :
        percepts -- l'état actuel du plateau sous une forme pouvant être utilisée par le constructeur de Board. Le plateau est toujours vu du point de vue où ce joueur est le yellow (les nombres positifs).
        max_height -- la hauteur maximale d'une tour.
        step -- le numéro de l'étape actuelle, en commençant à 1.
        time_left -- un flottant indiquant le nombre de secondes restantes dans le crédit temps pour ce joueur. Si la partie n'est pas limitée en temps, `time_left` vaut None.
        """
        pass

def serve_player(player, address, port):
    """Lance un serveur pour le joueur à l'adresse et au port spécifiés."""
    from xmlrpc.server import SimpleXMLRPCServer
    server = SimpleXMLRPCServer((address, port), allow_none=True)
    server.register_instance(player)
    print(f"Écoute sur {address}:{port}")  # Message traduit en français
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")  # Message pour signaler l'arrêt propre du serveur

def player_main(player, options_cb=None, setup_cb=None):
    """Lance le serveur du joueur en fonction des arguments."""
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option(
        "-b", "--bind",
        dest="address",
        default="",
        help="adresse d'écoute (par défaut : toutes les adresses)"
    )
    parser.add_option(
        "-p", "--port",
        type="int",
        dest="port",
        default=8000,
        help="définir le numéro de port (par défaut : %default)"
    )
    if options_cb is not None:
        options_cb(player, parser)
    
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("Aucun argument nécessaire.")  # Message traduit en français
    if options.port < 1 or options.port > 65535:
        parser.error("Option -p : numéro de port invalide.")  # Message traduit
    if setup_cb is not None:
        setup_cb(player, parser, options)
    
    serve_player(player, options.address, options.port)
