
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

    # Now we'll make a new object and use the mapper
    # to turn it into an insert statement.
    new_user = User()
    new_user.user_id = "00000004"
    new_user.username = "cheese"
    insert_stmt = mapper.insert_stmt_from_object(new_user)
    conn.execute(insert_stmt)

    # Now we can select this new object.
    # FIXME: Should provide column-like objects on the
    # mapper that can be used in expressions and automatically
    # apply the transform to the RHS so we don't need
    # to use the raw DB value here.
    select_stmt = (select( [ user_table ] )
                      .where(user_table.c.user_id == 4))
    new_result = conn.execute(select_stmt)
    new_user_selected = mapper.result_to_object(new_result)
    print repr(new_user_selected.__dict__)

    # We'll use the new_user object again to update
    # the object.
    # (but you could also start with a new object if you wanted)
    new_user.username = "ham"
    update_stmt = mapper.update_stmt_from_object(new_user,
                                                 no_where=True,
                                                 exclude_attrs=["user_id"])
    # FIXME: Eventually the update_stmt_from_object function
    # will do this automatically if no_where is omitted
    update_stmt = update_stmt.where(user_table.c.user_id == 4)
    conn.execute(update_stmt)

    # Now we can select the object again to get the updated version
    select_stmt = (select( [ user_table ] )
                      .where(user_table.c.user_id == 4))
    new_result = conn.execute(select_stmt)
    new_user_selected = mapper.result_to_object(new_result)
    print repr(new_user_selected.__dict__)

main()
