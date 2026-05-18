import sys
import types
import unittest
from unittest.mock import Mock

# Inyectamos un módulo `openai` falso para evitar dependencia externa
fake_openai = types.ModuleType("openai")

class DummyOpenAI:
    pass

fake_openai.OpenAI = DummyOpenAI

sys.modules["openai"] = fake_openai

# Inyectamos un `pydantic` mínimo para que `ChatResponse` pueda importarse sin la dependencia
fake_pydantic = types.ModuleType("pydantic")
class FakeBaseModel:
    pass
def Field(*args, **kwargs):
    return None
fake_pydantic.BaseModel = FakeBaseModel
fake_pydantic.Field = Field
sys.modules["pydantic"] = fake_pydantic

from src.utils.openai_service import ask_openai
from src.models.chat_response_ai import ChatResponse

class FakeUsage:
    def __init__(self, input_tokens=0, output_tokens=0, total_tokens=0):
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = total_tokens
        self.latency_ms = None

class FakeResponse:
    def __init__(self, usage):
        self.usage = usage

class TestAskOpenAI(unittest.TestCase):
    def test_calls_client_with_expected_parameters(self):
        client_mock = Mock()
        usage = FakeUsage(10, 20, 30)
        response = FakeResponse(usage)
        client_mock.responses.parse = Mock(return_value=response)

        system_prompt = "system text"
        user_prompt = "user text"
        result, elapsed = ask_openai(client_mock, system_prompt, user_prompt)

        client_mock.responses.parse.assert_called_once()
        called_kwargs = client_mock.responses.parse.call_args.kwargs
        self.assertEqual(called_kwargs.get("model"), "gpt-4.1-mini")
        self.assertEqual(called_kwargs.get("temperature"), 0.1)
        self.assertEqual(called_kwargs.get("text_format"), ChatResponse)
        inp = called_kwargs.get("input")
        self.assertIsInstance(inp, list)
        self.assertEqual(inp[0]["role"], "system")
        self.assertEqual(inp[0]["content"], system_prompt)
        self.assertEqual(inp[1]["role"], "user")
        self.assertEqual(inp[1]["content"], user_prompt)
        self.assertIs(result, response)
        self.assertIsInstance(elapsed, float)
        self.assertGreater(elapsed, 0)

    def test_response_latency_set_and_returned_elapsed(self):
        client = Mock()
        usage = FakeUsage(5, 7, 12)
        response = FakeResponse(usage)
        client.responses.parse = Mock(return_value=response)

        result, elapsed = ask_openai(client, "s", "u")
        self.assertIs(result, response)
        # decorator returns elapsed time and function sets usage.latency_ms
        self.assertIsNotNone(response.usage.latency_ms)
        self.assertIsInstance(response.usage.latency_ms, float)
        self.assertIsInstance(elapsed, float)
        self.assertGreater(elapsed, 0)

if __name__ == "__main__":
    unittest.main()
