# Ivan Wan Le Huang 60062626

class Cell:
    def __init__(self, color: str, status: str, row: int, col: int):
        self._color = color
        self._status = status
        self._row = row
        self._col = col

    def color(self) -> str:
        '''
        Returns the current color of the cell.
        '''
        return self._color

    def status(self) -> str:
        '''
        Returns the current status of the cell.
        '''
        return self._status

    def row(self) -> int:
        '''
        Returns the current row index of the cell.
        '''
        return self._row

    def col(self) -> int:
        '''
        Returns the current column index of the cell.
        '''
        return self._col

    def is_on_board(self) -> bool:
        '''
        This function returns False if the cell's index is negative.
        '''
        if self.row() >= 0:
            return True
        else:
            return False

    def change_color(self, new_color: str) -> None :
        '''
        This function takes a string and changes the cell's color
        to that string.
        '''
        self._color = new_color

    def move_left(self) -> None:
        '''
        Subtracts the cell's column index by 1.
        '''
        self._col -= 1

    def move_right(self) -> None:
        '''
        Increases the cell's column index by 1.
        '''
        self._col += 1

    def drop(self) -> None:
        '''
        Adds 1 to the cell's row index.
        '''
        self._row += 1

    def clear(self) -> None:
        '''
        Changes the cell's color to a blank space and changes
        it's status to 'EMPTY'
        '''
        self._color = " "
        self._status = "EMPTY"

    def match(self) -> None:
        '''
        Changes the cell's status to 'MATCH'
        '''
        self._status = "MATCH"

    def land(self) -> None:
        '''
        Changes the cell's status to 'LANDED'
        '''
        self._status = "LANDED"

    def freeze(self) -> None:
        '''
        Changes the cell's status to 'FROZEN'
        '''
        self._status= "FROZEN"

class Faller:
    def __init__(self, faller_info: list):
        self._col = self.set_faller_col(faller_info[0])
        self._cell_list = self._create_new_faller_cells(faller_info[1:])
        self._top_jewel = self._cell_list[0]
        self._mid_jewel = self._cell_list[1]
        self._bottom_jewel = self._cell_list[-1]
        self._state = "LANDING"

    def col(self) -> int:
        '''
        Returns the current column index of the Faller
        '''
        return self._col

    def cell_list(self) -> [Cell]:
        '''
        Return the cell list that the Faller contains
        '''
        return self._cell_list

    def state(self) -> str:
        '''
        Returns the current state of the faller.
        '''
        return self._state

    def top_jewel(self) -> Cell:
        '''
        Returns the current cell at the top of the faller.
        '''
        return self._top_jewel

    def mid_jewel(self) -> Cell:
        '''
        Returns the current cell in the middle of the faller.
        '''
        return self._mid_jewel

    def bottom_jewel(self) -> Cell:
        '''
        Returns the current cell at the bottom of the faller.
        '''
        return self._bottom_jewel

    def end_life(self) -> None:
        '''
        Changes the current state of the Faller to 'DEAD'.
        '''
        self._state = "DEAD"

    def set_faller_col(self, desired_faller_col: str) -> int:
        '''
        Sets the specific column that the faller should initially be
        If improper input given by user, an exception is raised.
        '''
        try:
            faller_col = int(desired_faller_col) - 1
            return faller_col
        except:
            raise InvalidMoveError

    def _create_new_faller_cells(self, faller_cells: str) -> list:
        '''
        Takes input as an argument and returns a list of desired Cells to be
        stored into a Faller.
        '''
        cell_list = []
        # Maybe change to -2 later?
        row_counter = -2
        for cell in faller_cells:
            new_cell = Cell(cell, "FALLER", row_counter, self._col)
            row_counter += 1
            cell_list.append(new_cell)
        if len(cell_list) != 3:
            raise InvalidMoveError
        return cell_list

    def rotate_faller(self) -> None:
        '''
        Rotates all the cells in the Faller. The Bottom cell becomes the
        new top cell and the other two shifts up two row indexes.
        '''

        old_faller_cells_color = []
        old_faller_cells_color.append(self.bottom_jewel().color())
        old_faller_cells_color.append(self.top_jewel().color())
        old_faller_cells_color.append(self.mid_jewel().color())

        counter = 0
        for cell in self.cell_list():
            new_color = old_faller_cells_color[counter]
            cell.change_color(new_color)
            counter += 1

    def shift_left(self) -> None:
        '''
        Subtracts the column index of the faller and all of its' cells by 1
        '''
        self._col -= 1
        for cell in self.cell_list():
            cell.move_left()

    def shift_right(self) -> None:
        '''
        Increases the column index of the faller and of its' cells by 1
        '''
        self._col += 1
        for cell in self.cell_list():
            cell.move_right()

    def drop(self) -> None:
        '''
        Increases the row index of all of the faller's cells by 1.
        '''
        for cell in self.cell_list():
            cell.drop()

    def land(self) -> None:
        '''
        Changes the state of the Faller and all of it's Cells to 'LANDED'
        '''
        self._state = "LANDED"
        for cell in self.cell_list():
            cell.land()

    def freeze(self) -> None:
        '''
        Changes the status of all of the Faller's Cells to 'FROZEN'
        '''
        for cell in self.cell_list():
            cell.freeze()

