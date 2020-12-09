"""
Solitaire clone.
"""
import arcade
import random
import arcade.gui
from arcade.gui import UIManager

# Constants for users
USER_LIST = ['MR.J', 'MR.Z', 'MR.L', 'MR.Y']
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_blue4.png"
# Constants for sizing
CARD_SCALE = 0.6
# How big are the cards?
CARD_WIDTH = 320 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE
# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)
BUTTOM_MAT_WIDTH = int((CARD_WIDTH / 2) * MAT_PERCENT_OVERSIZE)
# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10
# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
# Card constants
CARD_VALUES = [
    "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]
# define pile
BOTTOM_FACE_DOWN_PILE = 0
PLAY_PILE_1 = 1
PLAY_PILE_2 = 2
PLAY_PILE_3 = 3
PLAY_PILE_4 = 4
PILE_COUNT = 5


class TextButton:
    """ Text-based button """

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Arial",
                 face_color=arcade.color.LIGHT_GRAY,
                 highlight_color=arcade.color.WHITE,
                 shadow_color=arcade.color.GRAY,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
                                     self.height, self.face_color)

        if not self.pressed:
            color = self.shadow_color
        else:
            color = self.highlight_color

        # Bottom horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y - self.height / 2,
                         color, self.button_height)

        # Right vertical
        arcade.draw_line(self.center_x + self.width / 2, self.center_y - self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        if not self.pressed:
            color = self.highlight_color
        else:
            color = self.shadow_color

        # Top horizontal
        arcade.draw_line(self.center_x - self.width / 2, self.center_y + self.height / 2,
                         self.center_x + self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        # Left vertical
        arcade.draw_line(self.center_x - self.width / 2, self.center_y - self.height / 2,
                         self.center_x - self.width / 2, self.center_y + self.height / 2,
                         color, self.button_height)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(_x, _y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class StartTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(330, 180, 100, 40, "Start", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class StopTextButton(TextButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(330, 130, 100, 40, "Stop", 18, "Arial")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


class Card(arcade.Sprite):
    """ Card sprite """
    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False
        super().__init__(FACE_DOWN_IMAGE, scale)

    def face_down(self):
        """ Turn card face-down """
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        """ Turn card face-up """
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    @property
    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up


class MyGame(arcade.View):
    """ Main application class. """
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.AMAZON)
        self.card_list = None
        self.player_text = None
        self.held_cards_original_position = None
        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None
        # List of cards we are dragging with the mouse
        self.piles = None
        self.held_cards = None
        self.TOP_Y = self.window.height - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
        self.MIDDLE_Y = self.TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
        self.ui_manager = UIManager()
        self.pause = False
        self.button_list = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # List of cards we are dragging with the mouse
        self.ui_manager.purge_ui_elements()
        self.held_cards = []
        self.held_cards_original_position = []
        self.view_bottom = 0
        self.view_left = 0
        self.view_right = 0

        # Create our on-screen GUI buttons
        self.button_list = []
        # define button
        play_button = StartTextButton(60, 570, self.resume_program)
        self.button_list.append(play_button)
        quit_button = StopTextButton(60, 515, self.pause_program)
        self.button_list.append(quit_button)

        # create the mats, the cards go on
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()
        # Create the mats for the bottom face down and face up piles
        hole_pile = arcade.SpriteSolidColor(BUTTOM_MAT_WIDTH, MAT_HEIGHT,
                                            arcade.csscolor.DARK_OLIVE_GREEN)
        hole_pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(hole_pile)
        # Create My seat
        my_steat = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT,
                                           arcade.csscolor.DARK_OLIVE_GREEN)
        my_steat.position = START_X + X_SPACING * 2, BOTTOM_Y
        self.pile_mat_list.append(my_steat)
        # Create the other users middle piles and usernames
        for i in range(len(USER_LIST) - 1):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT,
                                           arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, self.TOP_Y
            self.pile_mat_list.append(pile)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()
        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)
        # Shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list[pos1], self.card_list[pos2] = self.card_list[
                pos2], self.card_list[pos1]

        # Create a list of lists, each holds a pile of cards.
        self.piles = [[] for _ in range(PILE_COUNT)]
        # Put all the cards in the bottom face-down pile
        for card in self.card_list:
            self.piles[BOTTOM_FACE_DOWN_PILE].append(card)
        # - Pull from that pile into the middle piles, all face-down
        # Loop for each pile
        for pile_no in range(PLAY_PILE_1, PLAY_PILE_4 + 1):
            for i in range(2):
                # Pop the card off the deck we are dealing from
                card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
                # Put in the proper pile
                self.piles[pile_no].append(card)
                # Move card to same position as pile we just put it in
                temp_position = [
                    self.pile_mat_list[pile_no].position[0],
                    self.pile_mat_list[pile_no].position[1]
                ]
                print(i)
                if i == 0:
                    temp_position[0] = temp_position[0] - 45
                    print(temp_position[0] - 30)
                else:
                    temp_position[0] = temp_position[0] + 45
                    print(temp_position[0] + 30)
                card.position = temp_position
                # Put on top in draw order
                self.pull_to_top(card)
        for public_card_no in range(5):
            # Pop the card off the deck we are dealing from
            card = self.piles[BOTTOM_FACE_DOWN_PILE].pop()
            temp_position = [
                self.window.width // 2 - 200, self.window.height // 2
            ]
            temp_position[0] = temp_position[0] + 90 * public_card_no
            print(public_card_no, temp_position)
            card.position = temp_position
            # Put on top in draw order
            self.pull_to_top(card)

    def send_hole_cards(self):
        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((START_X, BOTTOM_Y),
                                            self.card_list)
        primary_card = cards[-1]
        picked_card = [primary_card]
        # If we are holding cards, move them with the mouse
        for card in picked_card:
            card.center_x += 50
            card.center_y += 50

    def on_show_view(self):
        """ Called once when view is activated. """
        self.setup()

    def on_hide_view(self):
        self.ui_manager.unregister_handlers()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        arcade.start_render()
        # Draw the mats the cards go on to
        self.pile_mat_list.draw()
        # Draw the cards
        self.card_list.draw()
        # Draw the buttons
        for button in self.button_list:
            button.draw()
        # Draw the player's name
        arcade.draw_text("Hole\ncards", 10 + self.view_left,
                         10 + self.view_bottom, arcade.csscolor.WHITE, 18)
        arcade.draw_text("My\nSeat", 3 * self.window.width // 5,
                         10 + self.view_bottom, arcade.csscolor.WHITE, 18)
        for i in range(len(USER_LIST) - 1):
            arcade.draw_text(USER_LIST[i], START_X + i * X_SPACING - 20,
                             self.TOP_Y - 110, arcade.csscolor.WHITE, 18)

    def pull_to_top(self, card):
        """ Pull card to top of rendering order (last to render, looks on-top) """
        # Find the index of the card
        index = self.card_list.index(card)
        # Loop and pull all the other cards down towards the zero end
        for i in range(index, len(self.card_list) - 1):
            self.card_list[i] = self.card_list[i + 1]
        # Put this card at the right-side/top/size of list
        self.card_list[len(self.card_list) - 1] = card

    def on_mouse_press(self, x, y, button, key_modifiers):
        print(f"location: ({x}, {y})")
        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)
        if len(cards) > 0:
            # Might be a stack of cards, get the top one
            primary_card = cards[-1]
            if primary_card.is_face_down:
                # Is the card face down? In one of those middle 7 piles? Then flip up
                primary_card.face_up()
            else:
                primary_card.face_down()
                # All other cases, grab the face-up card we are clicking on
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [
                    self.held_cards[0].position
                ]
                # Put on top in drawing order
                self.pull_to_top(self.held_cards[0])
        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        check_mouse_release_for_buttons(x, y, self.button_list)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        pass

    def pause_program(self):
        print('pause')
        # self.pause = True

    def resume_program(self):
        print('resume')
        # self.pause = False


def main():
    """ Main method """
    window = arcade.Window(title="Texas Hold'em of NT Foursome")
    view = MyGame()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
