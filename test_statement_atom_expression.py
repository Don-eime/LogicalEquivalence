from unittest import TestCase
from statement_atom_expression import *


class TestAtom(TestCase):
    def setUp(self) -> None:
        self.pq_TT = dict(zip(['p', 'q'], [True, True]))

    def test_value(self):
        p = Atom('p')
        self.assertTrue(p.value(self.pq_TT))
        with self.assertRaises(ValueError):
            p.value({'r': False})


class TestExpression(TestCase):
    def setUp(self) -> None:
        self.p = Atom('p')
        self.q = Atom('q')

        pq_TT = dict(zip(['p', 'q'], [True, True]))
        pq_TF = dict(zip(['p', 'q'], [True, False]))
        pq_FT = dict(zip(['p', 'q'], [False, True]))
        pq_FF = dict(zip(['p', 'q'], [False, False]))

        self.p_and_q = Expression(conjunction, Atom('p'), Atom('q'))
        self.p_or_q = Expression(disjunction, Atom('p'), Atom('q'))
        self.p_or_r = Expression(disjunction, Atom('p'), Atom('r'))
        self.complex_expression = Expression(conjunction, self.p_and_q, self.p_or_r)

    def test_comprised_atomic_symbols(self):
        self.assertEqual(comprised_atomic_symbols(self.complex_expression), ['p', 'q', 'p', 'r'])
        self.assertEqual(unique_atomic_symbols_in(self.complex_expression), ['p', 'q', 'r'])

    def test_truth_table_of_p_and_q(self):
        expected_truth_table_of_p_and_q = [({'p': False, 'q': False}, False),
                                           ({'p': True, 'q': False}, False),
                                           ({'p': False, 'q': True}, False),
                                           ({'p': True, 'q': True}, True)]
        self.assertEqual(truth_table_of(self.p_and_q), expected_truth_table_of_p_and_q)

    def test_truth_table_of_p_or_q(self):
        expected_truth_table_of_p_or_q = [({'p': False, 'q': False}, False),
                                          ({'p': True, 'q': False}, True),
                                          ({'p': False, 'q': True}, True),
                                          ({'p': True, 'q': True}, True)]

        self.assertEqual(truth_table_of(self.p_or_q), expected_truth_table_of_p_or_q)

    def test_truth_table_of_not_p(self):
        not_p = Expression(negation, Atom('p'))
        expected_truth_table_of_not_p = [({'p': False}, True),
                                         ({'p': True}, False)]

        self.assertEqual(not_p.truth_table, expected_truth_table_of_not_p)

    def test_equivalence_of_truth_tables(self):
        self.assertTrue(Expression(conjunction, self.p, self.q).truth_table ==
                        Expression(conjunction, self.q, self.p).truth_table)


class TestLawsOfEquivalence(TestCase):
    def __init__(self):
        self.p = Atom('p')
        self.q = Atom('q')
        self.r = Atom('r')


    def test_commutative_law(self):
        p_and_q = Expression(conjunction, self.p, self.q)
        q_and_p = Expression(conjunction, self.q, self.p)

        self.assertEqual(commutative_law(p_and_q), q_and_p)
        self.assertEqual(commutative_law(q_and_p), p_and_q)

    def test_associative_law(self):
        assert False

    def test_distributive_law(self):
        assert False

    def test_reverse_distributive_law(self):
        assert False

    def test_identity_law(self):
        assert False

    def test_negation_law(self):
        assert False

    def test_double_negative_law(self):
        assert False

    def test_idempotent_law(self):
        assert False

    def test_universal_bound_law(self):
        assert False

    def test_de_morgans_law(self):
        assert False

    def test_reverse_de_morgans_law(self):
        assert False

    def test_absorption_law(self):
        assert False

    def test_negation_of_tautology(self):
        assert False

    def test_negation_of_contradiction(self):
        assert False
