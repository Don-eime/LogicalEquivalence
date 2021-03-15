import itertools
from abc import ABC, abstractmethod, abstractproperty
from collections import Callable
from typing import List, Tuple, Union

from functional_connjectives_with_atom_space_dict import negation, conjunction, disjunction
import networkx as nx
import matplotlib as plt

AND_SYMBOL = '∧'
NOT_SYMBOL = '~'
OR_SYMBOL = '∨'
IMPLIES_SYMBOL = 'not defined'
CONNECTIVE_SYMBOLS = [AND_SYMBOL, NOT_SYMBOL, OR_SYMBOL, IMPLIES_SYMBOL]

JUNCTIONS = [conjunction, disjunction]
CONNECTIVE_SYMBOL_DICTIONARY = {negation: NOT_SYMBOL, conjunction: AND_SYMBOL, disjunction: OR_SYMBOL}

TAUTOLOGY_SYMBOL = 't'
CONTRADICTION_SYMBOL = 'c'
TAUTOLOGY_CONTRADICTION_SYMBOLS = [TAUTOLOGY_SYMBOL, CONTRADICTION_SYMBOL]

# atoms cannot be assigned a reserved symbol
RESERVED_SYMBOLS = CONNECTIVE_SYMBOLS + TAUTOLOGY_CONTRADICTION_SYMBOLS


class Statement(ABC):
    symbol: str

    statement_1: 'Statement'
    statement_2: 'Statement'
    connective: Callable

    @abstractmethod
    def value(self, atom_space: dict) -> bool:
        pass


class _Tautology(Statement):

    def __init__(self):
        self.symbol = TAUTOLOGY_SYMBOL

    @property
    def value(self, atom_space=None):
        return True


class _Contradiction(Statement):
    def __init__(self):
        self.symbol = CONTRADICTION_SYMBOL

    @property
    def value(self, atom_space=None):
        """ False regardless of atom_space"""
        return False


TAUTOLOGY = _Tautology()
CONTRADICTION = _Contradiction()


class Atom(Statement):
    def __init__(self, letter):

        if letter not in RESERVED_SYMBOLS:
            self.symbol = letter
        else:
            raise ValueError(f'An Atom cannot be assigned a reserved_symbol ({RESERVED_SYMBOLS}')

    def value(self, atom_space: dict) -> bool:
        value_in_atom_space = atom_space.get(self.symbol)
        if value_in_atom_space is not None:
            return value_in_atom_space
        else:
            raise ValueError('Symbol not found in atom_space')

    def __repr__(self):
        return 'Atom(%s)' % self.symbol


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

    def __repr__(self):
        return '<%s as Expression(%s, %s, %s)>' % (
            self.symbol, self.connective, self.statement_1, self.statement_2)

    def __eq__(self, other):
        if other.__class__ == Expression:
            other: Expression
            if self.connective == other.connective and self.statement_1 == other.statement_1 and self.statement_2 == other.statement_2:
                return True
            else:
                return False
        else:
            return False

    def comprised_statement_values(self, atom_space: dict) -> List[bool]:
        comprised_values = [self.statement_1.value(atom_space)]
        if self.statement_2:
            comprised_values.append(self.statement_2.value(atom_space))

        return comprised_values

    def value(self, atom_space: dict):
        comprised_statement_values = self.comprised_statement_values(atom_space)
        return self.connective(comprised_statement_values)

    @property
    def statements(self):
        statements = [statement for statement in [self.statement_1, self.statement_2] if not None]
        return statements

    @property
    def truth_table(self):
        return truth_table_of(self)

    @property
    def is_tautology(self):
        for row in self.truth_table:
            consequent_value = row[0]
            if not consequent_value:  # if there is a row that evaluates to False
                return False
        return True

    @property
    def is_contradiction(self):
        for row in self.truth_table:
            consequent_value = row[0]
            if consequent_value:  # if there is a row that evaluates to True
                return False
        return True


# UTIL FUNCTIONS

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

    return truth_table


def evaluate_connective_in_atom_space(connective: Callable, atom_space: dict, keys: tuple):
    statement_values = tuple(atom_space[key] for key in keys)
    return connective(statement_values)


