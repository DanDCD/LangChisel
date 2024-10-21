# tests/test_lexer.py
import sys
import os
import pytest

# Add the package root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from LangChisel.parse import *


# E -> T E'
# E' -> + T E'
# E' -> eps
# T -> F T'
# T' -> * F T'
# T' -> eps
# F -> ( E )
# F -> id
test_grammar_1 = CFGrammar(
    [
        CFProduction(CFSymbol("E"), [CFSymbol("T"), CFSymbol("E'")]),
        CFProduction(
            CFSymbol("E'"), [CFSymbol(TokenTag("+")), CFSymbol("T"), CFSymbol("E'")]
        ),
        CFProduction(CFSymbol("E'"), [CFSymbol(None)]),
        CFProduction(CFSymbol("T"), [CFSymbol("F"), CFSymbol("T'")]),
        CFProduction(
            CFSymbol("T'"), [CFSymbol(TokenTag("*")), CFSymbol("F"), CFSymbol("T'")]
        ),
        CFProduction(CFSymbol("T'"), [CFSymbol(None)]),
        CFProduction(
            CFSymbol("F"),
            [CFSymbol(TokenTag("(")), CFSymbol("E"), CFSymbol(TokenTag(")"))],
        ),
        CFProduction(CFSymbol("F"), [CFSymbol(TokenTag("id"))]),
    ],
    CFSymbol("E"),
    CFSymbol(None),
    CFSymbol("$"),
)

expected_first_1 = {
    CFSymbol("E"): [CFSymbol(TokenTag("id")), CFSymbol(TokenTag("("))],
    CFSymbol("E'"): [CFSymbol(TokenTag("+")), CFSymbol(None)],
    CFSymbol("T"): [CFSymbol(TokenTag("id")), CFSymbol(TokenTag("("))],
    CFSymbol("T'"): [CFSymbol(TokenTag("*")), CFSymbol(None)],
    CFSymbol("F"): [CFSymbol(TokenTag("id")), CFSymbol(TokenTag("("))],
    test_grammar_1.epsilon: [test_grammar_1.epsilon],
}
for terminal in get_terminals(test_grammar_1.productions):
    expected_first_1[terminal] = [terminal]


expected_follow_1 = {
    CFSymbol("E"): [test_grammar_1.end_of_string, CFSymbol(TokenTag(")"))],
    CFSymbol("E'"): [test_grammar_1.end_of_string, CFSymbol(TokenTag(")"))],
    CFSymbol("T"): [
        test_grammar_1.end_of_string,
        CFSymbol(TokenTag(")")),
        CFSymbol(TokenTag("+")),
    ],
    CFSymbol("T'"): [
        test_grammar_1.end_of_string,
        CFSymbol(TokenTag(")")),
        CFSymbol(TokenTag("+")),
    ],
    CFSymbol("F"): [
        test_grammar_1.end_of_string,
        CFSymbol(TokenTag(")")),
        CFSymbol(TokenTag("+")),
        CFSymbol(TokenTag("*")),
    ],
}

