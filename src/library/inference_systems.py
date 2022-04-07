from abc import ABC
from enum import Enum

# subclass of enums
class MamdaniResolutions(Enum):
    SKYLINE = 1
    CENTER_OF_GRAVITY = 2


class InferenceType(ABC):
    def resolve(self, attribute, memberships):
        return NotImplemented


class Mamdani(InferenceType):
    def __init__(self, resolution_type: MamdaniResolutions = MamdaniResolutions.CENTER_OF_GRAVITY):
        if resolution_type == MamdaniResolutions.SKYLINE:
            self._resolution = self._skyline
        elif resolution_type == MamdaniResolutions.CENTER_OF_GRAVITY:
            self._resolution = self._center_of_gravity
        else:
            raise Exception("Undefined resolution type")

    def resolve(self, attribute, memberships):
        return self._resolution(attribute, memberships)

    def _skyline(self,attribute, memberships):
        return NotImplemented

    def _center_of_gravity(self, attribute, memberships):
        total_membership = []
        for key, value in attribute.sets.items():
            membership = memberships[key] if key in memberships else 0.0
            # calculate Center of gravity for each component, and weight (area)
            total_membership.append(value.cog_and_area(membership))

        return self._weighted_avg(total_membership)[0]


    def _weighted_avg(self, *args):
        total_weight = 0.0
        weighted_sum = 0.0
        for arg in args:
            for pair in arg:
                weighted_sum += pair[0] * pair[1]
                total_weight += pair[1]
        if total_weight == 0:
            return 0.0, 0.0
        else:
            return weighted_sum/total_weight, total_weight