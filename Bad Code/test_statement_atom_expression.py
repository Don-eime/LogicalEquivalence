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
    def setUp(self) -> None:
        # General use atoms
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

    def test_commutative_law(self):
        self.assertEqual(CommutativeLaw.apply(self.p_and_q).symbol, self.q_and_p.symbol)
        self.assertEqual(CommutativeLaw.apply(self.q_and_p).symbol, self.p_and_q.symbol)

    def test_commutative_eligibility(self):
        self.assertTrue(CommutativeLaw.eligible(self.p_and_q))
        self.assertTrue(CommutativeLaw.eligible(self.p_or_q))
        self.assertFalse(CommutativeLaw.eligible(self.not_p))


    def test_associative_law(self):
        associative_test_expression_AND = Expression(conjunction, self.p_and_q, self.r)
        expected_associative_result_1 = Expression(conjunction, self.p, self.q_and_r)

        associative_result_1 = AssociativeLaw.apply(associative_test_expression_AND)
        self.assertEqual(associative_result_1, expected_associative_result_1)

        associative_test_expression_OR = Expression(disjunction, self.p_or_q, self.r)
        expected_associative_result_2 = Expression(disjunction, self.p, self.q_or_r)
        associative_result_2 = AssociativeLaw.apply(associative_test_expression_OR)
        self.assertEqual(associative_result_2, expected_associative_result_2)

        self.assertTrue(AssociativeLaw.eligible(associative_test_expression_AND))
        self.assertTrue(AssociativeLaw.eligible(associative_test_expression_OR))
        self.assertFalse(AssociativeLaw.eligible(self.not_p))
        self.assertFalse(AssociativeLaw.eligible(self.not_p))

    def test_distributive_law(self):
        distributive_test_AND = Expression(conjunction, self.p,
                                           Expression(disjunction, self.q, self.r))
        out = Expression(disjunction,
                         Expression(conjunction, self.p, self.q),
                         Expression(conjunction, self.p, self.r))

        self.assertEqual(DistributiveLaw.apply(distributive_test_AND), out)

        distributive_test_OR = Expression(disjunction, self.p,
                                           Expression(conjunction, self.q, self.r))
        out = Expression(conjunction,
                         Expression(disjunction, self.p, self.q),
                         Expression(disjunction, self.p, self.r))

        self.assertEqual(DistributiveLaw.apply(distributive_test_OR), out)
        
        self.assertTrue(DistributiveLaw.eligible(distributive_test_AND))
        self.assertTrue(DistributiveLaw.eligible(distributive_test_OR))

    def test_reverse_distributive_law(self):
        or_in = Expression(disjunction,
                           Expression(conjunction, self.p, self.q),
                           Expression(conjunction, self.p, self.r))

        or_out = Expression(conjunction, self.p,
                            Expression(disjunction, self.q, self.r))

        self.assertEqual(ReverseDistributiveLaw.apply(or_in), or_out)

        and_in = Expression(conjunction,
                            Expression(disjunction, self.p, self.q),
                            Expression(disjunction, self.p, self.r))

        and_out = Expression(disjunction, self.p,
                             Expression(conjunction, self.q, self.r))

        self.assertEqual(ReverseDistributiveLaw.apply(and_in), and_out)

        self.assertTrue(ReverseDistributiveLaw.eligible(or_in))
        self.assertTrue(ReverseDistributiveLaw.eligible(and_in))

    def test_identity_law(self):
        identity_test_case_1 = Expression(conjunction, self.p, TAUTOLOGY)

        self.assertTrue(IdentityLaw.eligible(identity_test_case_1))

        self.assertEqual(IdentityLaw.apply(identity_test_case_1), self.p)
        self.assertEqual(IdentityLaw.apply(Expression(disjunction, self.p, CONTRADICTION)), self.p)

    def test_negation_law(self):
        p_or_not_p = Expression(disjunction, self.p, self.not_p)
        negation_law_product_1 = NegationLaw.apply(p_or_not_p)
        self.assertEqual(negation_law_product_1,
                         TAUTOLOGY)

        p_and_not_p = Expression(conjunction, self.p, self.not_p)
        negation_law_product_2 = NegationLaw.apply(p_and_not_p)
        self.assertEqual(negation_law_product_2,
                         CONTRADICTION)

        self.assertTrue(NegationLaw.eligible(p_or_not_p))
        self.assertTrue(NegationLaw.eligible(p_and_not_p))

    def test_double_negative_law(self):
        not_not_p = Expression(negation,
                               Expression(negation, self.p))

        self.assertEqual(DoubleNegativeLaw.apply(not_not_p), self.p)

        self.assertTrue(DoubleNegativeLaw.eligible(not_not_p))

    def test_idempotent_law(self):
        p_and_p = Expression(conjunction, self.p, self.p)
        self.assertEqual(IdempotentLaw.apply(p_and_p), self.p)

        p_or_p = Expression(disjunction, self.p, self.p)
        self.assertEqual(IdempotentLaw.apply(p_or_p), self.p)

        self.assertTrue(IdempotentLaw.eligible(p_and_p))
        self.assertTrue(IdempotentLaw.eligible(p_or_p))

    def test_universal_bound_law(self):
        p_or_t = Expression(disjunction, self.p, TAUTOLOGY)
        self.assertEqual(UniversalBoundLaw.apply(p_or_t), TAUTOLOGY)

        p_and_c = Expression(conjunction, self.p, CONTRADICTION)
        self.assertEqual(UniversalBoundLaw.apply(p_and_c), CONTRADICTION)

        self.assertTrue(UniversalBoundLaw.eligible(p_or_t))
        self.assertTrue(UniversalBoundLaw.eligible(p_and_c))

    def test_de_morgans_law(self):
        self.assertEqual(DeMorgansLaw.apply(self.not_of_p_and_q), self.not_p_or_not_q)
        self.assertEqual(DeMorgansLaw.apply(self.not_of_p_or_q), self.not_p_andp_not_q)

        self.assertTrue(DeMorgansLaw.eligible(self.not_of_p_and_q))
        self.assertTrue(DeMorgansLaw.eligible(self.not_of_p_or_q))

    def test_reverse_de_morgans_law(self):
        self.assertEqual(ReverseDeMorgansLaw.apply(self.not_p_or_not_q), self.not_of_p_and_q)
        self.assertEqual(ReverseDeMorgansLaw.apply(self.not_p_and_not_q), self.not_of_p_or_q)

        self.assertTrue(ReverseDeMorgansLaw.eligible(self.not_p_or_not_q))
        self.assertTrue(ReverseDeMorgansLaw.eligible(self.not_p_and_not_q))

    def test_absorption_law(self):
        p_disjunct_p_and_q = Expression(disjunction, self.p, self.p_and_q)
        self.assertEqual(AbsorptionLaw.apply(p_disjunct_p_and_q), self.p)

        p_conjunct_p_or_q = Expression(conjunction, self.p, self.p_or_q)
        self.assertEqual(AbsorptionLaw.apply(p_conjunct_p_or_q), self.p)

        eligibility_1 = AbsorptionLaw.eligible(p_disjunct_p_and_q)
        self.assertTrue(eligibility_1)
        self.assertTrue(AbsorptionLaw.eligible(p_conjunct_p_or_q))

    def test_negation_of_tautology(self):
        not_tautology = Expression(negation, TAUTOLOGY)
        self.assertEqual(TautologyNegationLaw.apply(not_tautology), CONTRADICTION)
        self.assertTrue(TautologyNegationLaw.eligible(not_tautology))


    def test_negation_of_contradiction(self):
        not_contradiction = Expression(negation, CONTRADICTION)
        self.assertEqual(ContradictionNegationLaw.apply(not_contradiction), TAUTOLOGY)
        self.assertTrue(ContradictionNegationLaw.eligible(not_contradiction))

    def test_find_all_eligible_laws(self):
        pass