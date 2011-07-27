
from sqlalchemy import *
from sqlalchemy import sql
from conjurer import *

metadata = MetaData()


# SQLAlchemy standard table object
user_table = Table('user', metadata,
                   Column('user_id', Integer, primary_key=True),
                   Column('username', String(16), nullable=False))


# Plain Old Python Object that we'll map to.
class User(object):
    pass


# A really simple example mapper that does a transform
# on user_id and just lets username get mapped directly
# by leaving it out of custom_mappings.
mapper = Mapper(user_table, User, custom_mappings={
    user_table.c.user_id: ("user_id", PaddedHexTransform()),
})


def main():
    global metadata, user_table, User

    # Use in-memory SQLite for this example
    engine = create_engine("sqlite://")
    metadata.create_all(engine)
    conn = engine.connect()

    # Insert some dummy data
    conn.execute("insert into user values (1, \"foo\")")
    conn.execute("insert into user values (2, \"bar\")")
    conn.execute("insert into user values (3, \"baz\")")

    # Use normal SQLAlchemy select statement to
    # select all of the rows from the user table.
    result = conn.execute(select( [ user_table ] ))

    # Use the mapper to get an object iterator from
    # the result and print out the internal dictionaries
    # of the objects to prove they were populated.
    for user in mapper.result_to_object_iter(result):
        print repr(user.__dict__)


main()
