
import argparse
import logging
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)


def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error(
        "FIXME: Unimplemented - put({!r}, {!r}".format(name, snippet))
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return an error

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""


def delete(name):
    """Delete the snippet with a given name.

    If there is no such snippet, return an error
    """
    logging.error("FIXME: Unimplemented - delete({!r})".format(name))


def update(name, snippet):
    """Replace the existing snippet with a given name.

    If there is no such snippet, create one.

    Returns the snippet.
    """
    logging.error(
        "FIXME: Unimplemented - update({!r}, {!r})".format(name, snippet))


def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(
        description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")
    
    # Subparser for the put command
    logging.debug("Constructing put subparser") # QQ: why is this debug when above is info?
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet of text")

    arguments = parser.parse_args(sys.argv[1:])


if __name__ == "__main__":
    main()

