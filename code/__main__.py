if __name__ == "__main__":
    import sys
    import os
    import re

    # get the absolute path of the root directory 
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    from LangChisel.compile import *
    from LangChisel.interpret import *
    from LangChisel.lex import *
    from LangChisel.parse import *
    
    # a mapping of compiled regular expressions to their respective tokentype enums
    regex_to_tokentype: dict[re.Pattern, TokenTag] = {
        re.compile(r"\s+") : TokenTag("WHITE_SPACE"),
        re.compile(r";"): TokenTag("LINE_BREAK"),
        re.compile(r"=") : TokenTag("ASSIGN"),
        re.compile(r"\+") : TokenTag("ADD"),
        re.compile(r"var") : TokenTag("VAR_DECL"),
        re.compile(r"\d+") : TokenTag("NUM"),
        re.compile(r"\w+") : TokenTag("IDENTIFIER"),
    }


    # a mapping of tokentypes to callables used to extract data from a lexeme of this type
    tokentype_to_data_extraction: dict[re.Pattern, Callable[[str], any]] = {
        TokenTag("IDENTIFIER"): lambda substr :  str(substr),
        TokenTag("NUM"): lambda substr : int(substr)
    }


    source_code = "my_num = 5; my_num = 5 + 5;"
    lexemes = find_lexemes(source_code, regex_to_tokentype)
    tokens = construct_tokens(lexemes, tokentype_to_data_extraction)
    print(tokens)