from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, List, TypedDict, Tuple, Dict
from types import SimpleNamespace


# Typed Dictionaries


# negate: Callable[[bool], bool] = lambda statement_1: not statement_1.truth_value
# conjoin: Callable[[bool], bool] = lambda statement_1, statement_2: statement_1.truth_value and statement_2.truth_value
# inclusive_disjoin: Callable[[bool], bool] = lambda statement_1, statement_2: statement_1.truth_value \
#                                                                              or statement_2.truth_value
#

# class Atom:
#     """ A statement variable, like p, ~p, q, p ∧ q, can either be True or False"""
#
#     def __init__(self, symbol: str, atom_space, value: bool = None):
#         self.symbol = symbol
#         self.space: AtomSpace = atom_space
#
#     @property
#     def value(self):
#         """ The value of an Atom is stored in its AtomSpace. Not in the Atom itself!"""
#         return self.space.atom_values[self.symbol]
#
#     def __str__(self):
#         return self.symbol
#
#     def __repr__(self):
#         return '<Atom: %s = %s>' % (self.symbol, self.value)
#
#
# class AtomSpace:
#     def __init__(self, symbols: set = None, values: Tuple[bool] = None):
#         """
#         An Atomspace is a mapping of symbols (str) to values. And symbols to Atoms. The Atoms do not store the values
#             themselves but retrieve them from their parent AtomSpace.
#
#
#         :param symbols (set): Set of symbols to add to the AtomSpace. Optional.
#         :param values (List[bool]), len must == len(symbols):  If symbols are given, a list of
#                                                                 Boolean values can be given to assign to them.
#         """
#
#         # PARAM CHECKING
#         if values and not symbols:
#             raise ValueError('An AtomSpace cannot be created with values but no symbols')
#         if symbols is not None and not isinstance(symbols, set):
#             raise ValueError('If symbols are given to an AtomSpace in construction, it must be a set.')
#         if symbols and values and len(symbols) != len(values):
#             raise ValueError('If symbols and values are given in construction of an AtomSpace, '
#                              'they must be of same length')
#
#         # ATTRIBUTE CREATION
#
#         # The 'atoms' Dict[str, Atom] maps symbols to their associated Atom.
#         # note that two Atoms cannot exist for the same symbol in one AtomSpace.
#         # the same letter can be used in two AtomSpaces however.
#         self.atoms: Dict[str, Atom] = {}
#
#         # The 'atom_values' Dict[str, bool] maps symbols to their truth value in this AtomSpace
#         self.atom_values: Dict[str, bool] = {}
#
#         if symbols:  # Create an Atom for each symbol and add the mapping of symbol to atom to the atoms dict
#             for symbol in symbols:
#                 self.atoms[symbol] = Atom(symbol, self)
#
#             if values:  # map the values to the symbol to value dict
#                 for symbol, value in zip(symbols, values):
#                     self.atom_values[symbol] = value
#
#     def __repr__(self):
#         return str(self.atoms)
#
#     def __str__(self):
#         return str(self.atoms)
#
class AtomSpace_dict(dict):
    def __init__(self, symbols: set = None, values: Tuple[bool] = None):
        """
        An AtomSpace is a mapping of symbols (str) to values. And symbols to Atoms. The Atoms do not store the values
            themselves but retrieve them from their parent AtomSpace.


        :param symbols (set): Set of symbols to add to the AtomSpace. Optional.
        :param values (List[bool]), len must == len(symbols):  If symbols are given, a list of
                                                                Boolean values can be given to assign to them.
        """

        # PARAM CHECKING
        if values and not symbols:
            raise ValueError('An AtomSpace cannot be created with values but no symbols')
        if symbols is not None and not isinstance(symbols, set):
            raise ValueError('If symbols are given to an AtomSpace in construction, it must be a set.')
        if symbols and values and len(symbols) != len(values):
            raise ValueError('If symbols and values are given in construction of an AtomSpace, '
                             'they must be of same length')

        for symbol, value in zip(symbols, values):
            self[symbol] = value
