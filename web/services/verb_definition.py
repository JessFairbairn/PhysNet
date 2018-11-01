import typing

# from ConDep import condep

# from ConDep import condep.parsing.cd_definitions.CDDefinition

from condep.parsing.cd_definitions import CDDefinition

class VerbDefinition:
    score = None
    example = None
    instances = None # Type: List[str]
    condep = None #Type: CDDefinition