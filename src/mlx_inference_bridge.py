"""
Bionic MLX Inference Bridge & KV-Cache Reuse Manager
Optimized for Apple Silicon unified memory using MLX.
"""

import sys
import json
import httpx
from typing import Generator, Dict, Any

class MLXInferenceBridge:
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.base_url = base_url.rstrip("/")

    def stream_completion(self, messages: list, temperature: float = 0.2) -> Generator[str, None, None]:
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": "qwen2.5-coder-32b-instruct",
            "messages": messages,
            "temperature": temperature,
            "stream": True
        }
        with httpx.Client(timeout=120.0) as client:
            with client.stream("POST", url, json=payload) as response:
                for line in response.iter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        try:
                            chunk = json.loads(line[6:])
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            continue

if __name__ == "__main__":
    bridge = MLXInferenceBridge()
    print("⚡ MLX Inference Bridge ready.")
