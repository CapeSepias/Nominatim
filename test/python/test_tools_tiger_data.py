"""
Test for tiger data function
"""
from pathlib import Path

import pytest

from nominatim.tools import tiger_data, database_import


@pytest.mark.parametrize("threads", (1, 5))
def test_add_tiger_data(dsn, src_dir, def_config, monkeypatch,tmp_path,
                        temp_db_cursor, threads, temp_db):
    monkeypatch.setenv('NOMINATIM_DATABASE_MODULE_PATH', '.')
    temp_db_cursor.execute('CREATE EXTENSION hstore')
    temp_db_cursor.execute('CREATE EXTENSION postgis')
    temp_db_cursor.execute('CREATE TABLE place (id INT)')

    database_import.import_base_data('dbname=' + temp_db, src_dir / 'data',
                                     ignore_partitions=False)
    sqlfile = tmp_path / '1010.sql'
    sqlfile.write_text("""INSERT INTO place values (1)""")
    tiger_data.add_tiger_data(dsn, str(tmp_path), threads, def_config, src_dir / 'lib-sql')

    assert temp_db_cursor.table_rows('place') == 1