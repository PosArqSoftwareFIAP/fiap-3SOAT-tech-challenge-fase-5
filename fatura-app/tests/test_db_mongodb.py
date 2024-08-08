import pytest
from unittest.mock import patch, MagicMock
import config
from src.db.db_mongodb import db_mongo_class

class TestDbMongoClass:

    @patch('src.db.db_mongodb.MongoClient')
    def test_init(self, mock_mongo_client):
        # Arrange
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        # Act
        db_instance = db_mongo_class()

        # Assert
        mock_mongo_client.assert_called_with(f"mongodb+srv://{config.mongo_user}:{config.mongo_senha}@mongo-fiap-food-936cf8b1.mongo.ondigitalocean.com/")
        assert db_instance.client == mock_client

    @patch('src.db.db_mongodb.MongoClient')
    def test_get_collection(self, mock_mongo_client):
        # Arrange
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.get_collection.return_value = mock_collection
        mock_client = MagicMock()
        mock_client.__getitem__.return_value = mock_db
        mock_mongo_client.return_value = mock_client

        db_instance = db_mongo_class()

        # Act
        result = db_instance.get_collection()

        # Assert
        mock_client.__getitem__.assert_called_with(config.mongo_db)
        mock_db.get_collection.assert_called_with(config.mongo_collection)
        assert result == mock_collection

if __name__ == '__main__':
    pytest.main()