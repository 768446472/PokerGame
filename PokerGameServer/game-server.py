'''------ Poker Game ------'''
from pygase import GameState, Backend
import random

initial_game_state = GameState(
    players={},
    poker_data={},
    operation={},
    game_round=0,  # define game round
)


# update gamestate
def game_time_step(game_state, dt):
    return {}


def on_start(player_name, game_state, client_address, **kwargs):
    print('into on_start')
    flower = ['\u2660', '\u2663', '\u2665', '\u2666']
    points = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    poker_list = []
    # Generate playing cards
    for i in flower:
        for j in points:
            poker_list.append(i + j)
    # Randomly select hole cards for each user
    hole_card = {}
    for num in range(len(game_state.players)):
        cards = []
        for i in range(2):
            picked_poker = random.choice(poker_list)
            cards.append(picked_poker)
            poker_list.remove(picked_poker)
        hole_card[num] = cards
    public_card = []
    for i in range(5):
        picked_poker = random.choice(poker_list)
        public_card.append(picked_poker)
        poker_list.remove(picked_poker)
    backend.server.dispatch_event("POKER",
                                  "ready",
                                  target_client=client_address)
    print('Shuffle success, public card: %s' % public_card)
    return {
        "poker_data": {
            game_state.game_round: {
                "public_card": public_card,
                "hole_card": hole_card,
            },
        }
    }


# "JOIN" event handler
def on_join(player_name, game_state, client_address, **kwargs):
    player_id = len(game_state.players)
    if player_id <= 5:
        print(f"{player_name} joined.")
        # Notify client that the player successfully joined the game.
        backend.server.dispatch_event("PLAYER_CREATED",
                                      player_id,
                                      game_state.game_round,
                                      target_client=client_address)
        return {
            # Add a new entry to the players dict
            "players": {
                player_id: {
                    "name": player_name,
                }
            }
        }
    else:
        print('user full')
        return {}


def on_holecard(player_id: int, game_round: int, game_state, client_address,
                **kwargs):
    print(game_state.poker_data)
    backend.server.dispatch_event(
        "HOLECARD_FEEDBACK",
        game_state.poker_data[game_round]['hole_card'][player_id],
        target_client=client_address)
    return {}


def on_bet(bet_ins, game_state, client_address, **kwargs):
    print(f"下注情况：{bet_ins}")
    return {
        "operation": {
            game_state.game_round: {
                "bet": {
                    "1": "1"
                }
            },
        },
    }


def on_flop(player_id: int, game_round: int, game_state, client_address,
            **kwargs):
    flop_card = game_state.poker_data[game_round]['public_card'][0:3]
    print("handling flop_card request. sending %s to player %s" %
          (flop_card, player_id))
    backend.server.dispatch_event("FLOP_FEEDBACK",
                                  flop_card,
                                  target_client=client_address)
    return {}


def on_turn(player_id: int, game_round: int, game_state, client_address,
            **kwargs):
    turn_card = game_state.poker_data[game_round]['public_card'][3:4]
    print("handling turn_card request. sending %s to player %s" %
          (turn_card, player_id))
    backend.server.dispatch_event("TURN_FEEDBACK",
                                  turn_card,
                                  target_client=client_address)
    return {}


def on_river(player_id: int, game_round: int, game_state, client_address,
             **kwargs):
    river_card = game_state.poker_data[game_round]['public_card'][4:5]
    print("handling river_card request. sending %sto player %s" %
          (river_card, player_id))
    backend.server.dispatch_event("RIVER_FEEDBACK",
                                  river_card,
                                  target_client=client_address)
    return {}


def on_newround(player_id: int, game_round: int, game_state, client_address,
                **kwargs):
    print("\nnewround start, now round %s player_id:%s client game_round:%s" %
          (game_state.game_round + 1, player_id, game_round))
    return {"game_round": game_state.game_round + 1}


backend = Backend(initial_game_state, game_time_step)
backend.game_state_machine.register_event_handler("JOIN", on_join)
backend.game_state_machine.register_event_handler('START', on_start)
backend.game_state_machine.register_event_handler('HOLECARD', on_holecard)
backend.game_state_machine.register_event_handler('BET', on_bet)
backend.game_state_machine.register_event_handler('FLOP', on_flop)
backend.game_state_machine.register_event_handler('TURN', on_turn)
backend.game_state_machine.register_event_handler('RIVER', on_river)
backend.game_state_machine.register_event_handler('NEWROUND', on_newround)
backend.run('localhost', 8080)