expected_table_1 = {
    # Entry for Non-terminal E
    (CFSymbol("E")): {
        (CFSymbol(TokenTag("id"))): CFProduction(
            CFSymbol("E"), [CFSymbol("T"), CFSymbol("E'")]
        ),
        (CFSymbol(TokenTag("("))): CFProduction(
            CFSymbol("E"), [CFSymbol("T"), CFSymbol("E'")]
        ),
    },
    # Entry for Non-terminal E'
    (CFSymbol("E'")): {
        (CFSymbol(TokenTag("+"))): CFProduction(
            CFSymbol("E'"), [CFSymbol(TokenTag("+")), CFSymbol("T"), CFSymbol("E'")]
        ),
        (CFSymbol(TokenTag(")"))): CFProduction(
            CFSymbol("E'"), [CFSymbol(None)]
        ),  # Represents ε
        (CFSymbol("$")): CFProduction(CFSymbol("E'"), [CFSymbol(None)]),  # Represents ε
    },
    # Entry for Non-terminal T
    (CFSymbol("T")): {
        (CFSymbol(TokenTag("id"))): CFProduction(
            CFSymbol("T"), [CFSymbol("F"), CFSymbol("T'")]
        ),
        (CFSymbol(TokenTag("("))): CFProduction(
            CFSymbol("T"), [CFSymbol("F"), CFSymbol("T'")]
        ),
    },
    # Entry for Non-terminal T'
    (CFSymbol("T'")): {
        (CFSymbol(TokenTag("*"))): CFProduction(
            CFSymbol("T'"), [CFSymbol(TokenTag("*")), CFSymbol("F"), CFSymbol("T'")]
        ),
        (CFSymbol(TokenTag("+"))): CFProduction(
            CFSymbol("T'"), [CFSymbol(None)]
        ),  # Represents ε
        (CFSymbol(TokenTag(")"))): CFProduction(
            CFSymbol("T'"), [CFSymbol(None)]
        ),  # Represents ε
        (CFSymbol("$")): CFProduction(CFSymbol("T'"), [CFSymbol(None)]),  # Represents ε
    },
    # Entry for Non-terminal F
    (CFSymbol("F")): {
        (CFSymbol(TokenTag("id"))): CFProduction(
            CFSymbol("F"), [CFSymbol(TokenTag("id"))]
        ),
        (CFSymbol(TokenTag("("))): CFProduction(
            CFSymbol("F"),
            [CFSymbol(TokenTag("(")), CFSymbol("E"), CFSymbol(TokenTag(")"))],
        ),
    },
}
test_token_seq_1 = [
    Token(TokenTag("id"), None),
    Token(TokenTag("+"), None),
    Token(TokenTag("("), None),
    Token(TokenTag("id"), None),
    Token(TokenTag("*"), None),
    Token(TokenTag("id"), None),
    Token(TokenTag(")"), None),
]

expected_derivations_1 = [
    CFProduction(CFSymbol("E"), [CFSymbol("T"), CFSymbol("E'")]),
    CFProduction(CFSymbol("T"), [CFSymbol("F"), CFSymbol("T'")]),
    CFProduction(CFSymbol("F"), [CFSymbol(TokenTag("id"))]),
    CFProduction(CFSymbol("T'"), [test_grammar_1.epsilon]), 
    CFProduction(CFSymbol("E'"), [CFSymbol(TokenTag("+")), CFSymbol("T"), CFSymbol("E'")]),
    CFProduction(CFSymbol("T"), [CFSymbol("F"), CFSymbol("T'")]),
    CFProduction(CFSymbol("F"), [CFSymbol(TokenTag("(")), CFSymbol("E"), CFSymbol(TokenTag(")"))]),
    CFProduction(CFSymbol("E"), [CFSymbol("T"), CFSymbol("E'")]),
    CFProduction(CFSymbol("T"), [CFSymbol("F"), CFSymbol("T'")]),
    CFProduction(CFSymbol("F"), [CFSymbol(TokenTag("id"))]),
    CFProduction(CFSymbol("T'"), [CFSymbol(TokenTag("*")), CFSymbol("F"), CFSymbol("T'")]),
    CFProduction(CFSymbol("F"), [CFSymbol(TokenTag("id"))]),
    CFProduction(CFSymbol("T'"), [test_grammar_1.epsilon]),
    CFProduction(CFSymbol("E'"), [test_grammar_1.epsilon]),
    CFProduction(CFSymbol("T'"), [test_grammar_1.epsilon]),
    CFProduction(CFSymbol("E'"), [test_grammar_1.epsilon])
]


# S -> A
# A -> B A'
# A' -> + B A'
# A' -> eps
# B -> C B'
# B' -> * C B'
# B' -> eps
# C -> ( A )
# C -> id
test_grammar_2 = CFGrammar(
    [
        CFProduction(CFSymbol("S"), [CFSymbol("A")]),
        CFProduction(CFSymbol("A"), [CFSymbol("B"), CFSymbol("A'")]),
        CFProduction(
            CFSymbol("A'"), [CFSymbol(TokenTag("+")), CFSymbol("B"), CFSymbol("A'")]
        ),
        CFProduction(CFSymbol("A'"), [CFSymbol(None)]),
        CFProduction(CFSymbol("B"), [CFSymbol("C"), CFSymbol("B'")]),
        CFProduction(
            CFSymbol("B'"), [CFSymbol(TokenTag("*")), CFSymbol("C"), CFSymbol("B'")]
        ),
        CFProduction(CFSymbol("B'"), [CFSymbol(None)]),
        CFProduction(
            CFSymbol("C"),
            [CFSymbol(TokenTag("(")), CFSymbol("A"), CFSymbol(TokenTag(")"))],
        ),
        CFProduction(CFSymbol("C"), [CFSymbol(TokenTag("id"))]),
    ],
    CFSymbol("S"),
    CFSymbol(None),
    CFSymbol("$"),
)

