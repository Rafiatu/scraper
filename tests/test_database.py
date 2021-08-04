from db import DB


def test_database_connects_properly_and_returns_cursor():
    assert DB().connect() is not None


def test_database_sets_up_tables_properly():
    db = DB()
    db.connect()
    assert db.setup_tables() is None
