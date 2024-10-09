from lexer import Token
from enum import Enum


class ASTNodeType(Enum):
    PROGRAM = "PROGRAM",
    OPERATION = "OPERATION",
    ASSIGNMENT = "ASSIGNMENT",
    BIN_OPERATION = "BINARY OPERATION",
    UN_OPERATION = "UNARY OPERATION",
    VALUE = "VALUE",
    L_VALUE = "LEFT VALUE",
    R_VALUE = "RIGHT VALUE",
    BIN_CALLABLE = "BINARY CALLABLE",
    UN_CALLABLE = "UNARY CALLABLE"



class ASTNode:
    def __init__(self, type:ASTNodeType, children:list['ASTNode'], data: dict) -> None:
        """an ASTNode is a node in a parse tree used to define the semantics of a program

        Args:
            type (ASTNodeType): The kind of node this is - i.e. what this node 'means' to the tree and execution
            children (list[ASTNode]): The children of this node (note: for some node types, order might matter)
            data (dict): The data associated with this node 
        """
        self.type = type
        self.children = children
        self.data = data






class Rule:
    def apply(self, string:str):
        raise NotImplementedError


class TerminalRule(Rule):
    def __init__(self, terminal: str) -> None:
        self.terminal
        
    def apply(self, string:str):
        if string.startswith(self.terminal):
            

class SequenceRule(Rule):
    def __init__(self, *rules: tuple[Rule]) -> None:
        self.rules = rules


rules = {
    
}


def parse_with_recursive_descent(tokens: list[Token]) -> ASTNode:
    """parse a list of tokens using recursive descent to perform LL parsing

    Args:
        tokens (list[Token]): the tokens to be parsed
        
    Returns:
        ASTNode: the root node of the constructed Abstract Syntax Tree
    """
    pass