import logging
import os
import pathlib
import shutil
import sys
import time
from json import JSONDecodeError

import dateutil.utils
import requests

from cache import FingerPrintCache
from config import SupportLoader, APPKEY
from datamodels import File, Mod, LatestFile
import curseforge as cf
from report import Report, Block, buildLink

logger = logging.Logger(__name__, level=logging.DEBUG)
# REPORT_NAME = f"report-{dateutil.utils.today().date()}.md"
REPORT_NAME = "report.md"


def run():
    """
    main func
    :return:
    """
    start = time.time()
    cache = FingerPrintCache()
    logger.debug(f"加载缓存用时 {time.time() - start:.2f} 秒")
    # print("Hello!")
    if not cache.data:
        # 第一次运行，爬取前10000排名模组assets的fingerprint
        print("第一次运行，爬取前 10000 排名模组 assets 的 fingerprint")
        init(cache)
        cache.save()
    latests = []
    pagesize = 50
    logger.warning(f"开始获取最近更新模组……")
    for index in range(0, 4 * pagesize, pagesize):
        logger.warning(f"正在获取第{index + 1}-{index + pagesize + 1}个模组")
        latests.extend(cf.getLastUpdatedMods(index, pagesize))
    newMods = {}
    updatedMods = {}
    for mod in latests:
        if mod.game_popularity_rank < 10000:
            if mod.slug not in cache.data:
                fingerprints = getFingerprints(mod)
                if fingerprints:
                    newMods[mod] = getFilesFromFingerprints(mod, fingerprints)
                    cache.data[mod.slug] = cache.data
            else:
                fingerprints = getFingerprints(mod)
                if fingerprints:
                    diff = fingerprints - cache.data[mod.slug]
                    if diff:
                        updatedMods[mod] = getFilesFromFingerprints(mod, diff)
                        cache.data[mod.slug] |= fingerprints
    report = Report()
    report.addTitle("🔝新热门模组")
    for mod in newMods:
        block = Block()
        for file in newMods[mod]:
            block.addUl(buildLink(file.file_name, file.download_url.replace(" ", "%20")))
        report.addFoldBlock(mod.name, block)
    report.addLine()
    report.addTitle("✨更新模组")
    for mod in updatedMods:
        block = Block()
        for file in updatedMods[mod]:
            block.addUl(buildLink(file.file_name, file.download_url.replace(" ", "%20")))
        report.addFoldBlock(mod.name, block)
    text = report.dumps()
    with open(REPORT_NAME, "w", encoding='utf8') as f:
        f.write(text)
        print(text)
    cache.save()
    # Set report name
    if 'GITHUB_OUTPUT' in os.environ.keys():
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f'report_name={REPORT_NAME}', file=fh)


def init(cache):
    pagesize = 50
    mods = []
    for index in range(0, 10000 - pagesize, pagesize):
        for leftTries in reversed(range(0, 3)):
            logger.warning(f"正在获取第 {index + 1}-{index + pagesize + 1} 个模组")
            try:
                mods.extend(cf.getPopularMods(index, pagesize))
                break
            except requests.exceptions.ProxyError:
                logger.warning(f"获取第 {index + 1}-{index + pagesize + 1} 个模组失败, 剩余尝试次数 {leftTries}")
                pass
    for mod in mods:
        if not mod.latest_files:
            logger.warning(f"模组 {mod.name} 未返回最新文件")
            continue
        cache.data[mod.slug] = getFingerprints(mod)


def getFingerprints(mod) -> set:
    """
    返回 Mod 实例的 所有带有 Asset 目录的 fingerprint
    :param mod:
    :return:
    """
    fingerprints = set()
    if not mod.latest_files:
        return fingerprints
    for latestFile in mod.latest_files:
        fingerprint = getFingerprint(latestFile)
        if fingerprint:
            fingerprints.add(fingerprint)
    return fingerprints


def getFingerprint(file: LatestFile) -> int | None:
    """
    返回 File 实例的 Asset 目录的 fingerprint（若存在）
    :param file:
    :return:
    """
    if not file:
        return None
    if not file.modules:
        return None
    for modlule in file.modules:
        if modlule.name == "assets":
            return modlule.fingerprint
    return None


def getFilesFromFingerprints(mod: Mod, fingerprints: set) -> [File]:
    files = []
    if not mod.latest_files:
        return files
    for file in mod.latest_files:
        if not cf.hasAssets(file):
            continue
        fp = getFingerprint(file)
        if fp and (fp in fingerprints):
            files.append(file)
    return files


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    run()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助