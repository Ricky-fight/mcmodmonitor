from enum import Enum
from pathlib import Path

APPKEY = "$2a$10$NeoaZOd7iGYnan3Clojbg.tVk/oLoJYhE9z3fqC/PdJEm0rj12oJy"
DATABASE = "store.db"
#
# class MaintainVersion(Enum):
#     FORGE_116 = "1.16"
#     FABRIC_116 = "1.16-fabric"
#     FORGE_118 = "1.18"
#     FABRIC_118 = "1.18-fabric"
#     FORGE_119 = "1.19"
#     UNKNOWN = "unknown"
    # FABRIC_119 = "1.19-fabric"


# curseforge api 相关，不需要动
class SupportLoader(Enum):
    FABRIC = "Fabric"
    FORGE = "Forge"


# class SupportVersion(Enum):
#     V1_12 = 628
#     V1_16 = 70886
#     V1_18 = 73250
#     V1_19 = 73407