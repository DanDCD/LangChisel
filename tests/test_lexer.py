import pytest
from src.lexer import *


def test_find_lexemes():
    source_code = "my_num = 5"
    expected_lexemes = [
        ('my_num', TokenType.IDENTIFIER),
        (' ', TokenType.WHITE_SPACE),
        ('=', TokenType.ASSIGN),
        (' ', TokenType.WHITE_SPACE),
        ('5', TokenType.NUM)
    ]
    
    lexemes = find_lexemes(source_code, regex_to_tokentype)
    assert lexemes == expected_lexemes, f"Expected {expected_lexemes}, but got {lexemes}"


def test_construct_tokens():
    lexemes = [
        ('my_num', TokenType.IDENTIFIER),
        (' ', TokenType.WHITE_SPACE),
        ('=', TokenType.ASSIGN),
        (' ', TokenType.WHITE_SPACE),
        ('5', TokenType.NUM)
    ]

    expected_tokens = [
        Token(TokenType.IDENTIFIER, "my_num"),
        Token(TokenType.WHITE_SPACE, None),
        Token(TokenType.ASSIGN, None),
        Token(TokenType.WHITE_SPACE, None),
        Token(TokenType.NUM, 5)         
    ]
    
    tokens = construct_tokens(lexemes, tokentype_to_data_extraction)
    assert tokens == expected_tokens, f"Expected {expected_tokens}, but got {tokens}"

