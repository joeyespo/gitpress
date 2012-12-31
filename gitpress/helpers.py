import os
import shutil


def remove_directory(directory, show_warnings=True):
    """Deletes a directory and its contents.
    Returns a list of errors in form (function, path, excinfo)."""
    errors = []

    def onerror(function, path, excinfo):
        if show_warnings:
            print 'Cannot delete %s: %s' % (os.path.relpath(directory), excinfo[1])
        errors.append((function, path, excinfo))

    if os.path.exists(directory):
        shutil.rmtree(directory, onerror=onerror)

    return errors


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