def symbolic_representation_of_expression(expression: Expression):
    """ Given an expression, returns the symbolic representation of it.
                    e.g '(p ∧ q)' or '~p' or '(p ∧ q) ∧ r'

        Requires the expression to have AT LEAST a connective and an expression.
    """
    assert expression.connective and expression.statement_1
    if expression.statement_2:
        symbolic_representation = '(%s %s %s)' % (
            expression.statement_1.symbol, CONNECTIVE_SYMBOL_DICTIONARY[expression.connective],
            expression.statement_2.symbol)
    else:
        # only one statement, so this is a negation.
        symbolic_representation = '%s%s' % (
            CONNECTIVE_SYMBOL_DICTIONARY[expression.connective], expression.statement_1.symbol)

    return symbolic_representation


def permutations_of_atom_values(atoms):
    """Given a set of atoms, returns a list with all possible combinations of their True/False values"""
    atom_count = len(atoms)

    unique_true_false_combinations = [[True] * i + [False] * (atom_count - i) for i in range(0, atom_count + 1)]
    all_permutations = []
    for combination in unique_true_false_combinations:
        permutations = set(itertools.permutations(combination))
        all_permutations.extend(permutations)

    return all_permutations


# LAWS OF LOGICAL EQUIVALENCE
def junction_opposite(junction):
    """ Returns conjunction if given disjunction and vice-versa"""
    if junction == conjunction:
        return disjunction
    elif junction == disjunction:
        return conjunction


class LawOfEquivalence(ABC):

    @staticmethod
    @abstractmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    @abstractmethod
    def apply(expression: Expression):
        pass


class CommutativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if expression.connective in JUNCTIONS:
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return Expression(expression.connective, expression.statement_2, expression.statement_1)


class AssociativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if expression.connective in JUNCTIONS:
            if expression.statement_1.__class__ == Expression:
                if expression.statement_1.connective == expression.connective:
                    return True
        else:
            return False

    @staticmethod
    def apply(expression: Expression):
        """ Given (p AND q) AND r. Returns Returns p AND (q AND r) """
        new_left = expression.statement_1.statement_1  # p

        new_right = Expression(expression.connective,
                               expression.statement_1.statement_2,  # q
                               expression.statement_2)  # r

        return Expression(expression.connective, new_left, new_right)


class ReverseAssociativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if expression.connective in JUNCTIONS:
            if expression.statement_2.__class__ == Expression:
                if expression.statement_2.connective == expression.connective:
                    return True
        else:
            return False

    @staticmethod
    def apply(expression: Expression):
        """ Given p AND (q AND r). Returns (p AND q) AND r."""
        new_left = Expression(expression.connective,
                              expression.statement_1,  # p
                              expression.statement_2.statement_1)  # q

        new_right = expression.statement_2.statement_2  # r

        return Expression(expression.connective, new_left, new_right)


class DistributiveLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        """ Returns the eligibility of expression for application of the Distributive Law. p ∧ (q ∨ r) """
        if expression.connective in JUNCTIONS:
            # the expression is a junction
            if expression.statement_1.__class__ == Atom and expression.statement_2.__class__ == Expression:
                # the left statement is an atom and the right statement is another expression
                if expression.statement_2.connective == junction_opposite(expression.connective):
                    # the connective of the second statement is the opposite junction of the parameter expression
                    return True
        else:
            return False

    @staticmethod
    def apply(expression: Expression):
        new_left_side = Expression(expression.connective, expression.statement_1,
                                   expression.statement_2.statement_1)
        new_right_side = Expression(expression.connective, expression.statement_1,
                                    expression.statement_2.statement_2)

        return Expression(expression.statement_2.connective, new_left_side, new_right_side)


class IdentityLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if expression.connective in JUNCTIONS and expression.statement_2 in [TAUTOLOGY, CONTRADICTION]:
            # the expression is a junction and the second statement is either tautology or contradiction
            return True
        else:
            return False

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1


def is_junction(statement):
    if is_expression(statement) and statement.connective in JUNCTIONS:
        return True
    else:
        return False


def is_atom(statement):
    return True if statement.__class__ == Atom else False


def is_expression(statement):
    return True if statement.__class__ == Expression else False


def are_opposite_junctions(expression_1, expression_2):
    if not is_junction(expression_1) or not is_junction(expression_2):
        return False

    if expression_1.connective == junction_opposite(expression_2.connective):
        return True
    return False


