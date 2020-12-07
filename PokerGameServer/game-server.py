from pygase import GameState, Backend
import random

# Let there be an imaginary enemy at position 0 with 100 health points.
initial_game_state = GameState(
    players={},
    chaser_id=None,  # id of player who is chaser
    protection=None,  # wether protection from the chaser is active
    countdown=0.0,  # countdown until protection is lifted
)


def poker(player_name, game_state, client_address, **kwargs):
    flower = ['\u2660', '\u2663', '\u2665', '\u2666']
    points = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    poker_list = []
    # Generate playing cards
    for i in flower:
        for j in points:
            poker_list.append(i + j)
    # Randomly select hole cards for each user
    for num in range(len(game_state.players)):
        cards = []
        for i in range(2):
            picked_poker = random.choice(poker_list)
            cards.append(picked_poker)
            poker_list.remove(picked_poker)
        game_state.players[num]['hole_cards'] = cards
    print(game_state.players)
    # Feedback to client
    backend.server.dispatch_event(
        'poker_FEEDBACK',
        f"hole card: {game_state.players[game_state.chaser_id]['hole_cards']}",
        target_client=client_address)
    return {}


def game_time_step(game_state, dt):
    return {}


# "JOIN" event handler
def on_join(player_name, game_state, client_address, **kwargs):
    print(f"{player_name} joined. player list {game_state.players}")
    player_id = len(game_state.players)
    # Notify client that the player successfully joined the game.
    backend.server.dispatch_event("PLAYER_CREATED",
                                  player_id,
                                  target_client=client_address)
    return {
        # Add a new entry to the players dict
        "players": {
            player_id: {
                "name": player_name,
                "hole_cards": ''
            }
        },
        # If this is the first player to join, make it the chaser.
        "chaser_id":
        player_id if game_state.chaser_id is None else game_state.chaser_id,
    }


def bet(player_name, game_state, client_address, **kwargs):
    pass


backend = Backend(initial_game_state, game_time_step)
# Register the "JOIN" handler.
backend.game_state_machine.register_event_handler("JOIN", on_join)
backend.game_state_machine.register_event_handler("poker", poker)
backend.run('localhost', 8080)
