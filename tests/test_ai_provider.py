"""Verify provider routing and request compatibility without network calls."""
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import httpx
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bot"))
from core.ai import AIService


class ProviderTests(unittest.TestCase):
    def test_custom_provider_receives_both_chat_requests(self):
        for base_url in ("https://openwebui.example.test/api", "https://example.test/v1/"):
            with self.subTest(base_url=base_url):
                requests = []

                def respond(request):
                    requests.append(request)
                    return httpx.Response(200, json={
                        "id": "test", "object": "chat.completion", "created": 0,
                        "model": "custom-model",
                        "choices": [{"index": 0, "message": {
                            "role": "assistant", "content": "Provider reply"
                        }, "finish_reason": "stop"}],
                    })

                with httpx.Client(transport=httpx.MockTransport(respond)) as http:
                    def make_client(**kwargs):
                        return OpenAI(http_client=http, **kwargs)

                    with patch("core.ai.OpenAI", side_effect=make_client):
                        service = AIService("provider-key", "custom-model", base_url)
                    self.assertIn("Provider reply", service.get_summary("Alice: Hi", 1))
                    self.assertIn("Provider reply", service.get_mention_response("Hi", "Recent chat"))

                self.assertEqual(len(requests), 2)
                for request in requests:
                    self.assertEqual(str(request.url), base_url.rstrip("/") + "/chat/completions")
                    self.assertEqual(request.headers["authorization"], "Bearer provider-key")
                    payload = json.loads(request.content)
                    self.assertEqual(payload["model"], "custom-model")
                    self.assertEqual(payload["messages"][0]["role"], "system")
                    self.assertEqual(payload["messages"][-1]["role"], "user")
                    self.assertIn(payload["max_tokens"], (300, 500))

    def test_default_endpoint_is_preserved(self):
        with patch.dict(os.environ, {}, clear=True):
            service = AIService("test-key")
            try:
                self.assertEqual(str(service.client.base_url), "https://api.openai.com/v1/")
            finally:
                service.client.close()


if __name__ == "__main__":
    unittest.main()
