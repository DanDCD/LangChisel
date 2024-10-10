from lexer import Token, TokenType
from enum import Enum


class CFSymbol:
    def __init__(self, value: str | TokenType) -> None:
        """A Single Context Free Symbol

        Args:
            value (str): the name of the non-terminal or token of the terminal
        """
        self.value = value

    def __repr__(self) -> str:
        return f"(CFSymbol: {self.value})"


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


# Grammar:
# 1. S -> A S
# 2. S -> epsilon
# 3. A -> t B
# 4. A -> u
# 5. B -> v

symbol_S = CFSymbol("S")
symbol_A = CFSymbol("A")
symbol_B = CFSymbol("B")
symbol_t = CFSymbol(TokenType.t)
symbol_u = CFSymbol(TokenType.u)
symbol_v = CFSymbol(TokenType.v)
symbol_epsilon = CFSymbol(None)

test_grammar = [
    CFProduction(symbol_S, [symbol_A, symbol_S]),
    CFProduction(symbol_S, [symbol_epsilon]),
    CFProduction(symbol_A, [symbol_t, symbol_B]),
    CFProduction(symbol_A, [symbol_u]),
    CFProduction(symbol_B, [symbol_v])
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
    return isinstance(symbol.value, TokenType)


def LL1_first(symbol: CFSymbol, grammar: list[CFProduction], known_first_sets: dict[CFSymbol, list[CFSymbol]]) -> list[CFSymbol]:
    """iterate through possible derivations from symbol and extract all the terminals that may appear first in a string derived from symbol"""
    
    if symbol in known_first_sets:
        return known_first_sets[symbol]
    
    # definition for First(a) = {a}  OR First(epsilon) = {epsilon}
    if is_terminal(symbol) or symbol.value == None:
        return [symbol]
    first_set = set()
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
            first_set.update(first_of_symbol - {CFSymbol(None)})

            # we can only keep adding (i.e. add First(C) if First(B) contained epsilon)
            if not CFSymbol(None) in first_of_symbol:
                break

            # if we have reached the end of the to_sequence and (from above) first(X) contains epsilon, we add epsilon
            if i == len(to_sequence) - 1:
                first_set.add(CFSymbol(None))

    return first_set


def extract_LL1_first_sets(grammar: list[CFProduction]) -> dict[CFSymbol, list[CFSymbol]]:
    """ """
    first_sets: dict[CFSymbol, list[CFSymbol]] = {}
    symbols = get_non_terminals(grammar)+get_terminals(grammar)

    for symbol in symbols:
        first_sets[symbol] = LL1_first(symbol, grammar, first_sets)

    return first_sets


extract_LL1_first_sets(test_grammar)


def extract_LL1_follow_sets(grammar: list[CFProduction]) -> dict:
    pass


def build_LL1_table(grammar: list[CFProduction]) -> dict:
    pass


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
