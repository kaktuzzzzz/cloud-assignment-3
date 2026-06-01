#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import zipfile
import gdown
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class AssetLoader:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.zip_path = self.base_dir / "public_release.zip"
        self.public_dir = self.base_dir / "public"
        self.temp_dir = self.base_dir / "temp_extract_zone"

    def log(self, message: str, color: str = Colors.BLUE):
        print(f"{color}ℹ️  {message}{Colors.ENDC}")

    def clean_system_artifacts(self, target_dir: Path) -> None:
        macosx = target_dir / "__MACOSX"
        if macosx.exists():
            shutil.rmtree(macosx)
        
        for path in target_dir.rglob("*"):
            if path.name == ".DS_Store":
                path.unlink()

    def download_assets(self, file_id: str) -> None:
        self.log(f"Downloading assets (ID: {file_id})...", Colors.BLUE)
        try:
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, str(self.zip_path), quiet=False)
        except Exception as e:
            print(f"{Colors.FAIL}❌ Download failed: {e}{Colors.ENDC}")
            sys.exit(1)

    def install_assets(self) -> None:
        self.log("Installing assets to 'public/'...", Colors.BLUE)

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
        except zipfile.BadZipFile:
            print(f"{Colors.FAIL}❌ Error: Corrupted zip file.{Colors.ENDC}")
            sys.exit(1)

        self.clean_system_artifacts(self.temp_dir)

        source_root = self.temp_dir
        if (self.temp_dir / "public").exists():
             source_root = self.temp_dir / "public"

        if not self.public_dir.exists():
            self.public_dir.mkdir()

        for item in source_root.iterdir():
            if item.is_dir():
                dest_path = self.public_dir / item.name
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                
                shutil.move(str(item), str(dest_path))
                self.log(f"Updated: public/{item.name}", Colors.CYAN)

        shutil.rmtree(self.temp_dir)
        if self.zip_path.exists():
            self.zip_path.unlink()

    def run(self):
        file_id = os.getenv("GDRIVE_ID")
        if not file_id:
            print(f"{Colors.FAIL}❌ Error: GDRIVE_ID not found in .env{Colors.ENDC}")
            sys.exit(1)
        
        self.download_assets(file_id)
        self.install_assets()
        print(f"{Colors.GREEN}✅ Setup complete.{Colors.ENDC}")

if __name__ == "__main__":
    AssetLoader().run()
