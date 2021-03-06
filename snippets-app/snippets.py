import argparse
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
    with connection, connection.cursor() as cursor:
        try:
            cursor.execute(
                "insert into snippets values (%s, %s)", (
                name, snippet))
        except psycopg2.IntegrityError as e:
            connection.rollback()
            cursor.execute(
                "update snippets set message = %s"
                " where keyword = %s", (snippet, name))
    logging.debug("Snippet stored successfully.")
    return name, snippet


def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return an error

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    with connection, connection.cursor() as cursor: # context manager
        cursor.execute(
            "select message from snippets where keyword = %s", (name,))
        row = cursor.fetchone()
    if row is None:
        return None
    logging.debug("Snippet retrieved successfully.")

    return row[0]


def delete(name):
    """Delete the snippet with a given name.

    Return the name of the snippet.
    """
    logging.info("Deleting snippet {!r}".format(name))
    with connection, connection.cursor() as cursor:
        cursor.execute(
            "delete from snippets where keyword = %s", (name,))
    logging.debug("Snippet deleted successfully.")
    return name


def catalog():
    """Return a list of existing keywords.
    """
    logging.info("Retrieving the snippet catalog.")
    keywords = []
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword")
        keywords = [row[0] for row in cursor.fetchall()]
    logging.info("Catalog retrieved successfully")
    return keywords


def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(
        description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet of text")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")

    # Subparser for the delete command
    logging.debug("Constructing delete subparser")
    delete_parser = subparsers.add_parser("delete", help="Delete a snippet")
    delete_parser.add_argument("name", help="The name of the snippet")

    # Subparser for the catalog
    logging.debug("Constructing the catalog subparser")
    catalog_parser = subparsers.add_parser(
        "catalog", help="See existing snippet keywords")

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
    elif command == "delete":
        name = delete(**arguments)
        print("Deleted snippet: {!r}".format(name))
    elif command == "catalog":
        names = catalog()
        print("Available snippets:\n {}".format(names))


if __name__ == "__main__":
    main()

