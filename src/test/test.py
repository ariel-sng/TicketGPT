import sys
import types
import unittest
from unittest.mock import Mock

# Inyectamos un módulo "openai" falso para evitar dependencia externa
fake_openai = types.ModuleType("openai")

class DummyOpenAI:
    pass

fake_openai.OpenAI = DummyOpenAI

sys.modules["openai"] = fake_openai

from src.utils.openai_service import ask_openai

class TestAskOpenAI(unittest.TestCase):
    def test_ask_openai_token_sum_is_correct(self):
        client_mock = Mock()
        input_tokens = 50
        output_tokens = 70
        total_tokens = input_tokens + output_tokens

        usage = Mock()
        usage.input_tokens = input_tokens
        usage.output_tokens = output_tokens
        usage.total_tokens = total_tokens

        response = Mock()
        response.usage = usage

        client_mock.responses.parse = Mock(return_value=response)

        result, elapsed = ask_openai(client_mock, "system prompt", "user prompt")

        self.assertEqual(result.usage.input_tokens, input_tokens)
        self.assertEqual(result.usage.output_tokens, output_tokens)
        self.assertEqual(result.usage.total_tokens, total_tokens)
        self.assertEqual(result.usage.input_tokens + result.usage.output_tokens, result.usage.total_tokens)
        self.assertIsInstance(elapsed, float)
        self.assertGreater(elapsed, 0)

if __name__ == "__main__":
    unittest.main()