class Field:
    def __init__(self, num_rows: int, num_cols: int, board: [[str]] ):
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._board = board
        self._found_matches = False

    def num_rows(self) -> int:
        '''
        Returns the number of rows in the field.
        '''
        return self._num_rows

    def num_cols(self) -> int:
        '''
        Returns the number of columns in the field.
        '''
        return self._num_cols

    def board(self) -> [[Cell]]:
        '''
        Returns the two dimensional list of Cells that represents the field
        '''
        return self._board

    def found_matches(self) -> bool:
        '''
        Returns a boolean representing whether there are
        any matches in the field
        '''
        return self._found_matches

    def set_matches_found(self, truFalse: bool) -> None:
        '''
        sets private variable '_matches_found' to a specified boolean
        '''
        self._found_matches = truFalse

    def get_cell(self, row: int, col: int) -> Cell:
        '''
        Returns the Cell located at the specified indexes of the Field.
        '''
        return self._board[row][col]

    def can_place_faller(self, faller: Faller) -> bool:

        '''
        Returns True if the Faller could be placed at the very top of field.
        If not, an exception is raised.
        '''
        if self.get_cell(0, faller.col()).status() != 'EMPTY':
            raise GameOverError
        else:
            return True

    def position_faller(self, faller: Faller) -> None:

        '''
        Takes each Cell from a Faller and makes new Cells on the Field.
        '''
        for cell in faller.cell_list():
            self.position_cell(cell)

    def shift_faller(self, faller: Faller, direction: str) -> None:

        '''
        Given a direction specified by the user, if possible, A Faller and all of
        its cells will shift by 1 index towards that direction.
        '''

        if is_faller_in_contact(faller, self, direction) == False:
            if direction == '<':
                if is_valid_col_number(faller.col() - 1, self) == True:
                    faller.shift_left()

            elif direction == '>':
                if is_valid_col_number(faller.col() + 1, self) == True:
                    faller.shift_right()
            # else:
            #     raise InvalidMoveError

    def clear_faller(self, faller: Faller) -> None:
        '''
        Takes the positions of each cell from a Faller and makes new
        EMPTY Cells onto the Field
        '''
        for cell in faller.cell_list():
            if cell.is_on_board():
                new_cell = Cell(' ', 'EMPTY', cell.row(), cell.col())
                self._board[cell.row()][cell.col()] = new_cell

    def position_cell(self, cell: Cell) -> None:

        '''
        Takes the row index and and column index of a cell and
        creates a copy of that cell in the respective indexes on the Field.
        '''
        if cell.is_on_board():
            self._board[cell.row()][cell.col()] = cell

    def pass_time(self, faller: Faller) -> None:

        '''
        Depending on the state of the faller and its cells,
        This function represents the passing of time and determines
        whether a Faller will simply drop or the Field will attempt to
        Find matches.
        '''

        while self.found_matches() == True:
            self.clear_matches()
            self.drop_air_cells()
            if self.find_matches() == True:
                self._found_matches = True
            else:
                self._found_matches = False
                faller.end_life()

        if faller.state() == "LANDED":
            faller.freeze()
            if self.find_matches() == True:
                self._found_matches = True
            else:
                faller.end_life()

        elif can_drop(faller.bottom_jewel(), self) == True:
            self.clear_faller(faller)
            faller.drop()
            self.position_faller(faller)
        else:
            if faller.state() != "DEAD":
                faller.land()

    def find_matches(self) -> bool:
        '''
        This function takes each Cell on the Field and returns True
        if any matches are found on the board.
        '''
        found_matches = False
        for cell_row in self.board():
            for cell in cell_row:
                 if check_for_matches(cell, self) == True:
                     found_matches = True
        return found_matches

    def clear_matches(self) -> None:
        '''
        If there are any matches on the board, the function replaces
        each MATCHED Cell with new EMPTY ones.
        '''
        for cell_row in self.board():
            for cell in cell_row:
                if cell.status() == "MATCH":
                    cell.clear()

    def drop_air_cells(self) -> None:
        '''
        If there are any Filled Cells that are suspended in the air
        after a matching sequence, this function continues to drop suspended Cells
        until each cell has landed on top of another cell or is on the bottom
        of the Field.
        '''
        while self._has_air_cells() == True:
            for cell_row in self.board():
                for cell in cell_row:
                    if cell.status() == "FROZEN" and can_drop(cell, self) == True:
                        new_cell = Cell(" ", "EMPTY", cell.row(), cell.col())
                        self.position_cell(new_cell)
                        cell.drop()
                        self.position_cell(cell)

    def _has_air_cells(self) -> bool:
        '''
        This function checks to see if there are any suspended Cells
        in the Field and returns True if there are. Returns False otherwise.
        '''
        for cell_row in self.board():
            for cell in cell_row:
                if cell.status() == "FROZEN" and can_drop(cell, self) == True:

                    return True
        return False

