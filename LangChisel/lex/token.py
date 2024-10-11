

class TokenTag:
    def __init__(self, identifier:str) -> None:
        """A representation of a ingle tag of Token
        
         Args:
            identifier (str): the name of the non-terminal or token of the terminal
        """
        self.identifier = identifier
    
    def __repr__(self) -> str:
        return f"Token: {self.identifier}"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, TokenTag):
            return self.identifier == other.identifier
        return False
    
    def __hash__(self) -> int:
        return hash((self.identifier))


class Token:
    def __init__(self, tag: TokenTag, value: any) -> None:
        """A Token a meaningful collection of characters that carry semantic weight to the language

        Args:
            tag (Tokentag): The tag of token this is
            value (any): Extra information (if any) to be associated with this token
        """
        self.tag = tag  # the tag of this token
        self.value = value  # data associated with this token

    def __repr__(self) -> str:
        return f"(tag: {self.tag}, Value: {self.value})"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.tag == other.tag and self.value == other.value
        return False

    def __hash__(self):
        return hash((self.tag, self.value))