import unittest
from logical_equivalence import *
from logical_statements import *


class TestLawsOfEquivalence(unittest.TestCase):
    def setUp(self) -> None:
        # General use atoms
        self.p = Create.atom('p')
        self.q = Create.atom('q')
        self.r = Create.atom('r')

        # general use negations
        self.not_p = Create.negation(self.p)
        self.not_q = Create.negation(self.q)
        self.not_r = Create.negation(self.r)

        # general use conjunctions
        self.p_and_q = Create.conjunction(self.p, self.q)
        self.q_and_p = Create.conjunction(self.q, self.p)
        self.q_and_r = Create.conjunction(self.q, self.r)

        # general use disjunctions
        self.p_or_q = Create.disjunction(self.p, self.q)
        self.q_or_p = Create.disjunction(self.q, self.p)
        self.q_or_r = Create.disjunction(self.q, self.r)

        # for de morgans tests
        self.not_of_p_and_q = Create.negation(self.p_and_q)
        self.not_p_or_not_q = Create.disjunction(self.not_p, self.not_q)

        self.not_of_p_or_q = Create.negation(self.p_or_q)
        self.not_p_and_not_q = Create.conjunction(self.not_p, self.not_q)

    def test_commutative_law(self):
        self.assertEqual(CommutativeLaw.apply(self.p_and_q).symbol, self.q_and_p.symbol)
        self.assertEqual(CommutativeLaw.apply(self.q_and_p).symbol, self.p_and_q.symbol)

    def test_commutative_eligibility(self):
        self.assertTrue(CommutativeLaw.eligible(self.p_and_q))
        self.assertTrue(CommutativeLaw.eligible(self.p_or_q))
        self.assertFalse(CommutativeLaw.eligible(self.not_p))

    def test_associative_law(self):
        associative_test_expression_AND = Create.conjunction(self.p_and_q, self.r)
        expected_associative_result_1 = Create.conjunction(self.p, self.q_and_r)

        associative_result_1 = AssociativeLaw.apply(associative_test_expression_AND)
        self.assertEqual(associative_result_1, expected_associative_result_1)

        associative_test_expression_OR = Create.disjunction(self.p_or_q, self.r)
        expected_associative_result_2 = Create.disjunction(self.p, self.q_or_r)
        associative_result_2 = AssociativeLaw.apply(associative_test_expression_OR)
        self.assertEqual(associative_result_2, expected_associative_result_2)

        self.assertTrue(AssociativeLaw.eligible(associative_test_expression_AND))
        self.assertTrue(AssociativeLaw.eligible(associative_test_expression_OR))
        self.assertFalse(AssociativeLaw.eligible(self.not_p))
        self.assertFalse(AssociativeLaw.eligible(self.not_p))

    def test_distributive_law(self):
        distributive_test_AND = Create.conjunction(self.p,
                                                   Create.disjunction(self.q, self.r))
        out = Create.disjunction(Create.conjunction(self.p, self.q),
                                 Create.conjunction(self.p, self.r))

        self.assertEqual(DistributiveLaw.apply(distributive_test_AND), out)

        distributive_test_OR = Create.disjunction(self.p,
                                                  Create.conjunction(self.q, self.r))
        out = Create.conjunction(Create.disjunction(self.p, self.q),
                                 Create.disjunction(self.p, self.r))

        self.assertEqual(DistributiveLaw.apply(distributive_test_OR), out)

        self.assertTrue(DistributiveLaw.eligible(distributive_test_AND))
        self.assertTrue(DistributiveLaw.eligible(distributive_test_OR))

    def test_reverse_distributive_law(self):
        or_in = Create.disjunction(Create.conjunction(self.p, self.q),
                                   Create.conjunction(self.p, self.r))

        or_out = Create.conjunction(self.p,
                                    Create.disjunction(self.q, self.r))

        self.assertEqual(ReverseDistributiveLaw.apply(or_in), or_out)

        and_in = Create.conjunction(Create.disjunction(self.p, self.q),
                                    Create.disjunction(self.p, self.r))

        and_out = Create.disjunction(self.p,
                                     Create.conjunction(self.q, self.r))

        self.assertEqual(ReverseDistributiveLaw.apply(and_in), and_out)

        self.assertTrue(ReverseDistributiveLaw.eligible(or_in))
        self.assertTrue(ReverseDistributiveLaw.eligible(and_in))

    def test_identity_law(self):
        identity_test_case_1 = Create.conjunction(self.p, TAUTOLOGY)

        self.assertTrue(IdentityLaw.eligible(identity_test_case_1))

        self.assertEqual(IdentityLaw.apply(identity_test_case_1), self.p)
        self.assertEqual(IdentityLaw.apply(Create.disjunction(self.p, CONTRADICTION)), self.p)

    def test_negation_law(self):
        p_or_not_p = Create.disjunction(self.p, self.not_p)
        negation_law_product_1 = NegationLaw.apply(p_or_not_p)
        self.assertEqual(negation_law_product_1,
                         TAUTOLOGY)

        p_and_not_p = Create.conjunction(self.p, self.not_p)
        negation_law_product_2 = NegationLaw.apply(p_and_not_p)
        self.assertEqual(negation_law_product_2,
                         CONTRADICTION)

        self.assertTrue(NegationLaw.eligible(p_or_not_p))
        self.assertTrue(NegationLaw.eligible(p_and_not_p))

    def test_double_negative_law(self):
        not_not_p = Create.negation(Create.negation(self.p))

        self.assertEqual(DoubleNegativeLaw.apply(not_not_p), self.p)

        self.assertTrue(DoubleNegativeLaw.eligible(not_not_p))


    def test_idempotent_law(self):
        p_and_p = Create.conjunction(self.p, self.p)
        self.assertEqual(IdempotentLaw.apply(p_and_p), self.p)

        p_or_p = Create.disjunction(self.p, self.p)
        self.assertEqual(IdempotentLaw.apply(p_or_p), self.p)

        self.assertTrue(IdempotentLaw.eligible(p_and_p))
        self.assertTrue(IdempotentLaw.eligible(p_or_p))

    def test_universal_bound_law(self):
        p_or_t = Create.disjunction(self.p, TAUTOLOGY)
        self.assertEqual(UniversalBoundLaw.apply(p_or_t), TAUTOLOGY)

        p_and_c = Create.conjunction(self.p, CONTRADICTION)
        self.assertEqual(UniversalBoundLaw.apply(p_and_c), CONTRADICTION)

        self.assertTrue(UniversalBoundLaw.eligible(p_or_t))
        self.assertTrue(UniversalBoundLaw.eligible(p_and_c))

    def test_de_morgans_law(self):
        de_morg_product = DeMorgansLaw.apply(self.not_of_p_and_q)
        expected_de_morg_product = self.not_p_or_not_q
        self.assertEqual(de_morg_product, expected_de_morg_product)
        #self.assertEqual(DeMorgansLaw.apply(self.not_of_p_or_q), self.not_p_and_not_q)

        self.assertTrue(DeMorgansLaw.eligible(self.not_of_p_and_q))
        self.assertTrue(DeMorgansLaw.eligible(self.not_of_p_or_q))

    def test_reverse_de_morgans_law(self):
        reverse_de_morg_prod_1 = ReverseDeMorgansLaw.apply(self.not_p_or_not_q)
        self.assertEqual(reverse_de_morg_prod_1, self.not_of_p_and_q)
        self.assertEqual(ReverseDeMorgansLaw.apply(self.not_p_and_not_q), self.not_of_p_or_q)

        self.assertTrue(ReverseDeMorgansLaw.eligible(self.not_p_or_not_q))
        self.assertTrue(ReverseDeMorgansLaw.eligible(self.not_p_and_not_q))

    def test_absorption_law(self):
        p_disjunct_p_and_q = Create.disjunction(self.p, self.p_and_q)
        self.assertEqual(AbsorptionLaw.apply(p_disjunct_p_and_q), self.p)

        p_conjunct_p_or_q = Create.conjunction(self.p, self.p_or_q)
        self.assertEqual(AbsorptionLaw.apply(p_conjunct_p_or_q), self.p)

        eligibility_1 = AbsorptionLaw.eligible(p_disjunct_p_and_q)
        self.assertTrue(eligibility_1)
        self.assertTrue(AbsorptionLaw.eligible(p_conjunct_p_or_q))

    def test_negation_of_tautology(self):
        not_tautology = Create.negation(TAUTOLOGY)
        self.assertEqual(TautologyNegationLaw.apply(not_tautology), CONTRADICTION)
        self.assertTrue(TautologyNegationLaw.eligible(not_tautology))

    def test_negation_of_contradiction(self):
        not_contradiction = Create.negation(CONTRADICTION)
        self.assertEqual(ContradictionNegationLaw.apply(not_contradiction), TAUTOLOGY)
        self.assertTrue(ContradictionNegationLaw.eligible(not_contradiction))

    def test_find_all_eligible_laws(self):
        pass

    def test_left_term_change_thing(self):
        self.assertEqual(equivalents_in_which_left_statement_changes(not_p), [])

if __name__ == '__main__':
    unittest.main()
