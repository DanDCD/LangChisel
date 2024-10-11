from LangChisel.lex.greedy_backtrack_lexer import Token, TokenTag
from enum import Enum


class CFSymbol:
    def __init__(self, value: str | TokenTag) -> None:
        """A Single Context Free Symbol

        Args:
            value (str): the name of the non-terminal or token of the terminal
        """
        self.value = value

    def __repr__(self) -> str:
        return f"(CFSymbol: {self.value})"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, CFSymbol):
            return self.value == other.value
        return False
    
    def __hash__(self) -> int:
        return hash((self.value))


class CFProduction:
    def __init__(self, from_symbol: CFSymbol, to_sequence: list[CFSymbol]):
        """A Production Rule defining a possible transition from one symbol to a sequence of other symbols

        Args:
            from_symbol (CFSymbol): The 'left hand-side' of this derivation, what the derviation 'derives from'
            to_sequence (list[CFSymbol]): The 'right hand-side' of this derivation, what the derivation 'derives to'
        """
        self.from_symbol = from_symbol
        self.to_sequence = to_sequence

    def __repr__(self) -> str:
        return f"(CFProduction: {self.from_symbol} => {self.to_sequence})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CFProduction):
            return self.from_symbol == other.from_symbol and self.to_sequence == other.to_sequence
        return False
    
    def __hash__(self) -> int:
        return hash((self.from_symbol, self.to_sequence))

# Grammar:
# 1. S -> A S
# 2. S -> epsilon
# 3. A -> t B
# 4. A -> u
# 5. B -> v

symbol_S = CFSymbol("S")
symbol_A = CFSymbol("A")
symbol_B = CFSymbol("B")
symbol_t = CFSymbol(TokenTag("t"))
symbol_u = CFSymbol(TokenTag("u"))
symbol_v = CFSymbol(TokenTag("v"))
symbol_epsilon = CFSymbol(None)

test_grammar = [
    CFProduction(symbol_S, [symbol_A, symbol_S]),
    CFProduction(symbol_S, [symbol_epsilon]),
    CFProduction(symbol_A, [symbol_t, symbol_B]),
    CFProduction(symbol_A, [symbol_u]),
    CFProduction(symbol_B, [symbol_v]),
]


def get_non_terminals(grammar: list[CFProduction]) -> list[CFSymbol]:
    """ """
    return list(set([production.from_symbol for production in grammar]))


def get_terminals(grammar: list[CFProduction]) -> list[CFSymbol]:
    """ """
    terminals = []
    for production in grammar:
        for symbol in production.to_sequence:
            if is_terminal(symbol):
                terminals.append(symbol)
    return list(set(terminals))


def is_terminal(symbol: CFSymbol) -> bool:
    """ """
    return isinstance(symbol.value, TokenTag)


def LL1_first(
    symbol: CFSymbol,
    grammar: list[CFProduction],
    known_first_sets: dict[CFSymbol, list[CFSymbol]],
):
    """Find the set of symbols that may appear in the front of a string derived from A
    That is, First(A) = { t | A->...->tW for some string w}
    First(A) will include epsilon, only if A can produce epsilon/the empty string as a complete derivation of A.

    Args:
        symbol (CFSymbol): the symbol we want the first set of
        grammar (list[CFProduction]): the grammar we will use to derive the first set
        known_first_sets (dict[CFSymbol, list[CFSymbol]]): a dictionary containing any pre-calculated first_sets - if empty, the function will simply calculate any dependency recursively - any newly calculated first-sets will be added to this dictionary
    """

    if symbol in known_first_sets:
        return known_first_sets[symbol]

    # definition for First(a) = {a}  OR First(epsilon) = {epsilon}
    if is_terminal(symbol) or symbol.value == None:
        return [symbol]

    first_set = set()  # this will be the set of 'First(symbol)' we will return
    relevant_productions = [
        production for production in grammar if production.from_symbol == symbol
    ]

    for production in relevant_productions:
        to_sequence = production.to_sequence
        # should never have a production that does not contain a single derived symbol
        assert len(to_sequence) > 0

        # First(A) += {t} if A -> t W OR First(A) += epsilon if A -> epsilon
        if is_terminal(to_sequence[0]) or to_sequence[0].value == None:
            first_set.add(production.to_sequence[0])
            continue

        # First(A) += First(B) + First(C) if A -> B C and epsilon in B OR First(A) += First(B) if A -> A B
        for i, symbol in enumerate(to_sequence):
            first_of_symbol = LL1_first(symbol, grammar, known_first_sets)
            # add all terminals in First(X) other than epsilon
            first_set.update(set(first_of_symbol) - {CFSymbol(None)})

            # we can only keep adding (i.e. add First(C) if First(B) contained epsilon)
            if not CFSymbol(None) in first_of_symbol:
                break

            # if we have reached the end of the to_sequence and (from above) first(X) contains epsilon, we add epsilon
            if i == len(to_sequence) - 1:
                first_set.add(CFSymbol(None))

    return list(first_set)