def is_tautology_or_contradiction(statement):
    if statement.__class__ in [TAUTOLOGY, CONTRADICTION]:
        return True
    return False


def is_negation(statement):
    if is_expression(statement):
        if statement.connective == negation:
            return True
    return False


def is_double_negative(statement):
    if is_negation(statement) and is_negation(statement.statement_1):
        return True
    return False


class ReverseDistributiveLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        """
            Eligible if:
                connective and both statements are junctions AND
                both statement connectives are the opposite junction to the central one
        :param expression:
        :return:
        """
        if is_junction(expression) and is_junction(expression.statement_2) and is_junction(expression.statement_1):
            if are_opposite_junctions(expression, expression.statement_2):
                return True
        return False

    @staticmethod
    def apply(expression: Expression):
        new_left = expression.statement_1.statement_1
        new_right = Expression(expression.connective, expression.statement_1.statement_2,
                               expression.statement_2.statement_2)

        return Expression(expression.statement_1.connective, new_left, new_right)


class NegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_junction(expression) and is_tautology_or_contradiction(expression.statement_2):
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        if expression.connective == disjunction:
            return TAUTOLOGY
        elif expression.connective == conjunction:
            return CONTRADICTION


class DoubleNegativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_negation(expression) and is_negation(expression.statement_1):
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1.statement_1


class ReverseDoubleNegativeLaw(LawOfEquivalence):
    """ Gives ~(~(p)) from p. Likely unneeded."""

    @staticmethod
    def eligible(expression: Expression):
        if not is_negation(expression):
            # everything except negations are eligible
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return Expression(negation, Expression(negation, expression))


class IdempotentLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_junction(expression) and expression.statement_1 == expression.statement_2:
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1


class UniversalBoundLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_junction(expression) and is_tautology_or_contradiction(expression.statement_2):
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        if expression.connective == disjunction:
            return TAUTOLOGY
        elif expression.connective == conjunction:
            return CONTRADICTION


class DeMorgansLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_negation(expression) and is_junction(expression.statement_1):
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        negated_expression = expression.statement_1
        new_left_side = Expression(negation, negated_expression.statement_1)
        new_right_side = Expression(negation, negated_expression.statement_2)

        new_connective = junction_opposite(negated_expression.connective)

        de_morgans_product = Expression(new_connective, new_left_side, new_right_side)
        return de_morgans_product


class ReverseDeMorgansLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_junction(expression) and is_negation(expression.statement_1) and is_negation(expression.statement_2):
            return True

        return False

    @staticmethod
    def apply(expression: Expression):
        new_connective = junction_opposite(expression.connective)

        new_junction = Expression(new_connective, expression.statement_1.statement_1,
                                  expression.statement_2.statement_1)

        return Expression(negation, new_junction)


class AbsorptionLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_junction(expression):
            # must be junction
            if are_opposite_junctions(expression, expression.statement_2):
                # right statement must also be a junction, and junction oppsite to expression
                if expression.statement_2.statement_1 != expression.statement_2.statement_2:
                    # the right junction cannot be between the same to Atoms (so that this law doesn't apply 2 laws)
                    if expression.statement_2.statement_1 == expression.statement_1:
                        # the left statement of right statement must be the same as
                        # the left statement of parent expression
                        return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1


class ContradictionNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_negation(expression) and expression.statement_1 == CONTRADICTION:
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return TAUTOLOGY


class TautologyNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        if is_negation(expression) and expression.statement_1 == TAUTOLOGY:
            return True
        return False

    @staticmethod
    def apply(expression: Expression):
        return CONTRADICTION


ALL_EQUIVALENCE_LAWS = LawOfEquivalence.__subclasses__()


def all_eligible_laws_of(statement: Statement):
    return [law for law in ALL_EQUIVALENCE_LAWS if law.eligible(statement)]


def all_simple_equivalents(statement, is_inner_statement_of_expression=False):
    """ Returns all equivalent statements using only one application of a LawOfLogicalEquivalence to the outer most
            statement.
     """
    return [(law.apply(statement), law) for law in all_eligible_laws_of(statement)]


