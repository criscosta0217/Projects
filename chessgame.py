a function is defined with a def, a name, parentheses for parameters and a colon. 
I test whether something is a function as an example callable(thing) returns True if it can be called like a function

parameters are defined inside the parantheses 

Lists: are an ordered collection accessed by index and have square brackets []


Dictionary: are key/value pairs accessed by key and have curly braces {}

Pseudocode are plain english steps that describe the logic without the exact code syntax 

I debugged the program by adding temporary prints where I printed the parsed input and printed the attacked squares & also wrote test scenarios to check for more than one piece in the same square, done after first black piece, etc

I made a small change in the pawn logic from ny = y + 1 (line 368)
to 
ny = y - 1

and that would make the white pawn capture "downwards" instead of upwards (opposite direction to what I implemented)s


why convert squares to coordinates instead of working directly with strings: I guess movement rules are easier to express numerically. As an example a rook moves becomes "add or subtract 1 from x or y" instead of working with character arithmetic. Working with numbers internally keeps the logic simpler and less margin for errors. 

Bugs could easily appear with pawn direction, I assumed white pawns move toward which increases rank.

whats the worst case performance of this program? The scale is small with at most one white piece and sixteen black pieces, even the most expensive operation, calculating attacked squares, runs over a fixed 8x8 board so performance is constant.

what would break if we removed parse_input_line and put that logic inline? 
Functionally the program would still work but we not have consistency and readability. 
the parsing logic is used in both get_white_piece and get_black_pieces. Without a shared function, the same logic would be duplicated, which makes bugs more likely and changes harder to maintain. It would also make the input functions easier to read because they focus on validation rules rather than string manipulation.

Why did you choose dictionaries for pieces instead of classes: At this stage I chose dictionaries because the data structure is very simple







"""
Chess Capture Checker (Console program)

Goal:
- The user enters 1 WHITE chess piece + position.
- The user enters 1 to 16 BLACK chess pieces + positions.
- The program prints which black pieces the white piece can capture immediately.

Input format:
    "<piece> <square>"
Examples:
    "rook a1"
    "pawn d6"

Stop adding black pieces:
    type "done" (only allowed after at least 1 black piece)
"""

# ----------------------------
# 1) SETTINGS & RULES OF THE GAME 

# ----------------------------
# Used CONSTANTS as written in CAPITAL LETTERS AND AT THE TOP 
# "Treat these values as fixed rules - do not change them during the program"

# Requirement: white piece must be one of TWO predefined piece types.
ALLOWED_WHITE_PIECES = ["pawn", "rook"] # stored as a List so can check if piece in ALLOWED_WHITE_PIECES

# Allow black pieces to be any standard chess piece type.
VALID_PIECES = ["pawn", "rook", "knight", "bishop", "queen", "king"] # again stored as a List so can validate input quickly

# FILES = board columns in chess ( a to h). Used a string to make indexing (position) easy.
# Example: FILES.index("a") -> 0, FILES.index("h") -> 7
FILES = "abcdefgh"

# RANKS = Board rows in chess (1 to 8). Also a string for easy indexing. 
# Example: RANKS.index("1") -> 0, RANKS.index("8") -> 7
RANKS = "12345678"


# ----------------------------
# 2) SMALL HELPER FUNCTIONS
# These helper functions do "small jobs" so the main logic stays easy to read, kept functions short for this purpose
# ----------------------------

def is_valid_square(square):
    """Check the square is on the board: a1 -> h8"""
    # Must be exactly 2 characters, example: "a1"
    # Letter (file) + number (rank)
    if len(square) != 2:
        return False

    file_char = square[0]  # square[0] means first character of the string like "a"
    rank_char = square[1]  # square[1] means second character of the string like "1"

    # Validate each character by checking membership:
    # file must be a-h and rank must be 1-8
    return (file_char in FILES) and (rank_char in RANKS)


def square_to_xy(square):
    """
    Convert chess square like "a1" into numbers (x, y) to make movement calculations easier.

    Mapping:
        a -> 0, b -> 1, ..., h -> 7
        1 -> 0, 2 -> 1, ..., 8 -> 7
    """
    
    # Extract the file (Letter) and rank (number) from the string square.
    file_char = square[0]
    rank_char = square[1]


    # .index(value) returns the position of value inside the string.
    # Example: FILES = "abcdefgh"
    # FILES.index("c") -> 2
    x = FILES.index(file_char)

    # Same thing for ranks:
    # RANKS = "12345678"
    # RANKS.index("4") -> 3
    y = RANKS.index(rank_char)

    # Return a tuple (x, y) which is a common way to return 2 related values.
    return x, y


def xy_to_square(x, y):
    """Convert (x, y) back into a chess square like "a1"."""
    # Reverse of square_to_xy:
    # FILES[x] gives the Letter; RANKS[y] gives the number
    # Example: x=0,y=0 -> "a" + "1" -> "a1"
    return FILES[x] + RANKS[y]


