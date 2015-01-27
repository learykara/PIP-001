
import argparse
import logging
import psycopg2
import sys


# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
connection = psycopg2.connect(
    "dbname='snippets' user='karaleary' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet):
    """
    Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values ('{}', '{}');"
    cursor.execute(command.format(name, snippet))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return an error

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "select * from snippets where keyword = '{}';"
    cursor.execute(command.format(name))
    snippet = cursor.fetchone()
    connection.commit()
    if snippet is None:
        return 'Error - snippet with keword {} not found'.format(name)
    logging.debug("Snippet retrieved successfully.")
    return snippet

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

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")

    arguments = parser.parse_args(sys.argv[1:])

    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))


if __name__ == "__main__":
    main()

