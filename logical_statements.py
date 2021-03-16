import itertools
from abc import ABC, abstractmethod, abstractproperty
from collections import Callable
from typing import List, Tuple, Union

import networkx as nx
import matplotlib as plt

AND_SYMBOL = '∧'
NOT_SYMBOL = '~'
OR_SYMBOL = '∨'
IMPLIES_SYMBOL = '->'
CONNECTIVE_SYMBOLS = [AND_SYMBOL, NOT_SYMBOL, OR_SYMBOL, IMPLIES_SYMBOL]



TAUTOLOGY_SYMBOL = 't'
CONTRADICTION_SYMBOL = 'c'
TAUTOLOGY_CONTRADICTION_SYMBOLS = [TAUTOLOGY_SYMBOL, CONTRADICTION_SYMBOL]

# atoms cannot be assigned a reserved symbol
RESERVED_SYMBOLS = CONNECTIVE_SYMBOLS + TAUTOLOGY_CONTRADICTION_SYMBOLS


class Util:

    # STATEMENT TYPE CHECKING
    @staticmethod
    def is_general_tautology(statement):
        return True if statement.connective is ValueFunctions.tautology else False

    @staticmethod
    def is_general_contradiction(statement):
        return True if statement.connective is ValueFunctions.contradiction else False

    @staticmethod
    def is_atom(statement):
        return True if statement.connective is ValueFunctions.atom else False

    @staticmethod
    def is_tautology(statement):
        return True if statement.connective is ValueFunctions.negation else False

    @staticmethod
    def is_conjunction(statement):
        return True if statement.connective is ValueFunctions.conjunction else False

    @staticmethod
    def is_disjunction(statement):
        return True if statement.connective is ValueFunctions.disjunction else False

    @staticmethod
    def symbolic_representation_of_expression(statement: 'Statement'):
        """ Given an statement, returns the symbolic representation of it.
                        e.g '(p ∧ q)' or '~p' or '(p ∧ q) ∧ r'

            Requires the statement to have AT LEAST a connective and an statement.
        """
        # Tautology and Contradiction
        if Util.is_general_tautology(statement):
            return TAUTOLOGY_SYMBOL
        elif Util.is_general_contradiction(statement):
            return CONTRADICTION_SYMBOL

        if Util.is_conjunction(statement) or Util.is_disjunction(statement):
            return '(%s %s %s)' % (
                statement.left_term.symbol, Util.connective_symbol(statement),
                statement.right_term.symbol)
        else:
            # only one statement, so this is a negation.
            return '%s%s' % (
                Util.connective_symbol(statement), statement.left_term.symbol)

    @staticmethod
    def unique_atomic_symbols_in(statement) -> list:
        """ First gets every instance of all atomic symbols in the statement. Then converts to set.
            Returns ordered list of that set."""
        all_atomic_symbols = Util.comprised_atomic_symbols(statement)
        unique_atomic_symbols = list(set(all_atomic_symbols))
        return sorted(unique_atomic_symbols)

    @staticmethod
    def truth_table_of(statement):
        unique_atomic_symbols = Util.unique_atomic_symbols_in(statement)
        combinations_of_tf_for_all_symbols = Util.permutations_of_atom_values(unique_atomic_symbols)

        truth_table = []
        for tf_combination in combinations_of_tf_for_all_symbols:
            atom_space = dict(zip(unique_atomic_symbols, tf_combination))
            statement_value = statement.value(atom_space)
            truth_table.append((atom_space, statement_value))

        return truth_table

    @staticmethod
    def comprised_atomic_symbols(statement: 'Statement'):
        if not statement:
            return []
        if statement.is_atom:
            return [statement.symbol]
        else:
            return Util.comprised_atomic_symbols(statement.left_term) + Util.comprised_atomic_symbols(
                statement.right_term)

    @staticmethod
    def permutations_of_atom_values(atoms):
        """Given a set of atoms, returns a list with all possible combinations of their True/False values"""
        atom_count = len(atoms)

        unique_true_false_combinations = [[True] * i + [False] * (atom_count - i) for i in range(0, atom_count + 1)]
        all_permutations = []
        for combination in unique_true_false_combinations:
            permutations = set(itertools.permutations(combination))
            all_permutations.extend(permutations)

        return all_permutations

    @staticmethod
    def connective_symbol(statement: 'Statement'):
        connective = statement.connective
        if not statement.connective or statement.connective is ValueFunctions.tautology or \
                connective is ValueFunctions.contradiction:
            return None
        elif statement.connective == ValueFunctions.conjunction:
            return AND_SYMBOL
        elif statement.connective == ValueFunctions.disjunction:
            return OR_SYMBOL
        elif statement.connective == ValueFunctions.negation:
            return NOT_SYMBOL


