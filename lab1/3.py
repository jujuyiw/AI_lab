# === 可選：安裝你要用的 SDK（Colab 環境）===
# 例如：
# !pip -q install openai

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any

# ========== 可重用：統一的 LLM 呼叫介面 ==========
@dataclass
class LLMConfig:
    provider: str = "openai"
    model: str = "gpt-4o-mini"     # TODO: 指定模型名稱（必填）
    api_key_env: str = "OPENAI_API_KEY"

def call_llm(prompt: str, system: Optional[str]=None, cfg: Optional[LLMConfig]=None, **kwargs) -> str:
    """
    統一的 LLM 呼叫函式（簡化版）。
    - 你可以在此實作實際的 SDK 呼叫；或在各任務中自行呼叫不同供應商的 API。
    - 若不想用雲端 API，可改為你自定義的規則程式碼（但需在報告中說明限制）。
    """
    cfg = cfg or LLMConfig()
    provider = cfg.provider.lower()
    os.environ["OPENAI_API_KEY"] = "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"  # TODO: 對應的 API Key 環境變數名

    # TODO: 依你選定的 provider 完成實作（下方示例為 OpenAI 的「佔位」程式碼片段）
    # ===== OpenAI （需: pip install openai）=====
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv(cfg.api_key_env))
        messages = []
        if system:
            messages.append({ "role": "system", "content": system })
        messages.append({ "role": "user", "content": prompt })
        resp = client.chat.completions.create(model=cfg.model, messages=messages, **kwargs)
        return resp.choices[0].message.content
        raise NotImplementedError("TODO: 請在 call_llm() 中實作 OpenAI呼叫。")
    else:
        raise NotImplementedError(f"TODO: 尚未支援 provider={provider!r}。")
    

# ========== 共用工具 ==========
def count_zh_chars(text: str) -> int:
    """簡易字數統計（中文為主，含中英文混排時可視需要自行調整）。"""
    return len(text.strip())

def save_text(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    

en_sentence = "I'm afraid I cannot attend tomorrow's meeting due to a scheduling conflict. Would it be possible to reschedule to next week?"

# ===== TODO(學生)：設計能同時完成「翻譯＋語氣調整」的 Prompt =====
system_trans = """
你是一位了解台灣語境的翻譯與口吻調整專家。
請將英文句子轉為「繁體中文」，語氣友善、輕鬆，但仍保留禮貌與清楚度。
若啟用進階挑戰，請產出 2–3 種不同語氣版本，並說明適用情境。
""".strip()

user_trans_prompt = f"""
將下列英文句子轉為繁體中文，語氣友善、輕鬆，並保留原意：
{en_sentence}

（進階）請額外給我 2–3 種不同口吻版本，並說明適用情境。
"""

# TODO: 使用 LLM 產生輸出
# trans_output = call_llm(user_trans_prompt, system=system_trans)

trans_output = """
【基礎版】TODO：友善、輕鬆版
【版本A】TODO：更口語
【版本B】TODO：較正式但溫和
（說明）TODO：各版本適用情境
""".strip()

save_text("outputs/task3_translation_tone.txt", trans_output)
print("✅ 任務三完成（暫存）。輸出檔：outputs/task3_translation_tone.txt")