def in_bounds(x, y):
    """Return True if x,y are inside the board (0..7)."""
    # Chess board coordinates in this program go from 0 to 7 for both axes.
    # This prevents moves like ( -1, 8), which would be off the board
    return 0 <= x <= 7 and 0 <= y <= 7


def parse_input_line(line): # parsing means take some raw text and break it into structured pieces you can work with
    """
    Convert a user input line into (piece, square).
    Expected format: "<piece> <square>"

    Returns:
        (piece, square) if valid format
        None if format is wrong
    """

    # strip() removes extra spaces at the start/end
    # lower() makes input case-insensitive ("Pawn" becomes "pawn")
    # split() breaks the string into parts separated by whitespace
    parts = line.strip().lower().split()

    # Must be 2 parts: piece and square. Example: "rook a1" -> ["rook", "a1"]
    if len(parts) != 2:
        return None

    # The first part is the piece
    piece = parts[0]

    # The second part if the square (a1-h8)
    square = parts[1]

    return piece, square


# ----------------------------
# 3) INPUT FUNCTIONS
# These functions handle user interaction and validation.
# They keep "asking again" until the user provides valid input.
# ----------------------------

def get_white_piece():
    """
    Ask user repeatedly until they enter a valid white piece and square.
    White piece must be pawn or rook (the two allowed pieces).
    """

    # Turn the allowed piece list into a string for the prompt:
    # ["pawn", "rook"] -> "pawn, rook"
    allowed_text = ", ".join(ALLOWED_WHITE_PIECES)

    while True:
        # Prompt the user for input.
        # Give example so its harder to misunderstand the format
        user_input = input(
            f"Enter the WHITE piece (must be {allowed_text}) and its position "
            f"(example: pawn a1): "
        )


        # Parse input into (piece, square). If format is wrong, parsed will be None
        parsed = parse_input_line(user_input)
        if parsed is None:
            print("Error: Use format '<piece> <square>' e.g. 'pawn a1'")
            continue

        # Unpack tuple into 2 variables    
        piece, square = parsed

        # Validate that the white piece is one of the allowed types.
        if piece not in ALLOWED_WHITE_PIECES:
            print(f"Error: White piece must be one of: {allowed_text}")
            continue

        # Validate that the square looks like a real board square (a1-h8).
        if not is_valid_square(square):
            print("Error: Square must be from a1 to h8.")
            continue

        # If all validations pass, return a dictinary describing the white piece
        # Using a dictionary keeps data grouped and readable.
        return {"color": "white", "piece": piece, "square": square}



def get_black_pieces(occupied_squares):
    """
    Ask user for 1..16 black pieces.

    Requirement:
    - Before the first black piece is added, do NOT mention 'done' in the prompt.
    - After at least one piece is added, allow 'done' to finish.
    """
    
    # Store black piece dictionaries here.
    black_pieces = []

    while True:
        # Cap at 16 black pieces (as per requirement)
        if len(black_pieces) == 16:
            print("Reached maximum of 16 black pieces.")
            break

        # Change prompt text depending on whether this is the first black piece.
        if len(black_pieces) == 0:
            prompt_text = "Enter the FIRST black piece and its position (example: pawn d6): "
        else:
            prompt_text = "Enter another black piece and its position (or type 'done'): "

        # Read input and normalise it.
        user_input = input(prompt_text).strip().lower()

        # Only allow 'done' after at least 1 piece is added
        if user_input == "done":
            if len(black_pieces) == 0:
                print("Error: You must add at least one black piece before typing 'done'.")
                continue
            break

        # Parse input format.
        parsed = parse_input_line(user_input)
        if parsed is None:
            print("Error: Use format '<piece> <square>' e.g. 'pawn d6'")
            continue

        piece, square = parsed

        # Validate piece name.
        if piece not in VALID_PIECES:
            print("Error: Unknown piece. Valid pieces are:", ", ".join(VALID_PIECES))
            continue

        # Validate square format and range.
        if not is_valid_square(square):
            print("Error: Square must be from a1 to h8.")
            continue

        # Prevent two pieces being placed on the same square.
        if square in occupied_squares:
            print(f"Error: Square {square} is already occupied.")
            continue

        # If valid, create the piece dictionary and store it.
        black = {"color": "black", "piece": piece, "square": square}
        black_pieces.append(black)

        # Track occupied squares so future inputs cant reuse them.
        occupied_squares.add(square)

    return black_pieces


# ----------------------------
# 4) CAPTURE LOGIC
# This section contains the "chess rules" for which squares are attacked.
# The program checks:
# "Is a black piece sitting on a quare the white piece attacks?"
# ----------------------------

