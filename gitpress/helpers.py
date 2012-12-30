import errno
import shutil


def copy_dir(source, dest):
    """Copies a file or directory to the specified location."""
    try:
        shutil.copytree(source, dest)
    except OSError as exc:
        # Allow files to be copied also
        if exc.errno != errno.ENOTDIR:
            raise
        shutil.copy2(source, dest)


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