class GameOverError(Exception):
    '''
    Raised when the game is over.
    '''
    pass

class InvalidMoveError(Exception):
    '''
    Raised whenever an invalid move is made.
    '''
    pass

def create_faller(user_input: str) -> Faller:
    '''
    Given input by the user, this function takes the input and creates
    the desired Faller.
    '''

    faller_input = user_input[2:]
    faller_information = []
    desired_col = ''
    counter = 0

    while counter < len(faller_input):
        if faller_input[counter] != ' ':
            desired_col += faller_input[counter]
            counter += 1
        else:
            break
    faller_information.append(desired_col)

    for info in faller_input[counter + 1:]:
        if info != ' ':
            faller_information.append(info)


    new_faller = Faller(faller_information)
    return new_faller

def shift_faller(faller: Faller, field: Field, direction: str) -> None:
    '''
    This function checks to see if the Faller is surrounded by neighboring
    nonEMPTY Cells and will move them in a given direction if it
    is possible
    '''
    if is_faller_in_contact(faller, field, direction) == False:
        if direction == '<':
            if is_valid_col_number(faller.col() - 1, field) == True:
                faller.shift_left()

        elif direction == '>':
            if is_valid_col_number(faller.col() + 1, field) == True:
                faller.shift_right()
        else:
            raise InvalidMoveError

def is_game_over(faller: Faller, field: Field) -> bool:
    '''
    This function returns True if the game is over while game is running.
    The game is over if each Cell on a Faller has landed and if at least
    one of it's Cells has a negative row index.
    '''
    for cell in faller.cell_list():
        if cell.status() == "LANDED" and cell.is_on_board() == False:
                raise GameOverError
    return False

def can_drop(cell: Cell, field: Field) -> bool:
    '''
    This function determines whether a Cell can drop by returning
     true if there is a nonEMPTY Cell beneath a specified Cell.
    '''
    bottom_row_index = field.num_rows() - 1
    if cell.row() < bottom_row_index:
        if field.get_cell(cell.row() + 1, cell.col()).status() == 'EMPTY':
            return True
    else:
        return False

