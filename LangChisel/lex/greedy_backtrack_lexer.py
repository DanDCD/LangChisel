import re
from typing import Callable
from .token import *


def check_for_match(
    substring: str, pattern_to_type: dict[re.Pattern, TokenTag]
) -> TokenTag:
    """checks if the substring matches a lexeme, if so returns the token type

    Args:
        substring (str): the substring to check
        pattern_to_type (dict[re.Pattern, TokenType]): a dictionary containing mappings of regex patterns that identify a lexeme and their respective tokens

    Returns:
        matching_type (TokenType): the token type that matches this substring
    """
    for [regex, type] in pattern_to_type.items():
        if regex.fullmatch(substring):
            return type
    return None


def find_lexemes(
    string: str, pattern_to_type: dict[re.Pattern, TokenTag]
) -> list[(str, TokenTag)]:
    """Identifies Lexemes in messy text

    Args:
        string str: the text to search for lexemes

    Returns
        list[(str, TokenType)]: a list of substring lexemes and the associated token types
    """
    foundLexemes: list[(str, TokenTag)] = []
    front = 0
    back = len(string)
    while back > front:
        substring = string[front:back]
        lexeme = check_for_match(substring, pattern_to_type)
        if lexeme:
            foundLexemes.append((substring, lexeme))
            front = back
            back = len(string)
        else:
            back -= 1
    return foundLexemes


def construct_tokens(
    lexemes: list[(str, TokenTag)],
    type_to_extractor: dict[TokenTag, Callable[[str], any]],
) -> list[Token]:
    """takes a list of lexemes and turns them into tokens

    Args:
        lexemes (list[(str, TokenType)]): a list of substring lexemes and the associated token types
        type_to_extractor (dict[TokenType, Callble[[str], any]]): a mapping of TokenType to a lambda that can be used to extract data from said TokenType
        
    Returns:
        list[Token]: a list of tokens
    """
    tokens: list[Token] = []
    for [substring, lexeme_type] in lexemes:
        extractor = type_to_extractor.get(lexeme_type)
        tokens.append(Token(lexeme_type, extractor(substring) if extractor else None))
    return tokens
