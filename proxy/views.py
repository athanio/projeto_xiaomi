
import re
import json
import urllib.parse as up

from ninja import NinjaAPI, Form
from pydantic import Field
from typing import Annotated

from .services.xiaomi_client import XiaomiClient

# ==========================================
# API
# ==========================================

api = NinjaAPI(
    title="IFPI Proxy API",
    version="1.0.0",
    description="API Proxy para comunicação com IA"
)

# ==========================================
# CLEAN RESPONSE
# ==========================================

def _clean_response_text(text: str) -> str:

    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = text.replace("\\u0000", " ")
    text = text.replace("**", "")
    text = text.replace("[DONE]", "")

    text = re.sub(r"^\s*\d+\s*", "", text)

    text = re.sub(
        r"The user is asking.*?Portuguese\.?",
        "",
        text,
        flags=re.IGNORECASE
    )

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    clean_lines = []

    for line in lines:

        if re.match(
            r"^The user is asking",
            line,
            flags=re.IGNORECASE
        ):
            continue

        clean_lines.append(line)

    texto = " ".join(clean_lines)

    texto = re.sub(r"<think>|</think>", "", texto)

    texto = re.sub(
        r"\(citation:\d+\)",
        "",
        texto
    )

    texto = re.sub(r"#{1,6}", "", texto)

    texto = re.sub(
        r"\|[-\s:]+\|",
        "",
        texto
    )

    anchors = [
        r"\b[Aa] capital\b",
        r"capital\s+do\s+Brasil",
        r"\bBras[ií]lia\b",
        r"\b[Aa] capital do\b"
    ]

    for anchor in anchors:

        match = re.search(
            anchor,
            texto,
            flags=re.IGNORECASE
        )

        if match:
            texto = texto[match.start():].strip()
            break

    if not any(
        re.search(a, texto, flags=re.IGNORECASE)
        for a in anchors
    ):

        match = re.search(
            r"[\u00C0-\u017F]",
            texto
        )

        if match:
            texto = texto[match.start():].strip()

    texto = re.sub(
        r"The user is asking.*?\.",
        "",
        texto,
        flags=re.IGNORECASE
    )

    texto = re.sub(
        r"Let me .*?\.",
        "",
        texto,
        flags=re.IGNORECASE
    )

    return texto.strip()

# ==========================================
# HEALTH
# ==========================================

@api.get(
    "/health",
    tags=["Sistema"]
)
def health(request):

    return {
        "status": "ok"
    }

# ==========================================
# CHAT
# ==========================================

@api.post(
    "/chat",
    tags=["IA"]
)
async def chat(

    request,

    pergunta: Annotated[
        str,
        Field(
         default="",
         description="Digite sua pergunta para IA",
         example="Qual a capital da Noroega?",
         json_schema_extra={
            "placeholder": "Qual a capital do Noroega?"
        }
    )
    ] = Form(...)

):

    # ==========================================
    # VALIDAÇÃO
    # ==========================================

    if not pergunta:

        return {
            "response": "Nenhuma pergunta enviada."
        }

    # ==========================================
    # CLIENT
    # ==========================================

    client = XiaomiClient()

    response = await client.ask(pergunta)

    texto = ""

    # ==========================================
    # LIST RESPONSE
    # ==========================================

    if isinstance(response, list):

        for item in response:

            data = (
                item.get("data")
                if isinstance(item, dict)
                else None
            )

            if isinstance(data, dict):

                texto += (
                    data.get("content", "")
                    or data.get("message", "")
                    or ""
                )

            elif isinstance(data, str):

                texto += data

    # ==========================================
    # DICT RESPONSE
    # ==========================================

    elif isinstance(response, dict):

        texto = (
            response.get("response")
            or response.get("message")
            or ""
        )

        if not texto:

            data = response.get("data")

            if isinstance(data, dict):

                texto = (
                    data.get("content", "")
                    or data.get("message", "")
                    or ""
                )

    # ==========================================
    # STRING RESPONSE
    # ==========================================

    else:

        texto = str(response)

    # ==========================================
    # CLEAN RESPONSE
    # ==========================================

    texto = _clean_response_text(texto)

    # ==========================================
    # RETURN
    # ==========================================

    return {
        "response": texto
    }
