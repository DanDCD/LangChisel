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
# 1. S -> AB
# 2. A -> a
# 3. A -> eps
# 4. B -> b

symbol_S = CFSymbol("S")
symbol_A = CFSymbol("A")
symbol_B = CFSymbol("B")
symbol_a = CFSymbol(TokenType.a)
symbol_b = CFSymbol(TokenType.b)
symbol_epsilon = CFSymbol(None)

production_1 = CFProduction(symbol_S, [symbol_A, symbol_B])
production_2 = CFProduction(symbol_A, [symbol_a])
production_3 = CFProduction(symbol_A, [symbol_epsilon])
production_4 = CFProduction(symbol_B, [symbol_b])


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
