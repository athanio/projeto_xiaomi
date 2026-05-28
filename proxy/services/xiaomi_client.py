import os
import uuid
import httpx
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from dotenv import load_dotenv
import json

load_dotenv()


def build_url_with_query(base_url, **params):
    parsed = urlparse(base_url)
    query = dict(parse_qsl(parsed.query))
    query.update({k: v for k, v in params.items() if v is not None})
    return urlunparse(parsed._replace(query=urlencode(query)))


class XiaomiClient:

    def __init__(self):

        self.service_token = os.getenv("SERVICE_TOKEN")
        self.user_id = os.getenv("USER_ID")
        self.chatbot_ph = os.getenv("XIAOMI_CHATBOT_PH")
        self.model = os.getenv("XIAOMI_MODEL_NAME", "mimo-v2.5-pro")

        self.url = build_url_with_query(
            os.getenv("XIAOMI_API_URL", "https://aistudio.xiaomimimo.com/open-apis/bot/chat"),
            xiaomichatbot_ph=self.chatbot_ph,
        )

        self.headers = {
            "Cookie": (
                f"serviceToken={self.service_token}; "
                f"userId={self.user_id}; "
                f"xiaomichatbot_ph={self.chatbot_ph}"
            ),

            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Cache-Control": "no-cache",

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

    def _normalize_model_name(self, model_name):
        if not model_name:
            return None
        return model_name.strip().lower()

    def _parse_sse(self, text):
        events = []
        for block in text.strip().split("\n\n"):
            if not block.strip():
                continue
            event = {}
            for line in block.splitlines():
                if line.startswith("event:"):
                    event["event"] = line[len("event:"):].strip()
                elif line.startswith("data:"):
                    payload = line[len("data:"):].strip()
                    try:
                        event["data"] = json.loads(payload)
                    except Exception:
                        event["data"] = payload
            if event:
                events.append(event)
        return events

    async def ask(self, prompt, conversation_id=None, model=None):
        conversation_id = conversation_id or str(uuid.uuid4())
        msg_id = str(uuid.uuid4())
        model_name = self._normalize_model_name(model or self.model)

        payload = {
            "conversationId": conversation_id,
            "msgId": msg_id,
            "query": prompt,
            "isEditedQuery": False,
            "previousDialogueId": None,
            "params": {},
            "modelConfig": {
                "model": model_name,
                "enableThinking": False,
                "webSearchStatus": "disabled",
            },
            "multiMedias": [],
        }

        async with httpx.AsyncClient(timeout=120) as client:

            response = await client.post(
                self.url,
                headers=self.headers,
                json=payload
            )

            try:
                if "text/event-stream" in response.headers.get("content-type", ""):
                    return self._parse_sse(response.text)
                return response.json()

            except:
                return {
                    "status": response.status_code,
                    "response": response.text
                }