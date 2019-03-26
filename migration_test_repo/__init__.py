import pkg_resources

# read version
with open(pkg_resources.resource_filename('migration_test_repo', 'VERSION'), 'r') as file:
    __version__ = file.read().strip()

# API
from .core import GitMetadata, Test, Reference

