#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022-2023 Barcelona Supercomputing Center (BSC), Spain
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import argparse
import sys

from cffconvert.cli.create_citation import create_citation  # type: ignore[import]
from cffconvert.cli.validate_or_write_output import validate_or_write_output  # type: ignore[import]
from distutils.core import run_setup


def main() -> "None":
    ap = argparse.ArgumentParser(description="CFF validator and checker")
    ap.add_argument("cfffile", help="The CFF file to validate against ")
    ap.add_argument(
        "packagedir",
        help="Directory where the setup.py of the package is living",
        nargs="?",
        default=None,
    )

    args = ap.parse_args()

    if os.path.isfile(args.cfffile):
        packagedir = (
            os.path.dirname(args.cfffile)
            if args.packagedir is None
            else args.packagedir
        )
        citation = create_citation(args.cfffile, None)
        validate_or_write_output(
            outfile=None, outputformat=None, validate_only=True, citation=citation
        )
        # Now, validate version
        citver = citation._implementation.cffobj["version"]
        pkgdist = run_setup(os.path.join(packagedir, "setup.py"), script_args=["check"])
        if pkgdist.metadata.version != citver:
            print(f"Version mismatch: {pkgdist.metadata.version} vs {citver}")
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        print(f"File {args.cfffile} does not exist", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
