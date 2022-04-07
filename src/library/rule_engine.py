from enum import Enum

from src.library.demorgans_tripple import Triple, Godel
from src.library.inference_systems import Mamdani


class OP(Enum):    # sets are defined as (attribute, set)
    AND = 1     # (OP.AND, A, B)        A/\B
    OR = 2      # (OP.OR, A, B)         A\/B
    NOT = 3     # (OP.NOT, A)           !A
    THEN = 4    # (OP.THEN, z, A)       A = z (membership in the set)


class Shape(Enum):
    LEFT = 1
    TRAP = 2
    RIGHT = 3


class FuzzySet:
    def __init__(self, x_values, y_values, source, name = "", shape : Shape = Shape.TRAP):
        assert len(x_values) == len(y_values), "X and Y values must match"
        assert source is not None, "Source must be defined"
        assert name != "", "Fuzzy set must have a name"

        self.x = x_values
        self.y = y_values
        self.source = source
        self.name = name

        if shape == Shape.LEFT:
            self.cog_and_area = self.left_cog_and_area
        elif shape == Shape.TRAP:
            self.cog_and_area = self.trap_cog_and_area
        elif shape == Shape.RIGHT:
            self.cog_and_area = self.right_cog_and_area
        else:
            raise Exception("Unidentified shape supplied to fuzzy set.")

    def left_cog_and_area(self, height):
        rect_area = (self.x[1] - self.x[0])*height
        rect_cog = (self.x[0] + self.x[1])/2
        tri_area = (self.x[2] - self.x[1])*height/2
        tri_cog = self.x[1] + (self.x[2] - self.x[1])/3

        weighted_cog = rect_area*rect_cog + tri_area*tri_cog
        total_area = tri_area+rect_area

        if total_area == 0:
            return 0.0, 0.0

        return weighted_cog/total_area, total_area

    def trap_cog_and_area(self, height):
        l_tri_area = (self.x[1] - self.x[0]) * height/2
        l_tri_cog = self.x[0] + (self.x[1]-self.x[0]) * 2/3     # is this wrong? it was in Prof. Dawes work.
        rect_area = (self.x[2] - self.x[1]) * height
        rect_cog = (self.x[2] - self.x[1])/2
        r_tri_area = (self.x[3] - self.x[2]) * height/2
        r_tri_cog = self.x[2] + (self.x[3] - self.x[2])/3

        weighted_cog = l_tri_cog*l_tri_area+rect_cog*rect_area+r_tri_cog*r_tri_area
        total_area = l_tri_area+rect_area+r_tri_area

        if total_area == 0:
            return 0.0, 0.0

        return weighted_cog/total_area, total_area

    def right_cog_and_area(self, height):
        rect_area = (self.x[2] - self.x[1])*height
        rect_cog = (self.x[1] + self.x[2]) / 2
        tri_area = (self.x[1] - self.x[0]) * height/2
        tri_cog = self.x[0] + (self.x[1] - self.x[0])*2/3

        weighted_cog = rect_cog*rect_area+tri_cog*tri_area
        total_area = rect_area+tri_area

        if total_area == 0:
            return 0.0, 0.0

        return weighted_cog/total_area, total_area

    def membership(self, x=None):
        if x is None:
            x = self.source.get()
        upper_bound = -1
        lower_bound = -1
        for i, val in enumerate(self.x):
            if val <= x:
                lower_bound = i
            if val >= x:
                upper_bound = i
                break
        if lower_bound == -1 or upper_bound == -1:
            return 0.0
        if lower_bound == upper_bound:
            return float(self.y[upper_bound])

        # within
        slope = (self.y[upper_bound] - self.y[lower_bound])/(self.x[upper_bound] - self.x[lower_bound])
        return self.y[lower_bound] + slope*(x-self.x[lower_bound])


class FuzzyAttribute:
    def __init__(self, name: str = ""):
        self.name = name
        self.sets = {}

    def append(self, fuz: FuzzySet):
        assert fuz.name not in self.sets.keys(), "FuzzyAttributes must be comprised of uniquely named fuzzy sets"
        self.sets[fuz.name] = fuz

    def get_membership(self, value):
        return {fuz.name: fuz.membership(value) for fuz in self.sets.values()}