def extract_LL1_first_sets(
    grammar: list[CFProduction],
) -> dict[CFSymbol, list[CFSymbol]]:
    """Calculate the First sets for all symbols in the grammar"""
    first_sets: dict[CFSymbol, list[CFSymbol]] = {}
    symbols = get_non_terminals(grammar) + get_terminals(grammar)

    for symbol in symbols:
        first_sets[symbol] = LL1_first(symbol, grammar, first_sets)

    return first_sets


def LL1_follow(
    symbol: CFSymbol,
    grammar: list[CFProduction],
    known_first_sets: dict[CFSymbol, list[CFSymbol]],
    known_follow_sets: dict[CFSymbol, list[CFSymbol]],
):
    """Find the set of symbols that may appear a string derived from this symbol (Note: this does not mean 'at the end' of a derived string, but immediately after/next any derived string)
    That is, Follow(A) = { t | S ->...-> aAtw for some a, w}, where S is the start symbol
    """
    if symbol in known_follow_sets:
        return known_follow_sets[symbol]

    follow_set = set()
    # if symbol is start symbol, add $ (the end of string symbol)
    if symbol == CFSymbol("S"):
        follow_set.add(CFSymbol(TokenTag("EOS")))

    # this time, relevant productions for symbol A, are those where X -> "..."A"..."
    relevant_productions = [
        production for production in grammar if symbol in production.to_sequence
    ]

    for production in relevant_productions:
        from_symbol = production.from_symbol
        to_sequence = production.to_sequence

        symbol_pos = to_sequence.index(symbol)

        # Follow(A) += Follow(B) if B -> w A and B != A
        if symbol_pos == len(to_sequence) - 1:
            if from_symbol != symbol:
                follow_set.update(LL1_follow(from_symbol, grammar, known_first_sets, known_follow_sets))
            continue

        # we now know there must be a 'next symbol' from here onwards:
        next_symbol = to_sequence[symbol_pos + 1]
        first_next = LL1_first(next_symbol, grammar, known_first_sets)

        # Follow(A) += Follow(B) if B -> a A w, and eps in First(w) -- (as if w can derive to nothing, a string Following B can also Follow A)
        if CFSymbol(None) in first_next:
            follow_set.update(
                LL1_follow(from_symbol, grammar, known_first_sets, known_follow_sets)
            )

        # Follow(A) += First(w) - {eps} if B -> a A w
        follow_set.update(set(first_next) - {CFSymbol(None)})

    return list(follow_set)


def extract_LL1_follow_sets(
    grammar: list[CFProduction], first_sets: dict[CFSymbol, list[CFSymbol]]
) -> dict:
    follow_sets: dict[CFSymbol, list[CFSymbol]] = {}
    symbols = get_non_terminals(grammar) # we only define follow for non-terminals

    for symbol in symbols:
        follow_sets[symbol] = LL1_follow(symbol, grammar, first_sets, follow_sets)
        # print(follow_sets)
    
    return follow_sets


def build_LL1_table(grammar: list[CFProduction]) -> dict:
    pass


first = extract_LL1_first_sets(test_grammar)
follow = extract_LL1_follow_sets(test_grammar, first)
print("FIRST")
print(first)
print("FOLLOW")
print(follow)

class ASTNodeType(Enum):
    PROGRAM = ("PROGRAM",)
    OPERATION = ("OPERATION",)
    ASSIGNMENT = ("ASSIGNMENT",)
    BIN_OPERATION = ("BINARY OPERATION",)
    UN_OPERATION = ("UNARY OPERATION",)
    VALUE = ("VALUE",)
    L_VALUE = ("LEFT VALUE",)
    R_VALUE = ("RIGHT VALUE",)
    BIN_CALLABLE = ("BINARY CALLABLE",)
    UN_CALLABLE = "UNARY CALLABLE"


class ASTNode:
    def __init__(
        self, type: ASTNodeType, children: list["ASTNode"], data: dict
    ) -> None:
        """an ASTNode is a node in a parse tree used to define the semantics of a program

        Args:
            type (ASTNodeType): The kind of node this is - i.e. what this node 'means' to the tree and execution
            children (list[ASTNode]): The children of this node (note: for some node types, order might matter)
            data (dict): The data associated with this node
        """
        self.type = type
        self.children = children
        self.data = data
