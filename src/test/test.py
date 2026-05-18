import sys
import types
import unittest
from unittest.mock import Mock, patch

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

from src.utils.openai_service import log_metrics

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
    def test_log_metrics_records_token_counts(self):
        usage = FakeUsage(input_tokens=50, output_tokens=70, total_tokens=120)
        response = FakeResponse(usage)
        with patch("src.utils.openai_service.log") as fake_log:
            log_metrics(response, 15.0)

        expected_cost = (50 / 1_000_000) * 0.40 + (70 / 1_000_000) * 1.60
        fake_log.assert_called_once()
        register = fake_log.call_args.args[0]
        self.assertEqual(register["tokens_prompt"], 50)
        self.assertEqual(register["tokens_completions"], 70)
        self.assertEqual(register["total_tokens"], 120)
        self.assertEqual(register["latency_ms"], 15.0)
        self.assertAlmostEqual(register["estimated_cost_usd"], round(expected_cost, 8))

if __name__ == "__main__":
    unittest.main()
