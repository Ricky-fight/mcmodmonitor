import logging
import os
import sys
from enum import Enum
from pathlib import Path

if 'CURSEFORGE_APPKEY' in os.environ.keys():
    APPKEY = os.environ['CURSEFORGE_APPKEY']
else:
    logging.getLogger(__name__).fatal("CURSEFORGE_APPKEY不存在！")
    exit(1)

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