expected_first_2 = {
    CFSymbol("S"): [CFSymbol(TokenTag("(")), CFSymbol(TokenTag("id"))],
    CFSymbol("A"): [CFSymbol(TokenTag("(")), CFSymbol(TokenTag("id"))],
    CFSymbol("A'"): [CFSymbol(TokenTag("+")), CFSymbol(None)],
    CFSymbol("B"): [CFSymbol(TokenTag("(")), CFSymbol(TokenTag("id"))],
    CFSymbol("B'"): [CFSymbol(TokenTag("*")), CFSymbol(None)],
    CFSymbol("C"): [CFSymbol(TokenTag("(")), CFSymbol(TokenTag("id"))],
    test_grammar_2.epsilon: [test_grammar_2.epsilon],
}
for terminal in get_terminals(test_grammar_2.productions):
    expected_first_2[terminal] = [terminal]

expected_follow_2 = {
    CFSymbol("S"): [test_grammar_2.end_of_string],
    CFSymbol("A"): [CFSymbol(TokenTag(")")), test_grammar_2.end_of_string],
    CFSymbol("A'"): [CFSymbol(TokenTag(")")), test_grammar_2.end_of_string],
    CFSymbol("B"): [
        CFSymbol(TokenTag("+")),
        CFSymbol(TokenTag(")")),
        test_grammar_2.end_of_string,
    ],
    CFSymbol("B'"): [
        CFSymbol(TokenTag("+")),
        CFSymbol(TokenTag(")")),
        test_grammar_2.end_of_string,
    ],
    CFSymbol("C"): [
        CFSymbol(TokenTag("+")),
        CFSymbol(TokenTag("*")),
        CFSymbol(TokenTag(")")),
        test_grammar_2.end_of_string,
    ],
}

expected_table_2 = {
    # Entry for Non-terminal S
    (CFSymbol("S")): {
        (CFSymbol(TokenTag("id"))): CFProduction(CFSymbol("S"), [CFSymbol("A")]),
        (CFSymbol(TokenTag("("))): CFProduction(CFSymbol("S"), [CFSymbol("A")]),
    },
    # Entry for Non-terminal A
    (CFSymbol("A")): {
        (CFSymbol(TokenTag("id"))): CFProduction(
            CFSymbol("A"), [CFSymbol("B"), CFSymbol("A'")]
        ),
        (CFSymbol(TokenTag("("))): CFProduction(
            CFSymbol("A"), [CFSymbol("B"), CFSymbol("A'")]
        ),
    },
    # Entry for Non-terminal A'
    (CFSymbol("A'")): {
        (CFSymbol(TokenTag("+"))): CFProduction(
            CFSymbol("A'"), [CFSymbol(TokenTag("+")), CFSymbol("B"), CFSymbol("A'")]
        ),
        (CFSymbol(TokenTag(")"))): CFProduction(
            CFSymbol("A'"), [CFSymbol(None)]
        ),  # Represents ε
        (CFSymbol("$")): CFProduction(CFSymbol("A'"), [CFSymbol(None)]),  # Represents ε
    },
    # Entry for Non-terminal B
    (CFSymbol("B")): {
        (CFSymbol(TokenTag("id"))): CFProduction(
            CFSymbol("B"), [CFSymbol("C"), CFSymbol("B'")]
        ),
        (CFSymbol(TokenTag("("))): CFProduction(
            CFSymbol("B"), [CFSymbol("C"), CFSymbol("B'")]
        ),
    },
    # Entry for Non-terminal B'
    (CFSymbol("B'")): {
        (CFSymbol(TokenTag("*"))): CFProduction(
            CFSymbol("B'"), [CFSymbol(TokenTag("*")), CFSymbol("C"), CFSymbol("B'")]
        ),
        (CFSymbol(TokenTag("+"))): CFProduction(
            CFSymbol("B'"), [CFSymbol(None)]
        ),  # Represents ε
        (CFSymbol(TokenTag(")"))): CFProduction(
            CFSymbol("B'"), [CFSymbol(None)]
        ),  # Represents ε
        (CFSymbol("$")): CFProduction(CFSymbol("B'"), [CFSymbol(None)]),  # Represents ε
    },
    # Entry for Non-terminal C
    (CFSymbol("C")): {
        (CFSymbol(TokenTag("id"))): CFProduction(
            CFSymbol("C"), [CFSymbol(TokenTag("id"))]
        ),
        (CFSymbol(TokenTag("("))): CFProduction(
            CFSymbol("C"),
            [CFSymbol(TokenTag("(")), CFSymbol("A"), CFSymbol(TokenTag(")"))],
        ),
    },
}


