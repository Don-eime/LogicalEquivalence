from unittest import TestCase
from logical_equivalence import *


TRUE_STATEMENT_p = Atom('p', True)
FALSE_STATEMENT_q = Atom('q', False)

class TestNegation(TestCase):
    def setUp(self) -> None:
        self.true_statement_p = Atom('p', True)
        self.false_statement_q = Atom('q', False)

    def test_negation_of_positive(self):
        # negation of True should be False
        self.assertFalse(Negation(self.true_statement_p).truth_value)

    def test_negation_of_false(self):
        # negation of False should be True
        self.assertTrue(Negation(self.false_statement_q).truth_value)

    def test_symbol(self):
        self.assertEqual(Negation(self.true_statement_p).__str__(), '~p')
        self.assertEqual(Negation(self.false_statement_q).__str__(), '~q')


class TestDisjunction(TestCase):
    def test_conjunction_true_true(self):
        self.assertTrue(Disjunction(TRUE_STATEMENT_p, TRUE_STATEMENT_p).truth_value)

    def test_conjunction_true_false(self):
        self.assertTrue(Disjunction(TRUE_STATEMENT_p, FALSE_STATEMENT_q).truth_value)

    def test_conjunction_false_true(self):
        self.assertTrue(Disjunction(FALSE_STATEMENT_q, TRUE_STATEMENT_p).truth_value)

    def test_conjunction_false_false(self):
        self.assertFalse(Disjunction(FALSE_STATEMENT_q, FALSE_STATEMENT_q).truth_value)

    def test_symbol(self):
        self.assertEqual(Disjunction(TRUE_STATEMENT_p, TRUE_STATEMENT_p).__str__(), 'p ' + OR_SYMBOL + ' p')


class TestConjunction(TestCase):
    def test_conjunction_true_true(self):
        self.assertTrue(Conjunction(TRUE_STATEMENT_p, TRUE_STATEMENT_p).truth_value)

    def test_conjunction_true_false(self):
        self.assertFalse(Conjunction(TRUE_STATEMENT_p, FALSE_STATEMENT_q).truth_value)

    def test_conjunction_false_true(self):
        self.assertFalse(Conjunction(FALSE_STATEMENT_q, TRUE_STATEMENT_p).truth_value)

    def test_conjunction_false_false(self):
        self.assertFalse(Conjunction(FALSE_STATEMENT_q, FALSE_STATEMENT_q).truth_value)


