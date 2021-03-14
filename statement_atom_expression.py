import itertools
from abc import ABC, abstractmethod, abstractproperty
from collections import Callable
from typing import List, Tuple, Union

from functional_connjectives_with_atom_space_dict import negation, conjunction, disjunction

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
def junction_opposite(junction: Union[conjunction, disjunction]):
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
        pass

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
        pass

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1


class ReverseDistributiveLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        new_left = expression.statement_1.statement_1
        new_right = Expression(expression.connective, expression.statement_1.statement_2,
                               expression.statement_2.statement_2)

        return Expression(expression.statement_1.connective, new_left, new_right)


class NegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        if expression.connective == disjunction:
            return TAUTOLOGY
        elif expression.connective == conjunction:
            return CONTRADICTION


class ReverseNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        pass


class DoubleNegativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1.statement_1


class IdempotentLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1


class UniversalBoundLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        if expression.connective == disjunction:
            return TAUTOLOGY
        elif expression.connective == conjunction:
            return CONTRADICTION


class DeMorgansLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

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
        pass

    @staticmethod
    def apply(expression: Expression):
        new_connective = junction_opposite(expression.connective)

        new_junction = Expression(new_connective, expression.statement_1.statement_1,
                                  expression.statement_2.statement_1)

        return Expression(negation, new_junction)


class AbsorptionLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        return expression.statement_1


class ContradictionNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        return TAUTOLOGY


class TautologyNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(expression: Expression):
        pass

    @staticmethod
    def apply(expression: Expression):
        return CONTRADICTION


# MAIN


def main():
    pass


if __name__ == 'main':
    main()

""" LOGICAL EQUIVALENCE REPRESENTED AS A GRAPH:
    Expressions can be expressed in a graph in which the edges between expressions indicate that the two connected
    expressions can be shown to be logically equivalent using ONE of the Laws of Logical Equivalence"""
