import src.library.demorgans_tripple as de
import src.library.inference_systems as inf
from src.library.rule_engine import FuzzyAttribute, Shape, FuzzySet, evaluate

# ===============
# Constant values
# ===============


# weightings
# ----------

# section weightings
COMMUNICATION_WEIGHTING = 0.4
COURSE_CONTENT_WEIGHTINGS = 0.4
EXPERIENCE_WEIGHTINGS = 0.2

# The following values might not be used, but they are important to know
# because we may use them in our reasoning

# communication weightings (truncated and rounded)
EMAIL_SPEED_WEIGHTING = 0.06
PUBLIC_SPEAKING_WEIGHTING = 0.09
NATIVE_SPEAKER_WEIGHTING = 0.12
EXPLANATION_QUALITY_WEIGHTING = 0.35
ONE_ON_ONE_WEIGHTING = 0.08
EXTRACURRICULAR_WEIGHTING = 0.11
CLASS_MANAGEMENT_WEIGHTING = 0.05
EMPATHY_WEIGHTING = 0.14

# course content weightings
WORKLOAD_WEIGHTING = 0.22
PREP_WEIGHTING = 0.16
ASSIGNMENT_VALUE_WEIGHTING = 0.12
ASSESSMENT_QUALITY_WEIGHTING = 0.13
WEB_PLATFORM_DESIGN_WEIGHTING = 0.07
REAL_WORLD_APPLICABILITY_WEIGHTING = 0.16
AVAILABLE_RESOURCES_WEIGHTING = 0.14

# professor experience weightings
KNOWLEDGE_WEIGHTING = 0.39
TEN_YEAR_PLUS_WEIGHTING = 0.09
TENURED_WEIGHTING = 0.05
RATE_MY_PROF_SCORE_WEIGHTING = 0.12
PUBLICATION_WEIGHTING = 0.10
REPEAT_INSTRUCTION_WEIGHTING = 0.25


# rule definitions
# ----------------
_BROAD_SPREAD = {
    "very low" : ([0, 0.1, 0.2], [1, 1, 0]),
    "low" : ([0, 0.25, 0.5], [1, 1, 0]),
    "medium" : ([0.3, 0.4, 0.6, 0.7], [0, 1, 1, 0]),
    "high" : ([0.5, 0.75, 1], [0, 1, 1]),
    "very high": ([0.8, 0.9, 1], [0, 1, 1])
}

_BINARY_SPREAD = {
    "no": ([0, 0.4, 0.6], [1, 1, 0]),
    "yes": ([0.4, 0.6, 1], [0, 1, 1])
}

_TRINARY_SPREAD = {
    "low" : ([0, 0.33, 0.5], [1, 1, 0]),
    "medium" : ([0.25, 0.33, 0.66, 0.75], [0, 1, 1, 0]),
    "high" : ([0.66, 0.75, 1], [0, 1, 1])
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


# communication attributes
EMAIL_SPEED = generate_generic_attribute(name="email reply speed")                      #
PUBLIC_SPEAKING = generate_generic_attribute(name="public speaking skill")              #
NATIVE_SPEAKER = generate_generic_attribute(name="working-language fluency")            #
EXPLANATION_QUALITY = generate_generic_attribute(name="quality of explanation")         #
ONE_ON_ONE = generate_generic_attribute(name="one on one skills")
EXTRACURRICULAR = generate_generic_attribute(name="availability outside of class")
CLASS_MANAGEMENT = generate_generic_attribute(name="ability to manage classroom")       #
EMPATHY = generate_generic_attribute(name="empathy")                                    #

# course contents
WORKLOAD = generate_generic_attribute(name="course workload")                           #
PREP = generate_generic_attribute(name="lecture preparedness")                          #
ASSIGNMENT_VALUE = generate_generic_attribute(name="fair assessment weightings")        #
ASSIGNMENT_QUALITY = generate_generic_attribute(name="assessment quality")              #
WEB_PLATFORM_DESIGN = generate_generic_attribute(name="quality of course web-platform") #
REAL_WORLD_APPLICABILITY = generate_generic_attribute(name="real world applicability")  #
AVAILABLE_RESOURCES = generate_generic_attribute(name="quality of available resources") #

# professor experience
KNOWLEDGE = generate_generic_attribute(name="subject mater expertize")                  #
TEN_YEAR_PLUS = generate_generic_attribute(name="long career")                          #
TENURED = generate_generic_attribute(member_sets=_BINARY_SPREAD, name="tenured")        # special case, requires a different ruleset
RATE_MY_PROF_SCORE = generate_generic_attribute(name="ratemyprofessor")                 #
PUBLICATION = generate_generic_attribute(name="number of publications")                 #
REPEAT_INSTRUCTION = generate_generic_attribute(name="course repeats")                  #


# resulting sets
TYRANT = generate_generic_attribute(name="Tyrant", member_sets=_TRINARY_SPREAD) # read: cares not for you or your time
OVER_THE_HILL = generate_generic_attribute(name="Close to retirement", member_sets=_TRINARY_SPREAD) # been doing this for long enough that they likely do not care.
INCOMPETENT = generate_generic_attribute(name="Not very good at their job, at all", member_sets=_TRINARY_SPREAD)

RESEARCHERS = generate_generic_attribute(name="Research Oriented Academic", member_sets=_TRINARY_SPREAD) #read: antisocial/not great pedigogy
SHY = generate_generic_attribute(name="Bad with crowds", member_sets=_TRINARY_SPREAD)
NEUROTIC = generate_generic_attribute(name= "Neurotic", member_sets=_TRINARY_SPREAD)

ORGANIZER = generate_generic_attribute(name="Organizer", member_sets=_TRINARY_SPREAD)   # read: absolute task master.
COMMUNICATOR = generate_generic_attribute(name="Great Communicators", member_sets=_TRINARY_SPREAD)  #
EXPERT = generate_generic_attribute(name="Expert", member_sets=_TRINARY_SPREAD)

# overall quality set
OVERALL_QUALITY = generate_generic_attribute(name="Quality", member_sets=_TRINARY_SPREAD)

evaluate(None)