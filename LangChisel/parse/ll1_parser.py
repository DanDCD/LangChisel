from LangChisel.lex.greedy_backtrack_lexer import Token, TokenTag
from enum import Enum
from dataclasses import dataclass
from typing import Callable

# TODO: move CF to new file


class CFSymbol:
    def __init__(self, value: str | TokenTag) -> None:
        """A Single Context Free Symbol

        Args:
            value (str): the name of the non-terminal or token of the terminal
        """
        self.value = value

    def __repr__(self) -> str:
        return f"(CFSymbol: {self.value})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CFSymbol):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash((self.value))


class CFProduction:
    def __init__(self, from_symbol: CFSymbol, to_sequence: list[CFSymbol]):
        """A Production Rule defining a possible transition from one symbol to a sequence of other symbols

        Args:
            from_symbol (CFSymbol): The 'left hand-side' of this derivation, what the derviation 'derives from'
            to_sequence (list[CFSymbol]): The 'right hand-side' of this derivation, what the derivation 'derives to'
        """
        self.from_symbol = from_symbol
        self.to_sequence = to_sequence

    def __repr__(self) -> str:
        return f"(CFProduction: {self.from_symbol} => {self.to_sequence})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CFProduction):
            return (
                self.from_symbol == other.from_symbol
                and self.to_sequence == other.to_sequence
            )
        return False

    def __hash__(self) -> int:
        return hash((self.from_symbol, self.to_sequence))


class CFGrammar:
    def __init__(
        self,
        productions: list[CFProduction],
        start_symbol: CFSymbol,
        epsilon: CFSymbol,
        end_of_string: CFSymbol,
    ):
        """A Context Free Grammar, defined by a series of productions, alongside  start symbol, epsilon, and end of string definitions"""
        self.productions = productions
        self.start_symbol = start_symbol
        self.epsilon = epsilon
        self.end_of_string = end_of_string


def get_non_terminals(derivations: list[CFProduction]) -> list[CFSymbol]:
    """ """
    return list(set([production.from_symbol for production in derivations]))


def get_terminals(derivations: list[CFProduction]) -> list[CFSymbol]:
    """ """
    terminals = []
    for production in derivations:
        for symbol in production.to_sequence:
            if is_terminal(symbol):
                terminals.append(symbol)
    return list(set(terminals))


def is_terminal(symbol: CFSymbol) -> bool:
    """ """
    return isinstance(symbol.value, TokenTag)


def LL1_first(
    symbol: CFSymbol,
    grammar: CFGrammar,
    known_first_sets: dict[CFSymbol, list[CFSymbol]],
):
    """Find the set of symbols that may appear at the start of a string derived from A
    That is, First(A) = { t | A->...->tW for some string w}
    First(A) will include epsilon, only if A can produce epsilon/the empty string as a complete derivation of A.

    Args:
        symbol (CFSymbol): the symbol we want the first set of
        grammar (list[CFProduction]): the grammar we will use to derive the first set
        known_first_sets (dict[CFSymbol, list[CFSymbol]]): a dictionary containing any pre-calculated first_sets - if empty, the function will simply calculate any dependency recursively - any newly calculated first-sets will be added to this dictionary
    """

    if symbol in known_first_sets:
        return known_first_sets[symbol]

    # definition for First(a) = {a}  OR First(epsilon) = {epsilon}
    if is_terminal(symbol) or symbol == grammar.epsilon:
        known_first_sets[symbol] = [symbol]
        return known_first_sets[symbol]

    first_set = set()  # this will be the set of 'First(symbol)' we will return
    relevant_productions = [
        production
        for production in grammar.productions
        if production.from_symbol == symbol
    ]

    for production in relevant_productions:
        to_sequence = production.to_sequence
        # should never have a production that does not contain a single derived symbol
        assert len(to_sequence) > 0

        # First(A) += First(B) + First(C) if (A -> B C) and (epsilon in B)
        # OR First(A) += First(B) if A -> A B
        for i, sym in enumerate(to_sequence):
            # add all terminals in First(X) other than epsilon
            first_of_sym = LL1_first(sym, grammar, known_first_sets)
            first_set.update(set(first_of_sym) - {grammar.epsilon})

            # if sym cannot derive epsilon, then we should not add the first of the next set (i.e. First(C)) to our first_set
            if not grammar.epsilon in first_of_sym:
                break

            # if we have reached the end of the to_sequence and (from above) first(X) contains epsilon, we add epsilon
            if i == len(to_sequence) - 1:
                first_set.add(grammar.epsilon)

    known_first_sets[symbol] = list(first_set)
    return list(first_set)


