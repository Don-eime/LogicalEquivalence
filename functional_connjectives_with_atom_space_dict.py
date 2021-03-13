from collections import Callable
from functools import partial
from typing import Tuple


def negation(statements: Tuple[bool]) -> bool:
    """ Simple negation.
    Given a tuple of one bool and not just a bool for uniformity with two-sided connective functions"""
    assert len(statements) == 1
    return not statements[0]


def conjunction(statements: Tuple[bool]):
    assert len(statements) == 2
    return statements[0] and statements[1]


def disjunction(statements: Tuple[bool]):
    assert len(statements) == 2
    return statements[0] or statements[1]


def evaluate_connective_in_atom_space(connective: Callable, atom_space: dict, keys: tuple):
    statement_values = tuple(atom_space[key] for key in keys)
    return connective(statement_values)


def spaceless_connective_of_symbols(connective: Callable, symbols: tuple):
    return partial(evaluate_connective_in_atom_space, connective, keys=symbols)


def atom_space_dictionary(symbols, values):
    """ An atom_space dictionary is merely a dictionary with symbols as keys, and bools as values.
        The purpose of a atom_space dictionaries is substitute different symbol-value mappings into the same expression

        :return: dict
        """
    if len(symbols) != len(values):
        raise ValueError('Symbols and values given in construction of an atom_space_dict, '
                         'must be of same length')

    atom_space = {}
    for symbol, value in zip(symbols, values):
        atom_space[symbol] = value
    return atom_space


def misc_testing():
    symbols = {'p', 'q', 'r'}
    values = (True, False, False)
    A = atom_space_dictionary(symbols, values)
    B = atom_space_dictionary(symbols, [True, True, True])
    neg_p = evaluate_connective_in_atom_space(negation, A, ('p',))
    p_or_q = evaluate_connective_in_atom_space(disjunction, A, ('p', 'q'))
    spaceless_negate_p = spaceless_connective_of_symbols(negation, ('p',))
    spaceless_conjoin_pq = spaceless_connective_of_symbols(conjunction, ('p', 'q'))

