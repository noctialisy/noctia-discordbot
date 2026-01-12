# Main testing file see Test class for tests
import asyncio

from game_classes.Test import Test

# Create tester instance
tester = Test()

# Run tests
tester.test_db()
tester.test_character()
tester.test_enemy()
asyncio.run(tester.clean_test())