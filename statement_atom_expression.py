import itertools
from collections import Callable
from typing import List, Tuple

from functional_connjectives_with_atom_space_dict import negation, conjunction, disjunction

AND_SYMBOL = '∧'
NEGATION_SYMBOL = '~'
OR_SYMBOL = '∨'
CONNECTIVE_CHARACTERS = {negation: NEGATION_SYMBOL, conjunction: AND_SYMBOL, disjunction: OR_SYMBOL}


class Statement:
    symbol: str


class Atom(Statement):
    def __init__(self, letter):
        self.symbol = letter

    def value(self, atom_space: dict):
        value = atom_space.get(self.symbol)
        if value is not None:
            return value
        else:
            raise ValueError('Symbol not found in atom_space')


class Expression(Statement):
    """ An expression is a type of statement that is composed of at least one statement and a connective.
            An expression can be evaluated with the value() function, given a specific atom_space that maps each
            unique atom in the expression to a Boolean.

            If the connective is not negation, it must have two statements.
            """

    def __init__(self, connective: Callable, statement_1: Statement, statement_2: Statement = None):
        # PARAM CHECKING
        if connective is not negation:
            assert statement_2

        self.connective = connective
        self.statement_1: Statement = statement_1
        self.statement_2: Statement = statement_2

        self.symbol = symbolic_representation_of_expression(self)

    def comprised_statement_values(self, atom_space: dict) -> List[bool]:
        comprised_values = [self.statement_1.value(atom_space)]
        if self.statement_2:
            comprised_values.append(self.statement_2.value(atom_space))

        return comprised_values

    def value(self, atom_space: dict) -> bool:
        comprised_statement_values = self.comprised_statement_values(atom_space)
        return self.connective(comprised_statement_values)

    @property
    def statements(self):
        statements = [statement for statement in [self.statement_1, self.statement_2] if not None]
        return statements

    @property
    def truth_table(self):
        return truth_table_of(self)

def comprised_atomic_symbols(statement):
    if not statement:
        return []
    elif statement.__class__ == Atom:
        return [statement.symbol]
    elif statement.__class__ == Expression:
        return comprised_atomic_symbols(statement.statement_1) + comprised_atomic_symbols(statement.statement_2)
    else:
        raise Exception(f'statement is not None but isn\'t Atom or Expression: type = {statement.__class__}')


def unique_atomic_symbols_in(statement) -> list:
    """ First gets every instance of all atomic symbols in the statement. Then converts to set.
        Returns ordered list of that set."""
    all_atomic_symbols = comprised_atomic_symbols(statement)
    unique_atomic_symbols = list(set(all_atomic_symbols))
    return sorted(unique_atomic_symbols)


def truth_table_of(expression):
    unique_atomic_symbols = unique_atomic_symbols_in(expression)
    combinations_of_tf_for_all_symbols = permutations_of_atom_values(unique_atomic_symbols)

    truth_table = []
    for tf_combination in combinations_of_tf_for_all_symbols:
        atom_space = dict(zip(unique_atomic_symbols, tf_combination))
        expression_value = expression.value(atom_space)
        truth_table.append((atom_space, expression_value))


# EVALUATION
def evaluate_connective_in_atom_space(connective: Callable, atom_space: dict, keys: tuple):
    statement_values = tuple(atom_space[key] for key in keys)
    return connective(statement_values)


# UTIL FUNCTIONS
def symbolic_representation_of_expression(expression: Expression):
    """ Given an expression, returns the symbolic representation of it.
                    e.g '(p ∧ q)' or '~p' or '(p ∧ q) ∧ r'

        Requires the expression to have AT LEAST a connective and an expression.
    """
    assert expression.connective and expression.statement_1
    if expression.statement_2:
        symbolic_representation = '(%s %s %s)' % (
            expression.statement_1.symbol, CONNECTIVE_CHARACTERS[expression.connective], expression.statement_2.symbol)
    else:
        # only one statement, so this is a negation.
        symbolic_representation = '%s%s' % (CONNECTIVE_CHARACTERS[expression.connective], expression.statement_1.symbol)

    return symbolic_representation

def truth_value_permutations(unique_atoms):
    atom_count = len(unique_atoms)
    rows = 2 ** atom_count

    columns = []
    row_number_divisor = 0.5
    atom_index = 0
    while atom_index <  atom_count - 1:
        row_values = [True] * int(rows * row_number_divisor) + [False] * int(rows * row_number_divisor)
        columns.append(row_values)
        row_number_divisor *= row_number_divisor
        atom_index += 1

    singleton_row = [True, False] * int(rows / 2)
    columns.append(singleton_row)
    return columns

def permutations_of_atom_values(atoms):
    """Given a set of atoms, returns a list with all possible combinations of their True/False values"""
    atom_count = len(atoms)

    unique_true_false_combinations = [[True]*i + [False]*(atom_count-i) for i in range(0,atom_count+1)]
    all_permutations = []
    for combination in unique_true_false_combinations:
        permutations = set(itertools.permutations(combination))
        all_permutations.extend(permutations)

    return all_permutations

def main():
    p = Atom('p')
    q = Atom('q')

    not_p = Expression(negation, p)
    p_and_q = Expression(conjunction, p, q)
    p_or_q = Expression(disjunction, p, q)

    pq_True_space = {'p': True, 'q': True}

    not_p_in_pqT_space = not_p.value(pq_True_space)

    p_and_q = Expression(conjunction, Atom('p'), Atom('q'))
    p_or_r = Expression(disjunction, Atom('p'), Atom('r'))
    complex_expression = Expression(conjunction, p_and_q, p_or_r)

    tt = truth_table_of(complex_expression)


if __name__ == 'main':
    main()
main()
""" LOGICAL EQUIVALENCE REPRESENTED AS A GRAPH:
    Expressions can be expressed in a graph in which the edges between expressions indicate that the two connected
    expressions can be shown to be logically equivalent using ONE of the Laws of Logical Equivalence"""
