import re
from operator import attrgetter

import requests as requests
from requests import JSONDecodeError

from config import APPKEY, SupportLoader
from datamodels import Mod, mod_from_dict, File, file_from_dict, LatestFile
from logging import Logger

logger = Logger(__name__)


def get(path, *, params=None) -> requests.Response:
    headers = {
        'Accept':    'application/json',
        'x-api-key': APPKEY
    }
    base_url = 'https://api.curseforge.com'
    return requests.get(base_url + path, headers=headers, params=params)


def post(path, *, body, params=None) -> requests.Response:
    headers = {
        'Accept':    'application/json',
        'x-api-key': APPKEY
    }
    base_url = 'https://api.curseforge.com'
    return requests.post(base_url + path, headers=headers, json=body, params=params)


def getData(r: requests.Response):
    """
    get response json data
    :param r: response fron requests.request()
    :return: dict object from json
    """
    if r.status_code == 200:
        try:
            return r.json()['data']
        except JSONDecodeError as e:
            logger.error(f"获取['data']失败：{e}")
            return None


def getLastUpdatedMods(index=0, pagesize=50) -> [Mod]:
    logger.info("正在获取模组更新列表……")
    params = {
        "gameId": 432,
        "sortOrder": "desc",
        "classId": 6,
        "sortField": 3,
        "index": index,
        "pageSize": pagesize
    }
    r = get(f"/v1/mods/search", params=params)
    mods = [mod_from_dict(moddata) for moddata in getData(r)]
    if mods:
        logger.info(f"获取到{len(mods)}个最新模组")
    else:
        logger.error("获取模组数据失败，请确认网络情况是否良好")
    return mods


def getPopularMods(index=0, pagesize=50) -> [Mod]:
    logger.info("正在获取热门模组列表……")
    params = {
        "gameId": 432,
        "sortOrder": "desc",
        "classId": 6,
        "sortField": 2,
        "index": index,
        "pageSize": pagesize
    }
    r = get(f"/v1/mods/search", params=params)
    mods = [mod_from_dict(moddata) for moddata in getData(r)]
    if mods:
        logger.info(f"获取到{len(mods)}个最新模组")
    else:
        logger.error("获取模组数据失败，请确认网络情况是否良好")
    return mods


def hasAssets(latestfile:LatestFile) -> bool:
    if latestfile.modules:
        for module in latestfile.modules:
            if module.name == "assets":
                return True
    return False


def getModLatestFile(mod: Mod) -> LatestFile | None:
    """
    获取模组最新文件
    :return: File
    """
    files = sorted(mod.latest_files, key=attrgetter('file_date'))
    if files:
        return files.pop()
    else:
        return None


def getLatestAssetFingerprint(file: LatestFile) -> int | None:
    """
    尝试获取文件asset的fingerprint
    :return: fingerprint
    """
    for module in file.modules:
        if module.name == "assets":
            return module.fingerprint
    return None


def getTags(file: LatestFile):
    gvs = file.game_versions
    tags = []
    for loader in SupportLoader:
        if loader in gvs:
            tags.append(gvs)


# def getModFiles(modid: int, version: SupportVersion = None) -> [File]:
#     logger.info("正在获取模组文件列表……")
#     r = get(f"/v1/mods/{modid}/files", params={"gameVersionTypeId": version})
#     filesdata = getData(r)
#     files = []
#     for filedata in filesdata:
#         files.append(file_from_dict(filedata))
#     return files