class Rule:
    def __init__(self, antecedents : [FuzzySet], consequents : [FuzzySet], name = ""):
        """
        A rule can be roughly thought of as some operation that maps fuzzy antecedents to fuzzy consequents.
        :param antecedents: a list of fuzzy antecedents
        :param consequents: a list of fuzzy consequents
        :param name: name of the rule
        """
        self.antecedents = antecedents
        self.consequents = consequents
        self.name = name

    @property
    def all_sets(self):
        """
        a list of all sets in the rule
        :return:
        """
        return self.antecedents.copy() + self.consequents.copy()


class RuleSet:
    def __init__(self, rules : [Rule]):
        self._rules = []
        for rule in rules:
            self.append(rule)

    def append(self, rule : Rule):
        """
        Takes a Rule object and appends it to our set of rules
        :param rule: a Rule object.
        """
        if type(rule) is Rule:
            self._rules.append(rule)
        else:
            raise Exception("Supplied rule is not of type: Rule")

# rule definitions
# ----------------
_BROAD_SPREAD = {
    "very low":     ([-0.3, -0.1, 0.1, 0.3], [0, 1, 1, 0]),
    "low":          ([-0.5, -0.3, 0.3, 0.5], [0, 1, 1, 0]),
    "medium":       ([0.2, 0.4, 0.6, 0.8], [0, 1, 1, 0]),
    "high":         ([0.5, 0.7, 1.3, 1.5], [0, 1, 1, 0]),
    "very high":    ([0.7, 0.9, 1.1, 1.3], [0, 1, 1, 0])
}

_BINARY_SPREAD = {
    "no":           ([-1, -0.1, 0.1, 1], [0, 1, 1, 0]),
    "yes":          ([0, 0.9, 1.14, 2], [0, 1, 1, 0])
}

_TRINARY_SPREAD = {
    "low":          ([-0.66, -0.33, 0.33, 0.66], [0, 1, 1, 0]),
    "medium":       ([0.1, 0.33, 0.66, 0.9], [0, 1, 1, 0]),
    "high":         ([0.33, 0.66, 1.34, 1.67], [0, 1, 1, 0])
}

# utility function
def generate_generic_attribute(member_sets=_BROAD_SPREAD, name=""):
    assert name != "", "attribute must have a name"
    attribute = FuzzyAttribute(name)
    for key in member_sets.keys():
        # determine shape
        if len(member_sets[key][1]) == 4:
            shape = Shape.TRAP
        elif len(member_sets[key][1]) == 3 and member_sets[key][1][0] == 0:
            shape = Shape.RIGHT
        elif len(member_sets[key][1]) == 3 and member_sets[key][1][2] == 0:
            shape = Shape.LEFT
        else:
            raise Exception("Invalid shape definition")
        attribute.append(FuzzySet(member_sets[key][0], member_sets[key][1], source=0, name=key, shape=shape))

    return attribute

# overall quality set
OVERALL_QUALITY = generate_generic_attribute(name="Quality", member_sets=_TRINARY_SPREAD)

raw_attributes = {"email_speed":                _BROAD_SPREAD,
                  "public_speaking":            _BROAD_SPREAD,
                  "native_speaker":             _BROAD_SPREAD,
                  "explanation_quality":        _BROAD_SPREAD,
                  "one_on_one":                 _BROAD_SPREAD,
                  "availability":               _BROAD_SPREAD,
                  "class_management":           _BROAD_SPREAD,
                  "empathy":                    _BROAD_SPREAD,
                  "workload":                   _BROAD_SPREAD,
                  "preparation":               _BROAD_SPREAD,
                  "assignment_value":           _BROAD_SPREAD,
                  "assignment_quality":         _BROAD_SPREAD,
                  "webplatform_quality":        _BROAD_SPREAD,
                  "real_world_applicability":   _BROAD_SPREAD,
                  "available_resources":        _BROAD_SPREAD,
                  "knowledge":                  _BROAD_SPREAD,
                  "career_length":              _BROAD_SPREAD,
                  "tenure":                     _BINARY_SPREAD,
                  "rate_my_prof_score":         _BROAD_SPREAD,
                  "publication":                _BROAD_SPREAD,
                  "repeat_instruction":         _BROAD_SPREAD}


