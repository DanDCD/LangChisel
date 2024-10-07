import re
from enum import Enum
from typing import Callable


class TokenType(Enum):
    WHITE_SPACE = "WHITE_SPACE"
    IDENTIFIER = "IDENTIFIER"
    ASSIGN = "ASSIGN"
    NUM = "NUM"


class Token:
    def __init__(self, type: TokenType, value: any) -> None:
        self.type = type  # the type of this token
        self.value = value  # data associated with this token

    def __repr__(self) -> str:
        return f"(Type: {self.type}, Value:{self.value})"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False
    
    def __hash__(self):
        return hash((self.type, self.value))


def check_for_match(substring: str, pattern_to_type: dict[re.Pattern, TokenType])->TokenType:
    """checks if the substring matches a lexeme, if so returns the token type

    Args:
        substring str: the substring to check

    Returns:
        TokenType: the token type that matches this substring
    """
    for [regex, type] in pattern_to_type.items():
        if regex.fullmatch(substring):
            return type
    return None


def find_lexemes(string: str, pattern_to_type: dict[re.Pattern, TokenType]) -> list[(str, TokenType)]:
    """Identifies Lexemes in messy text
    
    Args:
        string str: the text to search for lexemes
        
    Returns
        list[(str, TokenType)]: a list of substring lexemes and the associated token types
    """
    foundLexemes: list[(str, TokenType)] = []
    front = 0
    back = len(string)
    while(back > front):
        substring = string[front:back]
        lexeme = check_for_match(substring, pattern_to_type)
        if lexeme:
            foundLexemes.append((substring, lexeme))
            front = back
            back = len(string)
        else:
            back -=1
    return foundLexemes


def construct_tokens(lexemes: list[(str, TokenType)], type_to_extractor: dict[re.Pattern, Callable[[str], any]]) -> list[Token]:
    """_summary_

    Args:
        lexemes (list[(str, TokenType)]): a list of substring lexemes and the associated token types

    Returns:
        list[Token]: a list of tokens
    """
    tokens: list[Token] = []
    for [substring, lexeme_type] in lexemes:
        extractor = type_to_extractor.get(lexeme_type)
        tokens.append(Token(lexeme_type, extractor(substring) if extractor else None))
    return tokens

# a mapping of compiled regular expressions to their respective tokentype enums
regex_to_tokentype: dict[re.Pattern, TokenType] = {
    re.compile(r"\s+") : TokenType.WHITE_SPACE,
    re.compile(r"=") : TokenType.ASSIGN,
    re.compile(r"\d+") : TokenType.NUM,
    re.compile(r"\w+") : TokenType.IDENTIFIER,
}


# a mapping of tokentypes to callables used to extract data from a lexeme of this type
tokentype_to_data_extraction: dict[re.Pattern, Callable[[str], any]] = {
    TokenType.IDENTIFIER: lambda substr :  str(substr),
    TokenType.NUM: lambda substr : int(substr)
}


source_code = "my_num = 5"

print(construct_tokens(find_lexemes(source_code, regex_to_tokentype), tokentype_to_data_extraction))