def all_equivalents_where_one_side_has_changed(statement: Statement):
    equivalents_where_one_side_has_changed = []

    # left side
    # get left equivalents
    equivalents_of_left_statement = all_simple_equivalents(statement.statement_1)

    # create expressions where
    equivalents_where_left_side_changes = [Expression(statement.connective, new_left_side, statement.statement_2)
                                           for new_left_side in equivalents_of_left_statement]
    equivalents_where_one_side_has_changed.extend(equivalents_where_left_side_changes)

    # right side
    if statement.statement_2:


        equivalents_of_right_statement = all_simple_equivalents(statement.statement_2)
        equivalents_where_left_side_changes = [Expression(statement.connective, new_right_side, statement.statement_2)
                                               for new_right_side in equivalents_of_right_statement]
        equivalents_where_one_side_has_changed.extend(equivalents_where_left_side_changes)




def unique_combinations_of_two_lists(list_1, list_2):
    # create empty list to store the combinations
    unique_combinations = []

    # Extract Combination Mapping in two lists
    # using zip() + product()
    unique_combinations = list(list(zip(list_1, element))
                               for element in itertools.product(list_2, repeat=len(list_1)))

    # printing unique_combination list
    return unique_combinations


class Create:

    @staticmethod
    def atom(symbol):
        return Atom(symbol)

    @staticmethod
    def conjunction(statement_1, statement_2):
        return Expression(conjunction, statement_1, statement_2)

    @staticmethod
    def disjunction(statement_1, statement_2):
        return Expression(disjunction, statement_1, statement_2)

    @staticmethod
    def negation(statement_1):
        return Expression(negation, statement_1)


# MAIN


def main():
    p = Atom('p')
    q = Atom('q')
    not_q = Create.negation(q)
    not_q_and_q = Create.conjunction(not_q, q)
    to_explore = Create.disjunction(p, not_q_and_q)

    equivs = 1  # search_for_path_between(to_explore)


class TestExpressions:
    def __init__(self):
        self.p = Atom('p')
        self.q = Atom('q')
        self.r = Atom('r')

        # general use negations
        self.not_p = Expression(negation, self.p)
        self.not_q = Expression(negation, self.q)
        self.not_r = Expression(negation, self.r)

        # general use conjunctions
        self.p_and_q = Expression(conjunction, self.p, self.q)
        self.q_and_p = Expression(conjunction, self.q, self.p)
        self.q_and_r = Expression(conjunction, self.q, self.r)

        # general use disjunctions
        self.p_or_q = Expression(disjunction, self.p, self.q)
        self.q_or_p = Expression(disjunction, self.q, self.p)
        self.q_or_r = Expression(disjunction, self.q, self.r)

        # for de morgans tests
        self.not_of_p_and_q = Expression(negation, self.p_and_q)
        self.not_p_or_not_q = Expression(disjunction, self.not_p, self.not_q)

        self.not_of_p_or_q = Expression(negation, self.p_or_q)
        self.not_p_and_not_q = Expression(conjunction, self.not_p, self.not_q)


if __name__ == 'main':
    pass  # main()

p = Atom('p')
q = Atom('q')

not_q = Create.negation(q)
not_q_and_q = Create.conjunction(not_q, q)

r = Atom('r')

complex = Create.conjunction(r,
                             Create.disjunction(p, q))
complex_equivalents = equivalent_statements_using_one_step(complex)
to_explore = Create.disjunction(p, not_q_and_q)


def find_equivalence_nodes_from(statement):
    edge_pairs = []
    laws_used = []
    eligible_law = all_eligible_laws_of(statement)
    for equivalence_law in eligible_law:
        print(equivalence_law)
        equivalent_statement = equivalence_law.apply(statement)
        edge_pairs.append((statement, equivalent_statement))
        laws_used.append(equivalence_law)

    return zip(edge_pairs, laws_used)


def search_for_path_between(first_statement, second_statement=None):
    layers = 5

    G = nx.Graph()

    nodes_to_search = [first_statement]
    new_nodes = []
    for current_node in nodes_to_search:
        new_node_edge_pairs = find_equivalence_nodes_from(current_node)

        for edge_pair, law_used in new_node_edge_pairs:
            G.add_edge(edge_pair, object=law_used)

        return G


not_not_q = Create.negation(not_q)
equiv_nodes = find_equivalence_nodes_from(not_not_q)

""" LOGICAL EQUIVALENCE REPRESENTED AS A GRAPH:
    Expressions can be expressed in a graph in which the edges between expressions indicate that the two connected
    expressions can be shown to be logically equivalent using ONE of the Laws of Logical Equivalence"""
