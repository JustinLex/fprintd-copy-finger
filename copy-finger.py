import os

import click
import gi
gi.require_version('FPrint', '2.0')
from gi.repository import FPrint


@click.command()
@click.argument('fingerprint_path', help='Path to the existing fingerprint file')
@click.argument('new_user', help='username of the user to add the fingerprint to')
def copy_fingerprint(fingerpint_path: str, new_user: str):
    """
    Tool to copy a fingerprint from one user to another.

    Must be run as root.
    """
    # Duplication code found from tests here:
    # https://github.com/freedesktop/libfprint-fprintd/blob/b440acb57daf0459f2b8b8de82d8284c2040b720/tests/fprintd.py#L827
    print(f"We will copy fingerprint from {fingerpint_path} to user {new_user}")
    print("Note that duplicated fingers is NOT SUPPORTED by fprintd for a reason!"
          "Use of this tool may break the ability to identify a user by their fingerprint. No warranty is implied.")
    print("See comment here for why duplicate fingers are not supported:\n"
          "https://gitlab.freedesktop.org/libfprint/fprintd/-/blob/master/src/device.c#L2226")

    with open(fingerpint_path, "rb") as orig_file:
        dup_print = FPrint.Print.deserialize(orig_file.read())

    current_user = dup_print.get_username()
    print(f"Copying {dup_print.get_finger} finger from user {current_user}")
    dup_print.set_username(new_user)
    print(f'Successfully applied new username "{new_user}" to print.')

    # Reuse path structure from original file.
    # Note that the path is specific to device and finger.
    # We don't support the logic to convert here, nor would that make sense.
    new_fp_path = fingerpint_path.replace(current_user, new_user)
    os.makedirs(os.path.dirname(new_fp_path), exist_ok=True)

    with open(new_fp_path, "wb") as new_file:
        new_file.write(dup_print.serialize())
    print(f'Fingerprint successfully copied! Try out the fingerprint with the fprintd-verify tool.')


if __name__ == "__main__":
    copy_fingerprint()
