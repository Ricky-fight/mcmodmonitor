import logging
from unittest import TestCase
import curseforge as cf
import main

logger = logging.Logger(__name__)


class Test(TestCase):
    def test_get_files_from_fingerprints(self):
        mods = cf.getPopularMods()
        for mod in mods:
            if not mod.latest_files:
                continue
            fingerprints = []
            for file in mod.latest_files:
                if cf.hasAssets(file):
                    fingerprints.append(main.getFingerprint(file))
            files = main.getFilesFromFingerprints(mod, fingerprints)
            print(mod.name, fingerprints, files)
            self.assertEqual(len(files), len(fingerprints))
