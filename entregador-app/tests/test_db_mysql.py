import pytest
from unittest.mock import patch, MagicMock
from src.db import db_mysql_class
import sys,os
sys.path.insert(0, os.path.abspath('/home/runner/.local/lib/python3.10/site-packages')) 
from flask_testing import TestCase


@patch('src.db.db_mysql_class.get_db_connection')
def test_get_db_connection(mock_get_db_connection):
    # Mock the return value of the database connection
    mock_conn = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    
    db = db_mysql_class()
    conn = db.get_db_connection()
    
    mock_get_db_connection.assert_called_once()
    assert conn == mock_conn

if __name__ == '__main__':
    pytest.main()
