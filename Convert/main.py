import os
import sys
import shutil
import argparse
from Converter import Converter
from StructuralInfo import StructuralInfo
from pdf_to_markdown import (
    PrintDocument,
    print_document_raw_pages,
    set_warning_mode,
    set_debug_mode,
)

DEBUG = False


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert the Collecting Gold Dust book to markdown."
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        metavar="DIR",
        help="Relative path to output directory (default is CWD).",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run tests instead of converting.",
    )

    args = parser.parse_args()

    return args


def move_outputs_to_output_dir(output_dir):
    # Move all relevant output files
    input_dir = os.getcwd()
    converted_markdown_source = os.path.join(input_dir, "output.md")

    if not os.path.exists(converted_markdown_source):
        print(
            f"Converted markdown output file ({converted_markdown_source}) not found. Exiting."
        )
        sys.exit()

    converted_markdown_target = os.path.join(
        output_dir,
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md",
    )
    shutil.move(converted_markdown_source, converted_markdown_target)
    if DEBUG:
        print("Following file moved to output:")
        print(f"  - {converted_markdown_target}")


def convert():
    pdf_filename = os.path.join(
        os.path.dirname(__file__),
        "..",
        "original_data",
        "2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1.pdf",
    )

    if False:
        print_document_raw_pages(pdf_filename)

    # set_warning_mode(True)
    # set_debug_mode(True)
    converter = Converter(
        pdf_filename=pdf_filename,
        structural_info=StructuralInfo(),
    )
    document = converter.get_document()
    # Generate the markdown file
    document.to_markdown("output.md")

    # On debugging purposes
    if False:
        PrintDocument(document).pages()
        PrintDocument(document).paragraphs()
        PrintDocument(document).sentences()


if __name__ == "__main__":
    args = parse_arguments()
    if args.output_directory and not os.path.isdir(args.output_directory):
        print(f"Output directory not found: {args.output_directory!r}")
        sys.exit(1)
    if args.test:
        import subprocess
        result = subprocess.run(["pytest", "test_main.py"])
        sys.exit(result.returncode)
    convert()
    if args.output_directory:
        move_outputs_to_output_dir(args.output_directory)
