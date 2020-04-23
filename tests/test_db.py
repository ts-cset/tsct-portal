import psycopg2
import pytest

from portal.db import get_db


def test_get_db_then_close(app):
    # Start up the app and check for a database connection while it's running
    with app.app_context():
        db = get_db()
        assert db is get_db(), 'get_db should always return the same connection'

    # After app closes, database connection should close automatically so
    # running any queries with it should throw an error
    with pytest.raises(psycopg2.InterfaceError) as error:
        cur = db.cursor()
        cur.execute('SELECT 1')
        assert 'closed' in str(error)


# Run the following test twice to check both database CLI commands
@pytest.mark.parametrize(('function', 'command', 'output'), [
    ('portal.db.init_db', 'init-db', 'Initialized the database.'),
    ('portal.db.mock_db', 'mock-db', 'Inserted mock data.'),
    ('portal.db.import_csv', 'import-csv', 'Inserted csv data')
])
def test_cli_commands(runner, monkeypatch, function, command, output):
    # Create class to safely track state of function calls
    class Recorder(object):
        called = False

    # Create a stub function to run instead of the original that toggles
    # the recorder state. We don't need to call the original since they're
    # running before every test anyways (see fixtures in conftest.py).
    def cli_stub():
        Recorder.called = True

    # Replace the original import with the stub
    monkeypatch.setattr(function, cli_stub)
    # Use the CLI runner to call the function
    result = runner.invoke(args=[command])
    # Check CLI output and verify the stub was called
    assert output in result.output
    assert Recorder.called
