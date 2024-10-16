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
    CFSymbol("T"): [test_grammar_1.end_of_string, CFSymbol(TokenTag(")")), CFSymbol(TokenTag("+"))],
    CFSymbol("T'"): [test_grammar_1.end_of_string, CFSymbol(TokenTag(")")), CFSymbol(TokenTag("+"))],
    CFSymbol("F"): [test_grammar_1.end_of_string, CFSymbol(TokenTag(")")), CFSymbol(TokenTag("+")), CFSymbol(TokenTag("*"))],
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
    follow_sets = extract_LL1_follow_sets(test_grammar_1, expected_follow_1)
    
    print("\nFOLLOW sets:")
    for sym, follow in follow_sets.items():
        print(f"{sym.value}: {[s.value for s in follow]}")
    
    assert set(follow_sets.keys()) == set(expected_follow_1.keys())
    for symbol in follow_sets:
        assert set(follow_sets[symbol]) == set(expected_follow_1[symbol])