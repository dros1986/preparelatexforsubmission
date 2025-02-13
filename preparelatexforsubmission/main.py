import os
import argparse
from .processor import find_and_replace_tex_links, move_and_rename_files, flatten_directory


def main():
    parser = argparse.ArgumentParser(
        description="Prepare a LaTeX project for journal submission by flattening directories and updating paths."
    )
    parser.add_argument("tex_file", help="Path to the main LaTeX file")

    args = parser.parse_args()
    tex_file = args.tex_file

    if not os.path.exists(tex_file):
        print(f"Error: The file '{tex_file}' does not exist.")
        return

    # Get root directory where .tex is located
    root_dir = os.path.dirname(os.path.abspath(tex_file))

    print(f"Processing LaTeX file: {tex_file}")

    # Find and replace links in .tex file
    renamed_files = find_and_replace_tex_links(tex_file)

    # Move and rename files
    move_and_rename_files(root_dir, renamed_files)

    # Flatten the directory structure
    flatten_directory(root_dir)

    print("Processing completed successfully.")


if __name__ == "__main__":
    main()
