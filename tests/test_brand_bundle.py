#!/usr/bin/env python3
# Copyright © 2026 Mindclade, LLC. All Rights Reserved.
# Mindclade Proprietary and Confidential.
# SPDX-License-Identifier: LicenseRef-Mindclade-Proprietary

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "brand_bundle", ROOT / "scripts" / "brand_bundle.py"
)
assert SPEC and SPEC.loader
brand_bundle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(brand_bundle)


class BrandBundleTest(unittest.TestCase):
    def test_checked_in_manifest_is_exact(self) -> None:
        manifest = brand_bundle.load_manifest()
        self.assertEqual(brand_bundle.verify_manifest(manifest), [])
        self.assertEqual(
            manifest["authority"],
            "checked-in-distribution-not-brand-governance-authority",
        )

    def test_archive_is_reproducible(self) -> None:
        manifest = brand_bundle.load_manifest()
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.tar.gz"
            second = Path(temporary) / "second.tar.gz"
            self.assertEqual(
                brand_bundle.build_archive(manifest, first),
                brand_bundle.build_archive(manifest, second),
            )
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_invalid_version_fails_closed(self) -> None:
        with self.assertRaises(brand_bundle.BrandBundleError):
            brand_bundle.build_manifest("latest")


if __name__ == "__main__":
    unittest.main()
