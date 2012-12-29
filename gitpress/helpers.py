import errno
import shutil


def copy_files(source, dest):
    """Copies a file or directory to the specified location."""
    try:
        shutil.copytree(source, dest)
    except OSError as exc:
        # Allow files to be copied also
        if exc.errno != errno.ENOTDIR:
            raise
        shutil.copy2(source, dest)
