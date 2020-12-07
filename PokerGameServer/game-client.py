from pygase import Client


class ChaseClient(Client):
    def __init__(self):
        super().__init__()
        self.player_id = None
        # The backend will send a "PLAYER_CREATED" event in response to a "JOIN" event.
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)

    # "PLAYER_CREATED" event handler
    def on_player_created(self, player_id):
        # Remember the id the backend assigned the player.
        self.player_id = player_id


try:
    # Create a client.
    client = ChaseClient()
    client.connect_in_thread(hostname="localhost", port=8080)
    client.register_event_handler("poker_FEEDBACK", print)
    username = input("Player name: ")
    client.dispatch_event("JOIN", username)
    input('press any key to continue')
    client.dispatch_event("poker", username)
except(Exception):
    print(Exception)
    exit()

while True:
    if input() == 'y':
        client.disconnect(shutdown_server=True)
        break
