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


# ===== TODO(學生)：設計你的 Prompt（可含 system + user）=====
email_raw = (
    "嘿老闆，明天10點的會議我可能會遲到一下，大概15分鐘吧，"
    "昨晚小孩發燒，早上得先送他去看醫生。會議的資料我都準備好了，"
    "可以先請小王開始報告嗎？"
)

system_email = """
你是一位專業的商務寫手，負責將口語訊息改寫為正式且清楚的商業郵件。
風格：專業、精確、禮貌；包含主旨、稱謂、清楚說明、解決方案、專業結尾。
輸出格式：請以標題「主旨：...」開頭，其後為正式郵件內文。
""".strip()

# === 在此撰寫你的 user prompt，需明確描述格式要求與轉換目標 ===
user_email_prompt = f"""
【任務】將以下訊息改寫為正式商業郵件，並滿足：
1) 必含：主旨、稱謂、清楚說明、解決方案、專業結尾
2) 保持原意但提升專業度
3) 語氣禮貌、清楚、務實
【原始訊息】
{email_raw}
"""
 
# === 呼叫 LLM（或你自定義的規則程式）===
# TODO: 取消下一行註解，並完成 call_llm 的實作
email_formal = call_llm(user_email_prompt, system=system_email)

# 暫時：請同學自行將結果貼到此變數（若尚未串接 API），以便後續存檔。已經串接好openai的可以刪掉這行
'''
email_formal = """
#TODO：在這裡貼上你產生的正式商業郵件結果。
#""".strip()
'''

# 儲存輸出
save_text("outputs/task1_email_formal.txt", email_formal)
print("✅ 任務一完成（暫存）。輸出檔：outputs/task1_email_formal.txt")
    
