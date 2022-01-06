import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import AsyncMock

from cogs.cars import Cars

class TestCars(unittest.IsolatedAsyncioTestCase):

    @patch('discord.ext.commands.cog')
    @patch('discord.webhook')
    @patch('database.Database')
    async def test_carcount(self, cog, webhook, database):
        webhook.send = AsyncMock()
        database.fetch_all_cars = MagicMock(return_value=[None] * 252)
        cars = Cars(cog, database)
        await cars.carcount(cars, webhook)
        webhook.send.assert_called_once_with("There are 252 cars in the database!")

if __name__ == '__main__':
    unittest.main()