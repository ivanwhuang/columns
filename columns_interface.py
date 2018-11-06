# Ivan Wan Le Huang 60062626
import columns_logic
import random

COLORS = ['A', 'B', 'C', 'D', 'E']
SIZEOFFALLER = 3 

class ColumnsGame():
    def __init__(self):
        self._running = True
        self._game_field = None
        self._game_faller = None

    def quit_game(self) -> None:
        '''
        Sets the class's _running variable to False
        '''
        self._running = False

    def running(self) -> bool:
        '''
        Get's the current running state of the game
        '''
        return self._running

    def game_field(self) -> columns_logic.Field:
        "Gets the current game field"
        return self._game_field

    def game_faller(self) -> columns_logic.Faller:
        "Gets the current game faller"
        return self._game_faller

    def run(self) -> None:
        "Starts the game and continues to play the game until _running is false"
        self.set_up_field()
        while self._running == True:
            self.initial_faller_setup()
            if self.running() == False:
                break
            self.play_game()

    def play_game(self) -> None:
        '''
        This function handles the flow of the game and
        determines whether the game ends based on user inputs"
        '''
        try:
            while self._game_faller.state() != "DEAD" \
            and columns_logic.is_game_over(self.game_faller(), self.game_field()) == False:
                user_input = input().strip()
                if user_input == 'Q':
                    self.quit_game()
                    break
                self.handle_commands(self._game_faller, user_input)
            self._game_faller = None
        except columns_logic.GameOverError:
            print("GAME OVER")
            self.quit_game()

    def set_up_field(self) -> None:
        '''
        This function sets up the size of the field and creates the field for our game
        '''
        field_rows = int(input("# of ROWS for Game Board: "))
        field_columns = int(input("# of COLUMNS for Game Board: "))
        empty_field = columns_logic.new_game_field(field_rows, field_columns)
        self._game_field = empty_field
        self.display_board() 

    def initial_faller_setup(self) -> None:
        '''
        This function creates a random faller and positions it in a random column. 
        If the specified column has a filled cell at the top row, then the game ends.
        '''

        new_faller = 'F'

        rand_col = random.randint(1, self._game_field.num_cols())
        new_faller = new_faller + " " + str(rand_col)

        for x in range(SIZEOFFALLER):
            new_color = COLORS[random.randint(0, len(COLORS) - 1)]
            new_faller = new_faller + " " + new_color

        print(new_faller)

        try:
            self._game_faller = columns_logic.create_faller(new_faller)
            if self.game_field().can_place_faller(self.game_faller()) == True:
                self.game_field().position_faller(self.game_faller())

        except columns_logic.GameOverError:
            print("GAME OVER")
        except columns_logic.InvalidMoveError:
            pass
        finally:
            self.display_board()


    def display_board(self) -> None:
        '''
        This function displays the current state of the game field
        '''
        
        for cell_row in self._game_field.board():
            cell_str = '|'
            for cell in cell_row:
                if cell.status() == 'EMPTY':
                    cell_str += '   '
                if cell.status() == 'FALLER':
                    cell_str += '[' + cell.color() + ']'
                if cell.status() == 'FROZEN':
                    cell_str += ' ' + cell.color() + ' '
                if cell.status() == 'LANDED':
                    cell_str += '|' + cell.color() + '|'
                if cell.status() == 'MATCH':
                    cell_str += '*' + cell.color() + '*'
            print(cell_str, end='|')
            print('')

        bottom = ' '
        for num in range(self._game_field.num_cols()):
            bottom += '---'
        print(bottom, end=' ')
        print('')

    def handle_commands(self, current_faller: columns_logic.Faller, command: str) -> None:
        '''
        This function is the main event handler for the game. It takes in a command
        given by the user and changes the state of the faller based on command. If no
        specific command is given, then the faller drops, representing crude time.
        '''

        try:
            if len(command) >= 1 and current_faller.state() != 'LANDED':

                if command == "Q":
                    self.quit_game()

                if command == 'R':
                    current_faller.rotate_faller()

                if command == '<':
                    self._game_field.clear_faller(current_faller)
                    self._game_field.shift_faller(current_faller, '<')

                if command == '>':
                    self._game_field.clear_faller(current_faller)
                    self._game_field.shift_faller(current_faller, '>')

                self.game_field().position_faller(current_faller)

            elif command == '':
                self._game_field.pass_time(current_faller)

        except columns_logic.GameOverError:
            print("GAME OVER")
        finally:
            self.display_board()


if __name__ == '__main__':
    new_game = ColumnsGame()
    new_game.run()
