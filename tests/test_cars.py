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

    @patch('discord.ext.commands.cog')
    @patch('discord.webhook')
    @patch('database.Database')
    async def test_carcount_with_model(self, cog, webhook, database):
        webhook.send = AsyncMock()
        database.query_cars = MagicMock(return_value=[None] * 8)
        cars = Cars(cog, database)
        await cars.carcount(cars, webhook, model = "miata")
        database.query_cars.assert_called_once_with("miata")
        webhook.send.assert_called_once_with("There are 8 cars in the database!")

    @patch('discord.ext.commands.cog')
    @patch('discord.webhook')
    @patch('database.Database')
    async def test_rmcar_no_match(self, cog, webhook, database):
        webhook.send = AsyncMock()
        cars = Cars(cog, database)
        await cars.rmcar(cars, webhook, model = "a model that couldn't possibly exist")
        webhook.send.assert_called_once_with("I didn't find that car")

if __name__ == '__main__':
    unittest.main()