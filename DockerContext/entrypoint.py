# Producing the content of result_data directory
import pathlib
import os
import sys
import subprocess

if __name__ == "__main__":
    this_script_dir = pathlib.Path(__file__).parent.resolve()
    converter_dir = os.path.join(this_script_dir, "Convert")
    convert_script_file = os.path.join(converter_dir, "main.py")
    if not os.path.exists(convert_script_file):
        print(f"Converter script ({convert_script_file}) not found. Exiting.")
        sys.exit()

    args = [convert_script_file, "--output_directory", sys.argv]
    print("AAAAAAAAAAAAAAAAA args", args)
    # subprocess.Popen([sys.executable, convert_script_file])
