# python -m plugins.hash *COMMAND*

Tools for hashing.

## check

Check the hash for a path.

Args:
- `path` (positional): the path to check.
- `hashes` (positional): the hashes file to check against. Should be in either JSON or YAML format.
- `--log-file`: the log file to write the results to (in addition to console output) if specified.

## create

Create the hash for a path.

Args:
- `path` (positional): the path to create hashes from.
- `hashes` (positional): the hashes file to write to. Should be in either JSON or YAML format.
- `--algorithms`: algorithms to use for the hashing. If not specified, a default selection of algorithms will be used.