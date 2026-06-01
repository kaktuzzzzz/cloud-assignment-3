#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import shutil
import zipfile
from pathlib import Path

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class AssetPacker:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.public_dir = self.base_dir / "public"
        self.output_filename = "public_release.zip"
        self.output_path = self.base_dir / self.output_filename
        self.targets = ["data", "images"] 

    def log(self, message: str, color: str = Colors.BLUE):
        print(f"{color}  {message}{Colors.ENDC}")

    def clean_junk_files(self) -> None:
        self.log(f"Sanitizing targets: {', '.join(self.targets)}...", Colors.CYAN)
        for target in self.targets:
            target_path = self.public_dir / target
            if not target_path.exists():
                continue
            for path in target_path.rglob("*"):
                if path.is_file():
                    if path.name == ".DS_Store" or path.name.startswith("._"):
                        try:
                            path.unlink()
                        except OSError:
                            pass

    def compress_assets(self) -> None:
        self.log(f"Packing specific folders into '{self.output_filename}'...", Colors.BLUE)
        if self.output_path.exists():
            self.output_path.unlink()
        try:
            with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                files_count = 0
                for target in self.targets:
                    target_path = self.public_dir / target
                    if not target_path.exists():
                        continue
                    for file_path in target_path.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(self.public_dir)
                            zipf.write(file_path, arcname)
                            files_count += 1
            self.log(f"Packed {files_count} files successfully!", Colors.GREEN)
        except Exception as e:
            print(f"{Colors.FAIL} Packing failed: {e}{Colors.ENDC}")
            sys.exit(1)

    def run(self):
        self.clean_junk_files()
        self.compress_assets()

if __name__ == "__main__":
    AssetPacker().run()
