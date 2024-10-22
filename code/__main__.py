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

    source_code = """var x;
    x = 5;
    print(x);
    """

    regex_to_tokentype = {
        re.compile(r"var"): TokenTag("var"),
        re.compile(r";"): TokenTag("line_break"),
        re.compile(r"\="): TokenTag("assign"),
        re.compile(r"\("): TokenTag("l_brack"),
        re.compile(r"\)"): TokenTag("r_brack"),
        re.compile(r"print"): TokenTag("print"),
        re.compile(r"\s+"): TokenTag("white_space"),
        re.compile(r"\d+"): TokenTag("num"),
        re.compile(r"\w+"): TokenTag("identifier"),
    }

    tokentype_to_data_extraction = {
        TokenTag("num"): lambda string: int(string),
        TokenTag("identifier"): lambda string: str(string),
    }

    lexemes = find_lexemes(source_code, regex_to_tokentype)
    tokens = construct_tokens(lexemes, tokentype_to_data_extraction)
    # clear white space
    tokens = [token for token in tokens if token.tag != TokenTag("white_space")]
    print(tokens)

    # Grammar:
    # 1. S -> Statement S | epsilon
    # 2. Statement -> Declaration | Assignment | Print
    # 3. Declaration -> "var" "identifier" "break"
    # 4. Assignemnt -> "identifier" "assign" Value "break"
    # 5. Value -> "num" | "identifier"
    # 6. Print -> "print" "lbrack" Value "rbrack" "break"

    symbol_S = CFSymbol("S")
    symbol_statement = CFSymbol("Statement")
    symbol_declaration = CFSymbol("Declaration")
    symbol_assignment = CFSymbol("Assignemnt")
    symbol_print = CFSymbol("Print")
    symbol_value = CFSymbol("Value")

    term_var = CFSymbol(TokenTag("var"))
    term_linebreak = CFSymbol(TokenTag("line_break"))
    term_assign = CFSymbol(TokenTag("assign"))
    term_l_brack = CFSymbol(TokenTag("l_brack"))
    term_r_brack = CFSymbol(TokenTag("r_brack"))
    term_print = CFSymbol(TokenTag("print"))
    term_white_space = CFSymbol(TokenTag("white_space"))
    term_identifier = CFSymbol(TokenTag("identifier"))
    term_num = CFSymbol(TokenTag("num"))
    term_epsilon = CFSymbol(TokenTag("EPSILON"))
    term_end_of_string = CFSymbol(TokenTag("EOS"))

    test_grammar = CFGrammar(
        [
            CFProduction(symbol_S, [symbol_statement, symbol_S]),
            CFProduction(symbol_S, [term_epsilon]),
            CFProduction(symbol_statement, [symbol_declaration]),
            CFProduction(symbol_statement, [symbol_assignment]),
            CFProduction(symbol_statement, [symbol_print]),
            CFProduction(
                symbol_declaration, [term_var, term_identifier, term_linebreak]
            ),
            CFProduction(
                symbol_assignment,
                [term_identifier, term_assign, symbol_value, term_linebreak],
            ),
            CFProduction(
                symbol_print,
                [term_print, term_l_brack, symbol_value, term_r_brack, term_linebreak],
            ),
            CFProduction(symbol_value, [term_identifier]),
            CFProduction(symbol_value, [term_num]),
        ],
        symbol_S,
        term_epsilon,
        term_end_of_string,
    )

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

    derivation_sequence = get_LL1_derivation_seq(tokens.copy(), test_grammar, table)
    print("Derivations:")
    print(derivation_sequence)

    parsed_syntax_tree = generate_syntax_tree_symbols(derivation_sequence, test_grammar)
    print("Parsed Tree:")
    print(parsed_syntax_tree)
    tokenise_syntax_tree_terminals(parsed_syntax_tree, tokens, test_grammar)
    print("Parsed Tree:")
    print(parsed_syntax_tree)