def ray_attack_squares(start_square, directions, occupied_squares):
    """
    Used for sliding pieces: rook/bishop/queen.

    It "walks" step-by-step in each direction until:
    - it hits the board edge, or
    - it hits a square with ANY piece on it (occupied)

    The occupied square is included as attackable (you can capture it),
    but squares beyond it are not reachable because the piece blocks the line.
    """

    # Convert the start square from chess notation to numeric coordinates
    start_x, start_y = square_to_xy(start_square)

    # Use a set so we do not get duplicates and membership checks are fast.
    attacked = set()

    # directions is a list of (dx, dy) pairs, e.g. rook uses (1,0), etc
    for dx, dy in directions:
        # Start one step away from the piece.
        x = start_x + dx
        y = start_y + dy

        # Keep moving step-by-step until we leave the board.
        while in_bounds(x, y):
            # Convert numeric coordinates back into chess notation like "d6".
            sq = xy_to_square(x, y)

            # This square is attacked because the sliding piece can "see" it.
            attacked.add(sq)

            # If any piece is on this square, the line is blocked.
            # We can capture this piece, but cannot go beyond it.
            # Stop if blocked by any piece
            if sq in occupied_squares:
                break

            # Move one more step in the same direction.
            x += dx
            y += dy

    return attacked


def get_white_attack_squares(white, occupied_squares):
    """
    Return a set of squares that the white piece attacks.
    If a black piece is on one of these squares, it can be captured.
    """

    # Read the piece type and its position from the dictionary.
    piece = white["piece"]
    square = white["square"]

    attacked = set()

    # ROOK: moves in straight lines up/down/left/right; blocked by pieces.
    if piece == "rook":
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        attacked = ray_attack_squares(square, directions, occupied_squares)

    # BISHOP: moves diagonally; blocked by pieces
    elif piece == "bishop":
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        attacked = ray_attack_squares(square, directions, occupied_squares)

    # QUEEN: rook + bishop combined; blocked by pieces
    elif piece == "queen":
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        attacked = ray_attack_squares(square, directions, occupied_squares)

    # KNIGHT: jumps in L-shapes; NOT blocked by pieces
    elif piece == "knight":
        x, y = square_to_xy(square)

        # All 8 possible L-shaped jumps from the current square.
        jumps = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                 (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dx, dy in jumps:
            nx = x + dx
            ny = y + dy

            # Only include the move if it stays on the board.
            if in_bounds(nx, ny):
                attacked.add(xy_to_square(nx, ny))

    # KING: can move one square in any direction.
    elif piece == "king":
        x, y = square_to_xy(square)

        # All adjacent squares around the king.
        steps = [(1, 0), (-1, 0), (0, 1), (0, -1),
                 (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in steps:
            nx = x + dx
            ny = y + dy
            if in_bounds(nx, ny):
                attacked.add(xy_to_square(nx, ny))

    # PAWN (white): captures diagonally forward (not straight forward)
    elif piece == "pawn":
        
        # Assumption: white moves "up" toward rank 8, so y increases by +1.
        x, y = square_to_xy(square)

        # Pawns capture one step diagonally: left-forward and right-forward.
        for dx in [-1, 1]:
            nx = x + dx
            ny = y + 1
            if in_bounds(nx, ny):
                attacked.add(xy_to_square(nx, ny))

    return attacked


def get_capturable_black_pieces(white, black_pieces):
    """
    Create a list of black pieces that are on attacked squares.
    """
    # Build a set of occupied squares (needed for blocking rules)
    # We need occupied squares so sliding pieces know where they are blocked.
    occupied = set()

    # Add the white piece square so it also blocks lines (if applicable).
    occupied.add(white["square"])

    # Add every black piece square to the occupied set.
    for b in black_pieces:
        occupied.add(b["square"])

    # Compute all squares the white piece attacks
    attacked_squares = get_white_attack_squares(white, occupied)

    # Any black piece on an attacked square is capturable
    capturable = []
    for b in black_pieces:
        if b["square"] in attacked_squares:
            capturable.append(b)

    return capturable


# ----------------------------
# 5) MAIN PROGRAM
# main() is the entry point that coordinates:
# input -> processing -> output
# ----------------------------

def main():
    print("Chess Capture Checker")
    print("---------------------")

    # Step 1: Get the white piece from the user.
    white = get_white_piece()

    # Track squares already taken so black pieces cannot overlap
    occupied_squares = set()
    occupied_squares.add(white["square"])

    # Step 2: Get black pieces (1..16)
    black_pieces = get_black_pieces(occupied_squares)

    # Step 3: Compute which black pieces can be captured immediately.
    capturable = get_capturable_black_pieces(white, black_pieces)

    # Step 4: Output results
    print("\nResults")
    print("-------")

    if len(capturable) == 0:
        print("No black pieces can be captured.")
    else:
        for p in capturable:
            print(p["piece"] + " at " + p["square"])


# This line means: only run main() if this file is executed directly.
if __name__ == "__main__":
    main()


# ----------------------------
# ASSUMPTIONS:
# ----------------------------
# 1) White piece is limited to exactly two predefined types (ALLOWED_WHITE_PIECES).
# 2) Black pieces can be any standard chess piece type (VALID_PIECES).
# 3) White pawn captures diagonally forward toward rank 8 (y + 1).
# 4) This is "capture squares" logic only (no check/checkmate/pins/castling/en-passant).
# 5) For sliding pieces, the first occupied square blocks further squares in that direction.
