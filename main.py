"""Have You Tried Turning It Off? — make.fun entry.

Writes one original funny line — a hopeless tech support agent's reply
to a desperate customer — to /output/entry.txt (and a copy to entry.txt
beside this file). Deterministic, Python standard library only.

Structure: small validation helpers check the line, a writer helper
persists it, and a read-back helper confirms byte identity.
"""

import os
import sys

ENTRY = "Don't panic — turn the whole house off and on again, and if the fire's still there I'll escalate you to Tier 2."

MIN_LENGTH = 1
MAX_LENGTH = 200


def validate_length(line):
    """Entry must be between MIN_LENGTH and MAX_LENGTH characters."""
    if not MIN_LENGTH <= len(line) <= MAX_LENGTH:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(line))
        )


def validate_not_blank(line):
    """Entry must contain something other than whitespace."""
    if not line.strip():
        raise ValueError("entry must not be blank or whitespace-only")


def validate_single_line(line):
    """Entry must fit on one line: no newline or carriage return."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def validate_entry(line):
    """Run every validation rule over the entry line."""
    validate_length(line)
    validate_not_blank(line)
    validate_single_line(line)


def write_entry(path, data):
    """Write the encoded entry to ``path``, creating parent dirs."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def verify_readback(path, data, line):
    """Confirm ``path`` holds exactly ``data`` and decodes to ``line``."""
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != data:
        raise ValueError("read-back verification failed for %s" % path)
    if raw.decode("utf-8") != line:
        raise ValueError(
            "output is not valid UTF-8 text matching the entry: %s" % path
        )


def repo_entry_path():
    """Absolute path of the entry.txt copy next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.txt")


def main(argv=None):
    check_only = argv is not None and "--check-only" in argv
    line = ENTRY
    try:
        validate_entry(line)
    except ValueError as exc:
        sys.exit(str(exc))
    data = line.encode("utf-8")
    if check_only:
        # Dry run: validate the entry and confirm the existing outputs
        # already match, without writing anything.
        for path in ("/output/entry.txt", repo_entry_path()):
            try:
                verify_readback(path, data, line)
            except (ValueError, OSError) as exc:
                sys.exit(str(exc))
        print("Entry OK: %d characters, outputs verified" % len(line))
        return
    for path in ("/output/entry.txt", repo_entry_path()):
        write_entry(path, data)
        try:
            verify_readback(path, data, line)
        except ValueError as exc:
            sys.exit(str(exc))
    print("Wrote %d characters to /output/entry.txt" % len(line))


if __name__ == "__main__":
    main(sys.argv[1:])
