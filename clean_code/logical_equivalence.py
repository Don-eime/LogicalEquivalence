from logical_statements import *


# UTIL
def is_junction(statement):
    if statement.connective is ValueFunctions.conjunction or \
            statement.connective is ValueFunctions.disjunction:
        return True
    else:
        return False


def junction_opposite(statement):
    if statement.connective is ValueFunctions.conjunction:
        return ValueFunctions.disjunction
    elif statement.connective is ValueFunctions.disjunction:
        return ValueFunctions.conjunction
    return None


def is_statement(statement):
    return True if statement.__class__ == Statement else False


def are_opposite_junctions(statement_1, statement_2):
    if not is_junction(statement_1) or not is_junction(statement_2):
        return False

    junction_2s_opposite = junction_opposite(statement_2)
    if statement_1.connective is junction_2s_opposite:
        return True
    return False


def is_tautology_or_contradiction(statement):
    if statement.connective is ValueFunctions.tautology or\
            statement.connective is ValueFunctions.contradiction:
        return True
    return False


def is_negation(statement):
    if statement.connective is ValueFunctions.negation:
        return True
    return False


def is_double_negative(statement):
    if is_negation(statement) and is_negation(statement.left_term):
        return True
    return False


class LawOfEquivalence(ABC):

    @staticmethod
    @abstractmethod
    def eligible(statement: Statement):
        pass

    @staticmethod
    @abstractmethod
    def apply(statement: Statement):
        pass


class CommutativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return Statement(statement.connective, statement.right_term, statement.left_term)


class AssociativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            if statement.left_term.connective == statement.connective:
                return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        """ Given (p AND q) AND r. Returns Returns p AND (q AND r) """
        new_left = statement.left_term.left_term  # p

        new_right = Statement(statement.connective,
                              statement.left_term.right_term,  # q
                              statement.right_term)  # r

        return Statement(statement.connective, new_left, new_right)


class ReverseAssociativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            if statement.right_term.__class__ == Statement:
                if statement.right_term.connective == statement.connective:
                    return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        """ Given p AND (q AND r). Returns (p AND q) AND r."""
        new_left = Statement(statement.connective,
                             statement.left_term,  # p
                             statement.right_term.left_term)  # q

        new_right = statement.right_term.right_term  # r

        return Statement(statement.connective, new_left, new_right)


class DistributiveLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        """ Returns the eligibility of statement for application of the Distributive Law. p ∧ (q ∨ r) """
        if is_junction(statement):
            # the statement is a junction
            if Util.is_atom(statement.left_term) and statement.right_term.__class__ == Statement:
                # the left statement is an atom and the right statement is another statement
                if statement.right_term.connective == junction_opposite(statement):
                    # the connective of the second statement is the opposite junction of the parameter statement
                    return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        new_left_side = Statement(statement.connective, statement.left_term,
                                  statement.right_term.left_term)
        new_right_side = Statement(statement.connective, statement.left_term,
                                   statement.right_term.right_term)

        return Statement(statement.right_term.connective, new_left_side, new_right_side)


class IdentityLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and statement.right_term in [TAUTOLOGY, CONTRADICTION]:
            # the statement is a junction and the second statement is either tautology or contradiction
            return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term


class ReverseDistributiveLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        """
            Eligible if:
                connective and both statements are junctions AND
                both statement connectives are the opposite junction to the central one
        :param statement:
        :return:
        """
        if is_junction(statement) and is_junction(statement.right_term) and is_junction(statement.left_term):
            if are_opposite_junctions(statement, statement.right_term):
                return True
        return False

    @staticmethod
    def apply(statement: Statement):
        new_left = statement.left_term.left_term
        new_right = Statement(statement.connective, statement.left_term.right_term,
                              statement.right_term.right_term)

        return Statement(statement.left_term.connective, new_left, new_right)


class NegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and statement.left_term == statement.right_term.left_term:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        if statement.connective == ValueFunctions.disjunction:
            return TAUTOLOGY
        elif statement.connective == ValueFunctions.conjunction:
            return CONTRADICTION


class DoubleNegativeLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and is_negation(statement.left_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term.left_term


class ReverseDoubleNegativeLaw(LawOfEquivalence):
    """ Gives ~(~(p)) from p. Likely unneeded."""

    @staticmethod
    def eligible(statement: Statement):
        if not is_negation(statement):
            # everything except negations are eligible
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return Statement(negation, Statement(negation, statement))


class IdempotentLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and statement.left_term == statement.right_term:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term


class UniversalBoundLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and is_tautology_or_contradiction(statement.right_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        if statement.connective == ValueFunctions.disjunction:
            return TAUTOLOGY
        elif statement.connective == ValueFunctions.conjunction:
            return CONTRADICTION


class DeMorgansLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and is_junction(statement.left_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        negated_statement = statement.left_term
        new_left_side = Create.negation(negated_statement.left_term)
        new_right_side = Create.negation(negated_statement.right_term)

        new_connective = junction_opposite(negated_statement)

        de_morgans_product = Statement(new_connective, new_left_side, new_right_side)
        return de_morgans_product


class ReverseDeMorgansLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and is_negation(statement.left_term) and is_negation(statement.right_term):
            return True

        return False

    @staticmethod
    def apply(statement: Statement):
        new_connective = junction_opposite(statement)

        new_junction = Statement(new_connective, statement.left_term.left_term,
                                 statement.right_term.left_term)

        return Create.negation(new_junction)


class AbsorptionLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            # must be junction
            if are_opposite_junctions(statement, statement.right_term):
                # right statement must also be a junction, and junction opposite to statement
                if statement.right_term.left_term != statement.right_term.right_term:
                    # the right junction cannot be between the same to Atoms (so that this law doesn't apply 2 laws)
                    if statement.right_term.left_term == statement.left_term:
                        # the left statement of right statement must be the same as
                        # the left statement of parent statement
                        return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term


class ContradictionNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and statement.left_term == CONTRADICTION:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return TAUTOLOGY


class TautologyNegationLaw(LawOfEquivalence):
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and statement.left_term == TAUTOLOGY:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return CONTRADICTION


ALL_EQUIVALENCE_LAWS = LawOfEquivalence.__subclasses__()