def extract_LL1_first_sets(
    grammar: CFGrammar,
) -> dict[CFSymbol, list[CFSymbol]]:
    """Calculate the First sets for all symbols in the grammar"""
    first_sets: dict[CFSymbol, list[CFSymbol]] = {}
    symbols = get_non_terminals(grammar.productions) + get_terminals(
        grammar.productions
    )

    for symbol in symbols:
        LL1_first(symbol, grammar, first_sets)

    return first_sets


def LL1_follow(
    symbol: CFSymbol,
    grammar: CFGrammar,
    known_first_sets: dict[CFSymbol, list[CFSymbol]],
    known_follow_sets: dict[CFSymbol, list[CFSymbol]],
):
    """Find the set of symbols that may appear a string derived from this symbol (Note: this does not mean 'at the end' of a derived string, but immediately after/next any derived string)
    That is, Follow(A) = { t | S ->...-> aAtw for some a, w}, where S is the start symbol
    """
    if symbol in known_follow_sets:
        return known_follow_sets[symbol]

    follow_set = set()
    # if symbol is start symbol, add $ (the end of string symbol)
    if symbol == grammar.start_symbol:
        follow_set.add(grammar.end_of_string)

    # this time, relevant productions for symbol A, are those where X -> "..."A"..."
    relevant_productions = [
        production
        for production in grammar.productions
        if symbol in production.to_sequence
    ]

    for production in relevant_productions:
        # from_symbol -> to_sequence
        from_symbol = production.from_symbol
        to_sequence = production.to_sequence

        # find all occurrences of the symbol in this production
        positions = [i for i, sym in enumerate(to_sequence) if sym == symbol]
        for symbol_pos in positions:
            # Follow(A) += Follow(B) if B -> w A and B != A
            if symbol_pos == len(to_sequence) - 1:
                if from_symbol != symbol:
                    follow_set.update(
                        LL1_follow(
                            from_symbol, grammar, known_first_sets, known_follow_sets
                        )
                    )
                continue  # we are now finished with this derivation, so go to the next

            # Follow(A) += First(B) if W -> A B C
            # Follow(A) += First(C) if W -> A B C and First(B) has epsilon
            curr_pos = symbol_pos
            epsilon_in_curr_first = True
            while epsilon_in_curr_first and curr_pos < len(to_sequence) - 1:
                curr_pos += 1
                if curr_pos in positions:
                    break  # if we have reached another intance of the symbol, we can just continue to it in the outer loop
                # we can add the first set (i.e. First(B)) to the follow set of our symbol (i.e. follow(A))
                first_curr = known_first_sets[to_sequence[curr_pos]]
                follow_set.update(set(first_curr) - {grammar.epsilon})
                # if this has epsilon, then we have Follow(A) += First(C) if W -> A B C and First(B) has epsilon
                epsilon_in_curr_first = grammar.epsilon in first_curr

                # if this is also the last symbol in the sequence, we get Follow(A) += Follow(B) if B -> a A w, and eps in First(w)
                if curr_pos == len(to_sequence) - 1 and epsilon_in_curr_first:
                    follow_set.update(
                        LL1_follow(
                            from_symbol, grammar, known_first_sets, known_follow_sets
                        )
                    )

    known_follow_sets[symbol] = list(follow_set)
    return list(follow_set)


