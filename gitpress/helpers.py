import os
import errno
import shutil


def copy_file_tree(source, dest):
    """Copies a file or directory to the specified location."""
    try:
        shutil.copytree(source, dest)
    except OSError as exc:
        # Allow files to be copied also
        if exc.errno != errno.ENOTDIR:
            raise
        shutil.copy2(source, dest)


def copy_files(source_files, target_directory, source_directory=None):
    """Copies a list of files to the specified directory.
    If source_directory is provided, it will be prepended to each source file."""
    try:
        os.makedirs(target_directory)
    except:     # TODO: specific exception?
        pass
    for f in source_files:
        source = os.path.join(source_directory, f) if source_directory else f
        target = os.path.join(target_directory, f)
        shutil.copy2(source, target)


def yes_or_no(message):
    """Gets user input and returns True for yes and False for no."""
    while True:
        print message, '(yes/no)',
        line = raw_input()
        if line is None:
            return None
        line = line.lower()
        if line == 'y' or line == 'ye' or line == 'yes':
            return True
        if line == 'n' or line == 'no':
            return False
