# The script is targeting 3.6 to be able to support centos 7 and above
import json
import fnmatch
import shutil
import time
from pathlib import Path
from typing import List, Optional

# In and out directories
INPUT_DIRECTORY = Path("/app/transfer/sftp/in")
OUTPUT_DIRECTORY = Path("/app/transfer/sftp/out")
# Config file and holding place for possible output files
CONFIG_FILE = Path("/app/config.json")
OUTPUT_FILES = Path("/app/outputfiles/")


class ConfigEntry:
    def __init__(self, input_filename_pattern: str, output_files: List[Path],
                  input_byte_check: Optional[bytes]):
        self.input_filename_pattern = input_filename_pattern
        self.output_files = output_files
        self.input_byte_check = input_byte_check

    def matches(self, input_file: Path) -> bool:
        """
        Given a input file, does it match the input filename check and input byte check
        :param input_file: the file to check
        :return: True if it matches and the output files should be used
        """
        if not input_file.exists():
            return False

        if fnmatch.fnmatch(input_file.name, self.input_filename_pattern):
            if self.input_byte_check is None:
                return True

            return self.input_byte_check in input_file.read_bytes()

        return False

    @classmethod
    def parse_config(cls, config_file: Path) -> List["ConfigEntry"]:
        config_json = json.loads(config_file.read_text())
        config_entries = []
        for key in config_json:
            entry = config_json[key]
            input_filename_pattern: str = key
            output_files = []
            for output_file in entry.get("output_files", []):
                output_file = Path(output_file)
                if output_file.exists():
                    output_files.append(output_file)
                elif OUTPUT_FILES.joinpath(output_file).exists():
                    output_files.append(OUTPUT_FILES.joinpath(output_file))

            input_byte_check = entry.get("input_byte_match", None)
            if input_byte_check:
                input_byte_check = bytes.fromhex(input_byte_check)
            else:
                input_byte_check = None

            config_entries.append(cls(input_filename_pattern, output_files, input_byte_check))
        return config_entries


def safe_copy(source_file: Path, destination_directory: Path):
    hidden_file = destination_directory.joinpath("." + source_file.name)
    unhidden_file = destination_directory.joinpath(source_file.name)
    shutil.copy(str(source_file), str(hidden_file))
    hidden_file.chmod(0o660)
    shutil.chown(hidden_file, user=1002, group=1002)
    hidden_file.rename(unhidden_file)


def _main():
    # Parse config
    config_entries = ConfigEntry.parse_config(Path(CONFIG_FILE))

    while True:
        for file in INPUT_DIRECTORY.iterdir():
            if file.name.startswith("."):
                # ignore "hidden" files
                continue

            for entry in config_entries:
                if entry.matches(file):
                    for output_file in entry.output_files:
                        safe_copy(output_file, OUTPUT_DIRECTORY)
            file.unlink()
        time.sleep(1)


if __name__ == "__main__":
    _main()
