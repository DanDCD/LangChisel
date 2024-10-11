# tests/test_lexer.py
import sys
import os
import pytest

# Add the package root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from LangChisel.lex import *

 # a mapping of compiled regular expressions to their respective tokentype enums
regex_to_tokentype: dict[re.Pattern, TokenTag] = {
    re.compile(r"\s+") : TokenTag("WHITE_SPACE"),
    re.compile(r"=") : TokenTag("ASSIGN"),
    re.compile(r"\d+") : TokenTag("NUM"),
    re.compile(r"\w+") : TokenTag("IDENTIFIER"),
}


# a mapping of tokentypes to callables used to extract data from a lexeme of this type
tokentype_to_data_extraction: dict[re.Pattern, Callable[[str], any]] = {
    TokenTag("IDENTIFIER") : lambda substr :  str(substr),
    TokenTag("NUM") : lambda substr : int(substr)
}


def test_find_lexemes():
    source_code = "my_num = 5"
    expected_lexemes = [
        ('my_num', TokenTag("IDENTIFIER")),
        (' ', TokenTag("WHITE_SPACE")),
        ('=', TokenTag("ASSIGN")),
        (' ', TokenTag("WHITE_SPACE")),
        ('5', TokenTag("NUM")),
        ('', TokenTag("EOF"))
    ]
    
    lexemes = find_lexemes(source_code, regex_to_tokentype)
    assert lexemes == expected_lexemes, f"Expected {expected_lexemes}, but got {lexemes}"


def test_construct_tokens():
    lexemes = [
        ('my_num', TokenTag("IDENTIFIER")),
        (' ', TokenTag("WHITE_SPACE")),
        ('=', TokenTag("ASSIGN")),
        (' ', TokenTag("WHITE_SPACE")),
        ('5', TokenTag("NUM")),
        ('', TokenTag("EOF"))
    ]

    expected_tokens = [
        Token(TokenTag("IDENTIFIER"), "my_num"),
        Token(TokenTag("WHITE_SPACE"), None),
        Token(TokenTag("ASSIGN"), None),
        Token(TokenTag("WHITE_SPACE"), None),
        Token(TokenTag("NUM"), 5),
        Token(TokenTag("EOF"), None)  
    ]
    
    tokens = construct_tokens(lexemes, tokentype_to_data_extraction)
    assert tokens == expected_tokens, f"Expected {expected_tokens}, but got {tokens}"