def extract_LL1_follow_sets(
    grammar: CFGrammar, first_sets: dict[CFSymbol, list[CFSymbol]]
) -> dict:
    follow_sets: dict[CFSymbol, list[CFSymbol]] = {}
    symbols = get_non_terminals(
        grammar.productions
    )  # we only define follow for non-terminals

    for symbol in symbols:
        LL1_follow(symbol, grammar, first_sets, follow_sets)

    return follow_sets


def build_LL1_table(
    grammar: CFGrammar,
    first_sets: dict[CFSymbol, list[CFSymbol]],
    follow_sets: dict[CFSymbol, list[CFSymbol]],
) -> dict[CFSymbol, dict[CFSymbol, CFProduction]]:
    """Construct an LL(1) Parse Table given a grammar, first_sets, and follow_sets"""

    # our table is a mapping of (non-terminal, terminal) -> production the parser should use when terminal is front of input and non-terminal top of stack
    ll1_table: dict[CFSymbol, dict[CFSymbol, CFProduction]] = {}

    for production in grammar.productions:

        if production.from_symbol not in ll1_table:
            ll1_table[production.from_symbol] = {}

        # we keep adding to the first set, by iterating over symbols and fetching their first sets until we stop getting: (first(symbol) has epsilon)
        first_set = set()
        for symbol in production.to_sequence:
            first_set.update(first_sets[symbol])
            if grammar.epsilon not in first_sets[symbol]:
                break
        # for every terminal in the first set, we assert that (non-terminal, terminal -> production) does not already exist
        # if we are correct, we add the mapping and repeat
        for terminal in first_set - {grammar.epsilon}:
            if terminal not in ll1_table[production.from_symbol]:
                ll1_table[production.from_symbol][terminal] = production
            else:
                raise ValueError(
                    f"Conflict in LL(1) table at {production.from_symbol}, {terminal}"
                )
        # if the first set contains epsilong (i.e. every symbol in the production can derive epsilon)
        # we now know that the whole production can be used to derive eps
        if grammar.epsilon in first_set:
            for terminal in follow_sets[production.from_symbol]:
                if terminal not in ll1_table[production.from_symbol]:
                    ll1_table[production.from_symbol][terminal] = production
                else:
                    raise ValueError(
                        f"Conflict in LL(1) table at {production.from_symbol}, {terminal}"
                    )

    return ll1_table


class ParseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        if self.position:
            return f"Parse Error Raised: {self.message}"
        return self.message


def get_LL1_derivation_seq(
    tokens: list[Token],
    grammar: CFGrammar,
    parse_table: dict[CFSymbol, dict[CFSymbol, CFProduction]],
) -> list[CFProduction]:
    stack: list[CFSymbol] = [grammar.end_of_string, grammar.start_symbol]
    tokens.append(Token(grammar.end_of_string.value, None))
    tokens.reverse()

    derivation_sequence: list[CFProduction] = []

    while stack[-1] != grammar.end_of_string:
        symbol: CFSymbol = stack[-1]
        token: Token = tokens[-1]
        token_sym: CFSymbol = CFSymbol(token.tag)

        if symbol == grammar.epsilon:
            stack.pop()
        elif is_terminal(symbol) and symbol.value == token.tag:
            stack.pop()
            tokens.pop()
        elif symbol in parse_table and token_sym in parse_table[symbol]:
            derivation: CFProduction = parse_table[symbol][token_sym]
            assert symbol == derivation.from_symbol
            to_seq = derivation.to_sequence.copy()
            to_seq.reverse()

            stack.pop()
            stack += to_seq
            derivation_sequence.append(derivation)
        else:
            raise ParseError("No Valid Next Step for Parser")
    return derivation_sequence


# TODO: move to new file
# Below we are no longer tied to being LL1