derived_attributes = {"tyrant":                 (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, ("empathy", "very low"), ("workload", "very high"), ("assignment_value", "low"))),
                          (OP.THEN, "medium", (OP.AND, ("empathy", "low"), ("workload", "high"), ('assignment_value', "low"))),
                          (OP.THEN, "low", (OP.OR,
                                            (OP.AND, (OP.OR, ("empathy", "medium"), ("empathy", "high")), (OP.OR, ("workload", "low"), ("workload", "medium"))),
                                            (OP.NOT, ("empathy", "low"))))
                      ]),

                      "over_the_hill":          (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, (OP.OR, ("career_length", "very high"), ("career_length", "high")), (OP.OR, ("real_world_applicability", "low"), ("real_world_applicability", "very low")))),
                          (OP.THEN, "medium", (OP.AND, (OP.OR, ("career_length", "high"), ("career_length", "medium")), ("real_world_applicability", "medium"))),
                          (OP.THEN, "low", (OP.OR, (OP.NOT, (OP.OR, ("career_length", "high"), ("career_length", "very high"))), ("real_world_applicability", "high")))
                      ]),

                      "incompetent":            (_BINARY_SPREAD, [
                          (OP.THEN, "yes", (OP.OR,
                                             (OP.AND, ("explanation_quality", "low"), ("workload", "very low"), ("knowledge", "very low")),
                                             (OP.AND, ("knowledge", "very low"), ("repeat_instruction", "low")),
                                             (OP.AND, ("workload", "very low"), ("preparation", "low")))),
                          (OP.THEN, "no", (OP.OR,
                                             (OP.OR, ("workload", "medium"), ("preparation", "medium"), ("real_world_applicability", "medium")),
                                             (OP.AND, ("workload", "medium"), ("preparation", "medium")),
                                             (OP.AND, ("explanation_quality", "medium"), ("empathy", "medium")),
                                             (OP.AND, ("knowledge", "medium"), ("repeat_instruction", "medium")),
                                             (OP.AND, ("workload", "medium"), ("preparation", "medium")),
                                             (OP.NOT, ("knowledge", "low"))))
                      ]),

                      "researcher":             (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, ("publication", "high"), ("knowledge", "high"))),
                          (OP.THEN, "medium", (OP.AND, ("publication", "medium"), ("knowledge", "medium"))),
                          (OP.THEN, "low", (OP.AND, ("publication", "low"), (OP.OR, ("knowledge", "medium"), ("knowledge", "low"))))
                      ]),

                      "shy":                    (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, ("public_speaking", "low"), ("one_on_one", "high"))),
                          (OP.THEN, "medium", (OP.AND, ("public_speaking", "medium"), ("one_on_one", "medium"))),
                          (OP.THEN, "low", (OP.NOT, ("public_speaking", "low")))
                      ]),

                      "neurotic":               (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, ("email_speed", "very high"), ("webplatform_quality", "high"), ("preparation", "very high"))),
                          (OP.THEN, "medium", (OP.AND, (OP.OR, ("email_speed", "high"), ("email_speed", "medium")), (OP.OR, ("webplatform_quality", "high"), ("webplatform_quality", "medium")))),
                          (OP.THEN, "low", (OP.AND, ("email_speed", "low"), (OP.OR, ("webplatform_quality", "low"))))
                      ]),

                      "organizer":              (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, ("webplatform_quality", "high"), ("workload", "high"), ("preparation", "high"))),
                          (OP.THEN, "medium", (OP.AND, ("webplatform_quality", "medium"), ("workload", "medium"), ("preparation", "medium"))),
                          (OP.THEN, "low", (OP.AND, ("webplatform_quality", "low"), ("workload", "low"), ("preparation", "low")))
                      ]),


                      "communicator":           (_BINARY_SPREAD, [
                          (OP.THEN, "yes", (OP.AND, ("empathy", "high"), ("explanation_quality", "high"), ("native_speaker", "high"))),
                          (OP.THEN, "no", (OP.OR,
                                            (OP.AND, ("empathy", "low"), ("explanation_quality", "high")),
                                            (OP.AND, ("native_speaker", "low"), ("availability", "low"), ("public_speaking", "low"), ("one_on_one", "low"))))
                      ]),

                      "experienced":              (_TRINARY_SPREAD, [
                          (OP.THEN, "high", (OP.AND, ("knowledge", "high"), ("repeat_instruction", "high"), ("rate_my_prof_score", "high"))),
                          (OP.THEN, "medium", (OP.AND, ("career_length", "medium"), ("repeat_instruction", "medium"), (OP.OR, ("rate_my_prof_score", "high"), ("rate_my_prof_score", "medium")))),
                          (OP.THEN, "low", (OP.OR, ("career_length", "low"), ("tenure", "no"), ("repeat_instruction", "low")))
                      ])}