def test_first_1():
    first_sets = extract_LL1_first_sets(test_grammar_1)

    print("FIRST sets:")
    for sym, first in first_sets.items():
        print(f"{sym.value}: {[s.value for s in first]}")

    # compare first sets and expected first sets
    assert set(first_sets.keys()) == set(expected_first_1.keys())
    for symbol in first_sets:
        assert set(first_sets[symbol]) == set(expected_first_1[symbol])


def test_follow_1():
    follow_sets = extract_LL1_follow_sets(test_grammar_1, expected_first_1)

    print("\nFOLLOW sets:")
    for sym, follow in follow_sets.items():
        print(f"{sym.value}: {[s.value for s in follow]}")

    assert set(follow_sets.keys()) == set(expected_follow_1.keys())
    for symbol in follow_sets:
        assert set(follow_sets[symbol]) == set(expected_follow_1[symbol])


def test_table_1():
    table = build_LL1_table(test_grammar_1, expected_first_1, expected_follow_1)
    assert set(expected_table_1.keys()) == set(table.keys())
    for non_terminal in expected_table_1:
        expected = set(expected_table_1[non_terminal].keys())
        observed = set(table[non_terminal].keys())
        assert expected == observed
        for terminal in expected_table_1[non_terminal]:
            assert (
                expected_table_1[non_terminal][terminal]
                == table[non_terminal][terminal]
            )

def test_parse_1():
    derivation_seq = get_LL1_derivation_seq(test_token_seq_1, test_grammar_1, expected_table_1)
    assert derivation_seq == expected_derivations_1

def test_syntax_node_parse_1():
    root_syntax_node = generate_syntax_tree_symbols(expected_derivations_1, test_grammar_1)
    assert True
    
    

def test_first_2():
    first_sets = extract_LL1_first_sets(test_grammar_2)

    print("FIRST sets:")
    for sym, first in first_sets.items():
        print(f"{sym.value}: {[s.value for s in first]}")

    # compare first sets and expected first sets
    assert set(first_sets.keys()) == set(expected_first_2.keys())
    for symbol in first_sets:
        assert set(first_sets[symbol]) == set(expected_first_2[symbol])


def test_follow_2():
    follow_sets = extract_LL1_follow_sets(test_grammar_2, expected_first_2)

    print("\nFOLLOW sets:")
    for sym, follow in follow_sets.items():
        print(f"{sym.value}: {[s.value for s in follow]}")

    assert set(follow_sets.keys()) == set(expected_follow_2.keys())
    for symbol in follow_sets:
        assert set(follow_sets[symbol]) == set(expected_follow_2[symbol])


def test_table_2():
    table = build_LL1_table(test_grammar_2, expected_first_2, expected_follow_2)
    assert set(expected_table_2.keys()) == set(table.keys())
    for non_terminal in expected_table_2:
        expected = set(expected_table_2[non_terminal].keys())
        observed = set(table[non_terminal].keys())
        assert expected == observed
        for terminal in expected_table_2[non_terminal]:
            assert (
                expected_table_2[non_terminal][terminal]
                == table[non_terminal][terminal]
            )


    