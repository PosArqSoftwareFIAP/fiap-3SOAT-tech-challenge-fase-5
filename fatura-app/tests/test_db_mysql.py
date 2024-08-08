import pytest
from unittest.mock import patch, MagicMock
import config
from src.db.db_mysql import db_mysql_class

class TestDbMysqlClass:

    @patch('src.db.db_mysql.mysql.connector.connect')
    def test_get_db_connection(self, mock_connect):
        # Arrange
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        db_instance = db_mysql_class()
        
        expected_db_config = {
            'host':     config.db_host,
            'user':     config.db_user,
            'password': config.db_password,
            'port':     config.db_port,
            'database': config.db_database
        }

        # Act
        result = db_instance.get_db_connection()

        # Assert
        mock_connect.assert_called_with(**expected_db_config)
        assert result == mock_connection

    def test_init(self):
        # Act
        db_instance = db_mysql_class()

        # Assert
        assert db_instance.db_config == {
            'host':     config.db_host,
            'user':     config.db_user,
            'password': config.db_password,
            'port':     config.db_port,
            'database': config.db_database
        }