final_attribute = {"quality":                 (_BROAD_SPREAD, [
                                                    # if (EMPATHY is VERY LOW) and (WORKLOAD is VERY HIGH) and (ASSESSMENT_VALUES is VERY LOW) then TYRANT is HIGH
                                                    (OP.THEN, "very high", (OP.AND, ("expertise", "high"), (OP.AND, ("communicator", "high"), (OP.AND, ("organizer", "high"), (OP.AND, (OP.OR, ("neurotic", "low"), ("neurotic", "medium")), (OP.AND, (""), ()))))))
                      ])}


def resolve(rules, sets, triple: Triple = Godel):
    unary_ops = [OP.THEN, OP.NOT]
    binary_ops = [OP.AND, OP.OR]
    if rules[0] in unary_ops:
        if rules[0] == OP.THEN:             # OP.THEN, Affected Set, (fuzzy fluents)
            return resolve(rules[2], sets, triple)
        elif rules[0] == OP.NOT:
            return triple.neg(resolve(rules[1], sets, triple))

    elif rules[0] in binary_ops:
        resolutions = [resolve(rule, sets, triple) for rule in rules[1:]]
        value = resolutions[0]
        for r in resolutions[1:]:
            if rules[0] == OP.AND:
                value = triple.t(value, r)
            elif rules[0] == OP.OR:
                value = triple.s(value, r)
        return value

    else:
        return sets[rules[0]][rules[1]]

"""
def resolve(rule, sets, triple: Triple = Godel):
    if rule[0] == OP.THEN:
        return resolve(rule[2], sets, triple)
    elif rule[0] == OP.AND:
        return triple.t(resolve(rule[1], sets, triple), resolve(rule[2], sets, triple))
    elif rule[0] == OP.OR:
        return triple.s(resolve(rule[1], sets, triple), resolve(rule[2], sets, triple))
    elif rule[0] == OP.NOT:
        return triple.neg(resolve(rule[1], sets, triple))
    else:
        return sets[rule[0]][rule[1]]
"""


# Production Rules
def evaluate(variable_dict, triple: Triple = Godel):
    base_valuation = {}
    # get valuations in all base sets.
    for key, value in variable_dict.items():
        base_valuation[key] = generate_generic_attribute(name=key, member_sets=raw_attributes[key]).get_membership(value)

    derived_attribute = {}
    derived_valuation = {}
    for key, value in derived_attributes.items():
        derived_attribute[key] = generate_generic_attribute(name=key, member_sets=value[0])
        derived_valuation[key] = {}
        for rule in value[1]:
            derived_valuation[key][rule[1]] = resolve(rule, base_valuation)





    # defuzzify and get cogs of the above
    #m = Mamdani()
    #defuzzed_derived_memberships = {}
    #refuzzed_memberships = {}
    #for key in derived_attribute.keys():
    #    defuzzed_derived_memberships[key] = m.resolve(derived_attribute[key], derived_valuation[key])
    #    refuzzed_memberships[key] = derived_attribute[key].get_membership(defuzzed_derived_memberships[key])

    # recombine the memberships and generate the final output
    return derived_valuation


    # merge them together

    # if (EXPERT is HIGH) and (ORGANIZER is HIGH) and (COMMUNICATOR is HIGH) and (RESEARCHER is LOW or MEDIUM) and (SHY is NOT HIGH) and (NEUROTIC is MEDIUM) and (TYRANT is LOW) then OVERALL_QUALITY is (HIGH)
    # if ((INCOMPOTENT is HIGH) or (OVER_THE_HILL is HIGH)) AND (NEUROTIC is HIGH) then OVERALL_Quality is (LOW)


evaluate({
    "email_speed": 1.0,
    "public_speaking": 1.0,
    "native_speaker": 1.0,
    "explanation_quality": 1.0,
    "one_on_one": 1.0,
    "availability": 1.0,
    "class_management": 1.0,
    "empathy": 1.0,
    "workload": 1.0,
    "preparation": 1.0,
    "assignment_value": 1.0,
    "assignment_quality": 1.0,
    "webplatform_quality": 1.0,
    "real_world_applicability": 1.0,
    "available_resources": 1.0,
    "knowledge": 1.0,
    "career_length": 1.0,
    "tenure": 1.0,
    "rate_my_prof_score": 1.0,
    "publication": 1.0,
    "repeat_instruction": 1.0
})