import os
import re
import shutil


def truncate_filename(filename, max_length=64):
    """Truncate filename from the left to fit within the max_length constraint, keeping the extension."""
    name, ext = os.path.splitext(filename)
    if len(filename) > max_length:
        truncated_name = name[-(max_length - len(ext)):]  # Keep only the last part
        return truncated_name + ext
    return filename


def find_and_replace_tex_links(tex_file):
    """Find all linked files in a .tex file and update paths."""
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_content = f.read()

    # Regular expressions for various included file types
    patterns = [
        r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',  # Images and figures
        r'\\input\{([^}]+)\}',  # Input files
        r'\\bibliography\{([^}]+)\}',  # Bibliography files
        r'\\include\{([^}]+)\}'  # Other included files
    ]

    matched_files = set()
    for pattern in patterns:
        matches = re.findall(pattern, tex_content)
        matched_files.update(matches)

    renamed_files = {}

    for old_path in matched_files:
        new_path = old_path.replace(os.sep, "_")  # Replace path separators
        new_path = truncate_filename(new_path)  # Truncate if necessary
        renamed_files[old_path] = new_path
        tex_content = tex_content.replace(old_path, new_path)  # Update .tex content

    # Save the updated .tex file
    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(tex_content)

    return renamed_files


def move_and_rename_files(root_dir, renamed_files):
    """Move files from subdirectories to root directory with renamed paths."""
    for old_path, new_path in renamed_files.items():
        full_old_path = os.path.join(root_dir, old_path)

        if os.path.exists(full_old_path):
            full_new_path = os.path.join(root_dir, new_path)
            shutil.move(full_old_path, full_new_path)
            print(f"Moved: {full_old_path} -> {full_new_path}")


def flatten_directory(root_dir):
    """Move all files from subdirectories to the root, renaming them."""
    for subdir, _, files in os.walk(root_dir):
        if subdir == root_dir:
            continue  # Skip the root itself

        for file in files:
            old_path = os.path.join(subdir, file)
            new_name = old_path.replace(root_dir + os.sep, "").replace(os.sep, "_")
            new_name = truncate_filename(new_name)  # Apply truncation
            new_path = os.path.join(root_dir, new_name)

            if os.path.exists(new_path):
                print(f"Warning: File {new_name} already exists! Skipping.")
                continue

            shutil.move(old_path, new_path)
            print(f"Moved: {old_path} -> {new_path}")

    # Remove empty subdirectories
    for subdir, _, _ in os.walk(root_dir, topdown=False):
        if subdir != root_dir and not os.listdir(subdir):
            os.rmdir(subdir)
            print(f"Removed empty directory: {subdir}")