# VALUE FUNCTIONS
class ValueFunctions:

    @staticmethod
    def atom(statement: 'Statement', atom_space: dict):
        value_in_atom_space = atom_space.get(statement.symbol)
        if value_in_atom_space is not None:
            return value_in_atom_space
        else:
            raise ValueError('Symbol not found in atom_space')

    @staticmethod
    def conjunction(statement: 'Statement', atom_space: dict):
        left_value = statement.left_term.value(atom_space)
        right_value = statement.right_term.value(atom_space)

        if left_value is not None and right_value is not None:
            return left_value and right_value
        else:
            raise ValueError('Symbols not found in atom_space')

    @staticmethod
    def disjunction(statement: 'Statement', atom_space: dict):
        left_value = statement.left_term.value(atom_space)
        right_value = statement.right_term.value(atom_space)

        if left_value is not None and right_value is not None:
            return left_value or right_value
        else:
            raise ValueError('Symbols not found in atom_space')

    @staticmethod
    def negation(statement: 'Statement', atom_space: dict):
        left_value = statement.left_term.value(atom_space)

        if left_value is not None:
            return not left_value
        else:
            raise ValueError('Symbols not found in atom_space')

    @staticmethod
    def tautology(*args):
        return True

    @staticmethod
    def contradiction(*args):
        return False


# CLASSES

class Statement:
    """ A statement can be an atom or an expression. Do not instantiate directly but use Create class"""

    def __init__(self, connective: Callable, left_term: 'Statement' = None, right_term: 'Statement' = None,
                 symbol=None, law_used_in_creation = None):
        # PARAM CHECK
        if connective == ValueFunctions.conjunction or connective == ValueFunctions.disjunction:
            assert right_term, 'A junction must be made with two terms'

        self._connective = connective
        self._left_term = left_term
        self._right_term = right_term

        self.is_atom = True if Util.is_atom(self) else False
        self.symbol = symbol if self.is_atom else Util.symbolic_representation_of_expression(self)

        self.law_used_in_creation = law_used_in_creation

        self._truth_table = None

    # GETTERS of private attributes
    @property
    def left_term(self):
        return self._left_term

    @property
    def right_term(self):
        return self._right_term

    @property
    def connective(self):
        return self._connective

    # VALUE and TTable
    def value(self, atom_space: dict) -> bool:
        return self._connective(self, atom_space)

    @property
    def truth_table(self):
        if self._truth_table:
            return self._truth_table
        else:
            self._truth_table = Util.truth_table_of(self)

    # MISC
    @property
    def terms(self):
        return [term for term in [self._left_term, self._right_term] if term]

    # DATA MODEL FUNCs
    def __repr__(self):
        if self.is_atom:
            return f'_Statement(symbol={self.symbol})'
        return '<Statement(%s, %s, %s) with symbol: %s>' % (self.connective,
                                                            self._left_term, self._right_term, self.symbol)

    def __eq__(self, other):
        if other.__class__ == Statement:
            if self._connective == other._connective and self.left_term == other.left_term and \
                    self.right_term == other.right_term and self.symbol == other.symbol:
                return True
            return False

    # Factory method
    def copy(self, new_connective=None, new_left_term=None, new_right_term=None, law_used_in_creation=None):
        connective = self._connective if new_connective is None else new_connective
        left_term = self.left_term if new_left_term is None else new_left_term
        right_term = self.right_term if new_right_term is None else new_right_term

        return Statement(connective, left_term, right_term, law_used_in_creation=law_used_in_creation)

# SPECIAL STATEMENT CONSTANT DEFINITIONS
TAUTOLOGY = Statement(connective=ValueFunctions.tautology)
CONTRADICTION = Statement(connective=ValueFunctions.contradiction)


class Create:
    @staticmethod
    def atom(symbol):
        return Statement(ValueFunctions.atom, symbol=symbol)

    @staticmethod
    def conjunction(left_term, right_term):
        return Statement(ValueFunctions.conjunction, left_term, right_term)

    @staticmethod
    def disjunction(left_term, right_term):
        return Statement(ValueFunctions.disjunction, left_term, right_term)

    @staticmethod
    def negation(left_term):
        return Statement(ValueFunctions.negation, left_term)