def is_faller_in_contact(faller:Faller, field: Field, direction: str) -> bool:

    '''
    This function checks if the faller is in contact with any non_empty
    cell objects or has reached the bottom of the field
    '''

    if faller.col() == 0:
        for cell in faller.cell_list():
            if cell.is_on_board() == True:

                if field.get_cell(cell.row(), cell.col() + 1).status() == "FROZEN":
                    return True

    elif faller.col() == field.num_cols() - 1:
        for cell in faller.cell_list():
            if cell.is_on_board() == True:
                if field.get_cell(cell.row(), cell.col() - 1).status() == "FROZEN":
                    return True
    else:
        for cell in faller.cell_list():
            if cell.is_on_board() == True:
                if direction == '<':
                    if field.get_cell(cell.row(), cell.col() - 1).status() == "FROZEN":
                        return True
                if direction == '>':
                    if field.get_cell(cell.row(),cell.col() + 1).status() == "FROZEN":
                        return True
    return False

def is_valid_row_number(new_row: int, field: Field) -> bool:
    '''
    This function returns True if a given row number is valid.
    '''
    if new_row < 0 or new_row >= field.num_rows():
        return False
    else:
        return True

def is_valid_col_number(new_col: int, field: Field) -> bool:
    '''
     This function returns True if a given column number is valid.
    '''
    if new_col < 0 or new_col >= field.num_cols() :
        return False
    else:
        return True

def check_for_matches(cell, field) -> bool:
    '''
    Returns True if a matching sequence of pieces appears on the board
    beginning in the given column and row and extending in any of the
    eight possible directions; returns False otherwise
    '''

    there_is_a_match = False

    if search_and_match(cell,field, 0, 1) == True:
        there_is_a_match = True

    if search_and_match(cell,field, 0, -1) == True:
        there_is_a_match = True

    if search_and_match(cell, field, 1, 0) == True:
        there_is_a_match = True

    if search_and_match(cell, field, -1, 0) == True:
        there_is_a_match = True

    if search_and_match(cell, field, 1, 1) == True:
        there_is_a_match = True

    if search_and_match(cell, field, 1, -1) == True:
        there_is_a_match = True

    if search_and_match(cell, field, -1, -1) == True:
        there_is_a_match = True

    if search_and_match(cell, field, -1, 1) == True:
        there_is_a_match = True

    return there_is_a_match

def search_and_match(cell: Cell, field: Field, row_increment, col_increment) -> bool:
    '''
    Given a cell, this function returns True if there are any valid diagonal
    matches that can be made with the Cell.
    '''
    if cell.status() == "EMPTY":
        return False

    counter = 0
    next_cell_row = cell.row() + row_increment
    next_cell_col = cell.col() + col_increment
    while True:
        if is_valid_col_number(next_cell_col, field) == True\
            and is_valid_row_number(next_cell_row, field) == True:
            if field.get_cell(next_cell_row, next_cell_col).status() != "EMPTY" \
                    and field.get_cell(next_cell_row, next_cell_col).color() == cell.color():

                counter += 1
                next_cell_row += row_increment
                next_cell_col += col_increment
            else:
                break
        else:
            break
    if counter >= 2:
        for num in range(counter + 1):
            field.board()[cell.row() + row_increment * num][cell.col() + col_increment * num].match()
        return True
    else:
        return False

def new_game_field(row_size: int, col_size: int) -> Field:
    '''
    Given a specified row size and column size, this function creates
    a new field of Empty Cells
    '''
    empty_field = []
    for row in range(row_size):
        empty_field.append([])
        for col in range(col_size):
            new_cell = Cell(' ', 'EMPTY', row, col)
            empty_field[-1].append(new_cell)

    field = Field(row_size, col_size, empty_field)
    return field


# def new_content_field(content_list: list) -> Field:
#     '''
#     This function takes a pre specified list of colors for each desired cell
#     and creates a Content Field with these cells.
#     '''
#     content_field = []

#     col_counter = 0
#     for row in range(len(content_list)):
#         content_field.append([])
#         cell_counter = 0
#         cell_list = content_list[col_counter][0]
#         for cell_color in cell_list:
#             if cell_color == ' ':
#                 new_cell = Cell(cell_color, 'EMPTY', row, cell_counter)
#             else:
#                 new_cell = Cell(cell_color, 'FROZEN', row, cell_counter)

#             content_field[-1].append(new_cell)
#             cell_counter += 1
#         col_counter += 1

#     field = Field(len(content_field), len(content_field[0]), content_field)
#     return field