class SyntaxNode:
    def __init__(
        self,
        symbol: CFSymbol,
        token: Token = None,
        connection_symbols: list[CFSymbol] = [],
        connection_nodes: list["SyntaxNode"] = [],
    ):
        """A SyntaxNode describes a node in a tree generated by some parsing step. The Syntax Node will contain a CFSymbol to identify its grammatical class, alongside a token to define exactly what it is representing (in both sub-type and value)

        Args:
            symbol (CFSymbol): the context free grammar symbol of this Node
            token (Token): a token (if any) that contains the actual lexed token for this Node
            connection_symbols (list[CFSymbol]): an ordered list of the CFSymbols this SyntaxNode wants to connect to
            connection_nodes (list[SyntaxNode]): an ordered list of nodes that this SyntaxNode has connected to - connection_nodes[i] is the connection for connection_symbols[i] - due to left-most connections, we can assume that len(connection_nodes) <= len(connection_symbols)
        """
        self.symbol = symbol
        self.token = token
        self.connection_symbols = connection_symbols
        self.connection_nodes = connection_nodes

    def __repr__(self):
        return f"(SyntaxNode: symbol:{self.symbol}, token:{self.token}, connections:{self.connection_nodes})"
    
    

def parse_sequence(
    tokens: list[Token], derivation_sequence: list[CFProduction]
) -> SyntaxNode:
    """Generate a Syntax Tree from a list of Tokens and a series of derivations"""

    def find_syntax_node_in_order(
        start_node: SyntaxNode, condition: Callable[[SyntaxNode], bool]
    ) -> SyntaxNode:
        """Helper function for descending the tree in depth-first, left-to-right order until we find a node meeting 'condition'"""
        # for each child, check if it or a grandchild matches condition
        for child_node in start_node.connection_nodes:
            exploration = find_syntax_node_in_order(child_node, condition)
            if exploration:
                return exploration
        # if no children (or no children match), check condition against self
        if condition(start_node):
            return start_node
        return None

    assert derivation_sequence  # should not be getting empty sequence
    assert tokens
    
    tokens.reverse() # we reverse the tokens so we can just pop() the front off
    
    root_node = SyntaxNode(
        derivation_sequence[0].from_symbol, None, derivation_sequence[0].to_sequence, []
    )

    for derivation in derivation_sequence[1:]:
        # to map this derivation on our tree, we need to find where the transition takes place
        from_symbol: CFSymbol = derivation.from_symbol
        to_sequence: list[CFSymbol] = derivation.to_sequence

        # find deepest left most node with this derivation's 'from_symbol' as possible connection
        node_to_expand = find_syntax_node_in_order(
            root_node,
            lambda node: any(
                node.connection_symbols[i] == from_symbol
                and i >= len(node.connection_nodes)
                for i in range(len(node.connection_symbols))
            ),
        )

        # we assert that the next symbol this node can/wants to connect to is the from symbol of our derivation
        assert (
            node_to_expand.connection_symbols[len(node_to_expand.connection_nodes)]
            == from_symbol
        )
        # we can now add this node to the tree
        node_to_expand.connection_nodes.append(
            SyntaxNode(from_symbol, None, to_sequence, [])
        )

        # we now need to identify all terminal connections that have no SyntaxNode assigned and fill the connections
        # we look for the deepest left-most terminal each time
        def terminal_connection_needs_handling() -> SyntaxNode:
            """Helper function to check our tree for any open connection to a terminal CFSymbol

            Returns:
                parent (SyntaxNode): the parent node of the terminal
            """
            return find_syntax_node_in_order(
                root_node,
                lambda node: not (len(node.connection_symbols) == len(node.connection_nodes)) and is_terminal(
                     node.connection_symbols[len(node.connection_nodes)]
                ),
                # we are looking for a node where there is an outgoing terminal connection that has no node assigned
                # AND it is the next node that needs a connection
            )

        node_with_terminal = terminal_connection_needs_handling()
        while node_with_terminal:
            next_token: Token = tokens.pop()
            terminal_symbol: CFSymbol = node_with_terminal.connection_symbols[len(node_with_terminal.connection_nodes)]
            # if the next token in the input sequence is not expected from the derivation sequence, the two sequences are incompatible
            assert next_token.tag == terminal_symbol.value
            node_with_terminal.connection_nodes.append(SyntaxNode(terminal_symbol, next_token, [], []))
            node_with_terminal = terminal_connection_needs_handling()

    return root_node