if __name__ == "__main__":
    import lexer
    import parser
    import re
    from typing import Callable
    
    # a mapping of compiled regular expressions to their respective tokentype enums
    regex_to_tokentype: dict[re.Pattern, lexer.TokenType] = {
        re.compile(r"\s+") : lexer.TokenType.WHITE_SPACE,
        re.compile(r"=") : lexer.TokenType.ASSIGN,
        re.compile(r"var") : lexer.TokenType.VAR_DECLARATION,
        re.compile(r"\d+") : lexer.TokenType.NUM,
        re.compile(r"\w+") : lexer.TokenType.IDENTIFIER,
    }


    # a mapping of tokentypes to callables used to extract data from a lexeme of this type
    tokentype_to_data_extraction: dict[re.Pattern, Callable[[str], any]] = {
        lexer.TokenType.IDENTIFIER: lambda substr :  str(substr),
        lexer.TokenType.NUM: lambda substr : int(substr)
    }


    source_code = "my_num = 5"
    lexemes = lexer.find_lexemes(source_code, regex_to_tokentype)
    tokens = lexer.construct_tokens(lexemes, tokentype_to_data_extraction)
    print(tokens)