if __name__ == "__main__":
    import sys
    import os
    import re

    # get the absolute path of the root directory
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from LangChisel.compile import *
    from LangChisel.interpret import *
    from LangChisel.lex import *
    from LangChisel.parse import *

    # source_code = "my_num = 5; my_num = 5 + 5;"

    # # a mapping of compiled regular expressions to their respective tokentype enums
    # regex_to_tokentype: dict[re.Pattern, TokenTag] = {
    #     re.compile(r"\s+"): TokenTag("WHITE_SPACE"),
    #     re.compile(r";"): TokenTag("LINE_BREAK"),
    #     re.compile(r"="): TokenTag("ASSIGN"),
    #     re.compile(r"\+"): TokenTag("ADD"),
    #     re.compile(r"var"): TokenTag("VAR_DECL"),
    #     re.compile(r"\d+"): TokenTag("NUM"),
    #     re.compile(r"\w+"): TokenTag("IDENTIFIER"),
    # }

    # # a mapping of tokentypes to callables used to extract data from a lexeme of this type
    # tokentype_to_data_extraction: dict[re.Pattern, Callable[[str], any]] = {
    #     TokenTag("IDENTIFIER"): lambda substr: str(substr),
    #     TokenTag("NUM"): lambda substr: int(substr),
    # }

    source_code = "tvu"

    regex_to_tokentype = {
        re.compile(r"t"): TokenTag("t"),
        re.compile(r"u"): TokenTag("u"),
        re.compile(r"v"): TokenTag("v"),
    }
    
    tokentype_to_data_extraction = {}

    lexemes = find_lexemes(source_code, regex_to_tokentype)
    tokens = construct_tokens(lexemes, tokentype_to_data_extraction)
    print(tokens)

    # Grammar:
    # 1. S -> A S
    # 2. S -> epsilon
    # 3. A -> t B
    # 4. A -> u
    # 5. B -> v

    symbol_S = CFSymbol("S")
    symbol_A = CFSymbol("A")
    symbol_B = CFSymbol("B")
    symbol_t = CFSymbol(TokenTag("t"))
    symbol_u = CFSymbol(TokenTag("u"))
    symbol_v = CFSymbol(TokenTag("v"))
    symbol_epsilon = CFSymbol(None)

    test_grammar = [
        CFProduction(symbol_S, [symbol_A, symbol_S]),
        CFProduction(symbol_S, [symbol_epsilon]),
        CFProduction(symbol_A, [symbol_t, symbol_B]),
        CFProduction(symbol_A, [symbol_u]),
        CFProduction(symbol_B, [symbol_v]),
    ]

    first_sets = extract_LL1_first_sets(test_grammar)
    follow_sets = extract_LL1_follow_sets(test_grammar, first_sets)     

    print("FIRST sets:")
    for sym, first in first_sets.items():
        print(f"{sym.value}: {[s.value for s in first]}")

    print("\nFOLLOW sets:")
    for sym, follow in follow_sets.items():
        print(f"{sym.value}: {[s.value for s in follow]}")
        
    table = build_LL1_table(test_grammar, first_sets, follow_sets)
    print("\nTABLE")
    print(table)