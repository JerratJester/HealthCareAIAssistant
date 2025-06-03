from typing import Optional
from .preload import PRELOADED_QUESTIONS
from transformers import pipeline           # helper
from transformers import Pipeline                           # type hints
import json, pathlib
_FAQ = json.loads(
    open(pathlib.Path(__file__).parents[1] / "data/surgery_faqs.json").read()
)

# -------- module-level singleton ------------
_chat_pipeline: Optional[Pipeline] = None

SYSTEM_PROMPT = (
    "You are SISBot, an AI assistant for Surgical Information Systems. "
    "Answer peri-operative questions clearly and concisely.\n\n"
)

def init_chat_pipeline(model_name: str = "tiiuae/falcon-rw-1b"):
    global _chat_pipeline
    if _chat_pipeline is None:
        _chat_pipeline = pipeline(
            "text-generation",
            model=model_name,
            device_map="auto"
        )


def generate_response(prompt: str) -> str:
    global _chat_pipeline
    output = _chat_pipeline(
        prompt,
        max_new_tokens=100,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.2
    )
    return output[0]['generated_text']

def shutdown_pipeline() -> None:
    """
    Clean up the singleton pipeline and free GPU/CPU memory.
    """
    global _chat_pipeline
    if _chat_pipeline is not None:
        # Delete the model & tokenizer
        del _chat_pipeline
        _chat_pipeline = None
        # If using GPU, clear CUDA cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()