from pygase import Client
import time
import logging


logging.basicConfig(level=logging.ERROR)


class ChaseClient(Client):
    def __init__(self):
        super().__init__()
        self.player_id = None
        self.game_round = None
        self.register_event_handler("PLAYER_CREATED", self.on_player_created)
        self.register_event_handler("POKER", self.handel_poker)
        self.register_event_handler("HOLECARD_FEEDBACK", self.holecard_feedback)
        self.register_event_handler("FLOP_FEEDBACK", self.flop_feedback)

    def on_player_created(self, player_id, game_round):
        # need to remember
        self.player_id = player_id
        self.game_round = game_round
        print('\nid:', self.player_id, 'game_round:', self.game_round)

    def handel_poker(self, msg):
        if msg == 'ready':
            print('GameState refresh, Game Ready Now')
        else:
            pass

    def holecard_feedback(self, msg):
        print('My Hole Card:', msg)

    def flop_feedback(self, msg):
        print('Flop Card:', msg)

    def main(self):
        bet_ins = ['yanglin', '5']
        try:
            username = "yanglin"
            client.dispatch_event("JOIN", username)
            time.sleep(2)
            client.dispatch_event("START", username)
            time.sleep(2)
            client.dispatch_event("HOLECARD", self.player_id, self.game_round)
            time.sleep(2)
            print('Try to bet')
            client.dispatch_event("BET", bet_ins)
            time.sleep(2)
            client.dispatch_event("FLOP", self.player_id, self.game_round)
        except(Exception):
            print(Exception)
            client.disconnect(shutdown_server=True)

        input()
        client.disconnect(shutdown_server=True)


if __name__ == "__main__":
    client = ChaseClient()
    client.connect_in_thread(hostname="localhost", port=8080)
    client.main()
