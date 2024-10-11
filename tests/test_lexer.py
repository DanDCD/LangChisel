# tests/test_lexer.py
import sys
import os
import pytest

# Add the package root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from LangChisel.lex import *

 # a mapping of compiled regular expressions to their respective tokentype enums
regex_to_tokentype: dict[re.Pattern, TokenType] = {
    re.compile(r"\s+") : TokenType.WHITE_SPACE,
    re.compile(r"=") : TokenType.ASSIGN,
    re.compile(r"\d+") : TokenType.NUM,
    re.compile(r"\w+") :TokenType.IDENTIFIER,
}


# a mapping of tokentypes to callables used to extract data from a lexeme of this type
tokentype_to_data_extraction: dict[re.Pattern, Callable[[str], any]] = {
    TokenType.IDENTIFIER: lambda substr :  str(substr),
    TokenType.NUM: lambda substr : int(substr)
}


def test_find_lexemes():
    source_code = "my_num = 5"
    expected_lexemes = [
        ('my_num', TokenType.IDENTIFIER),
        (' ', TokenType.WHITE_SPACE),
        ('=', TokenType.ASSIGN),
        (' ', TokenType.WHITE_SPACE),
        ('5', TokenType.NUM),
        ('', TokenType.EOF)
    ]
    
    lexemes = find_lexemes(source_code, regex_to_tokentype)
    assert lexemes == expected_lexemes, f"Expected {expected_lexemes}, but got {lexemes}"


def test_construct_tokens():
    lexemes = [
        ('my_num', TokenType.IDENTIFIER),
        (' ', TokenType.WHITE_SPACE),
        ('=', TokenType.ASSIGN),
        (' ', TokenType.WHITE_SPACE),
        ('5', TokenType.NUM),
        ('', TokenType.EOF)
    ]

    expected_tokens = [
        Token(TokenType.IDENTIFIER, "my_num"),
        Token(TokenType.WHITE_SPACE, None),
        Token(TokenType.ASSIGN, None),
        Token(TokenType.WHITE_SPACE, None),
        Token(TokenType.NUM, 5),
        Token(TokenType.EOF, None)  
    ]
    
    tokens = construct_tokens(lexemes, tokentype_to_data_extraction)
    assert tokens == expected_tokens, f"Expected {expected_tokens}, but got {tokens}"

