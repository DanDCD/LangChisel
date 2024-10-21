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
    symbol_epsilon = CFSymbol(TokenTag("EPSILON"))
    end_of_string = CFSymbol(TokenTag("EOS"))

    test_grammar = CFGrammar(
        [
            CFProduction(symbol_S, [symbol_A, symbol_S]),
            CFProduction(symbol_S, [symbol_epsilon]),
            CFProduction(symbol_A, [symbol_t, symbol_B]),
            CFProduction(symbol_A, [symbol_u]),
            CFProduction(symbol_B, [symbol_v]),
        ],
        symbol_S,
        symbol_epsilon,
        end_of_string,
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