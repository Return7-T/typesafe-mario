import json

import httpx2
from typesafe_sdk import Choice, TypeSafeClient

from typesafe_mario.openrouter import OpenRouterTransport


def test_openrouter_preserves_decisions_and_auth():
    def respond(request):
        assert str(request.url) == "https://openrouter.ai/api/alpha/decisions"
        assert request.headers["Authorization"] == "Bearer test-key"
        assert request.headers["host"] == "openrouter.ai"
        body = json.loads(request.content)
        assert body["model"] == "typesafe/jev-1.13"
        assert body["state"] == {"x": 40}
        question = body["questions"]["action"]
        assert json.loads(question["instructions"]) == {"goal": "advance"}
        assert question["criteria"] == {"right": "Move right"}
        assert int(request.headers["content-length"]) == len(request.content)
        return httpx2.Response(
            200,
            json={
                "model": "typesafe/jev-1.13",
                "usage": {"input_tokens": 10, "output_tokens": 0, "cost": 0.0},
                "answers": {
                    "action": {
                        "type": "choice",
                        "choice": "right",
                        "confidence": 0.9,
                        "probabilities": {"right": 0.9},
                    }
                },
            },
        )

    with TypeSafeClient(
        api_key="test-key",
        model="typesafe/jev-1.13",
        transport=OpenRouterTransport(httpx2.MockTransport(respond)),
    ) as client:
        answer = client.system_one(
            state={"x": 40},
            questions={
                "action": Choice(instructions={"goal": "advance"}, criteria={"right": "Move right"})
            },
        )
    assert answer.choices["action"].choice == "right"
    assert answer.choices["action"].confidence == 0.9
