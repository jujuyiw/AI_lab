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


article = (
    """根據最新研究顯示，台灣的科技產業正面臨人才短缺的嚴峻挑戰。調查發現，有超過70%的科技公司表示難以找到合適的AI和資料科學人才。這個問題的根源包括：教育體系與產業需求脫節、薪資競爭力不足，以及人才外流至海外市場。為了解決這個問題，政府推出了多項措施，包括增加大學相關科系名額、提供企業培訓補助，以及放寬外籍人才引進政策。然而，專家認為這些措施需要時間才能看到成效，短期內企業仍需要自行投資人才培育。"""
)

# ===== TODO(學生)：設計你的 CoT Prompt =====
system_cot = """
你是一位善於結構化分析的助教。請先輸出「分析步驟」，再輸出「最終摘要」。
格式：
[分析步驟]
1) 主題識別：...
2) 要點提取：...
3) 重要性排序：...
[最終摘要]（<= 50 字）
""".strip()

user_cot_prompt = f"""
閱讀以下文章，依指示先列出分析步驟，再產生 50 字以內的總結：
【文章】
{article}
"""

# TODO: 使用 LLM（或你自定義的規則程式）產生輸出
cot_output = call_llm(user_cot_prompt, system=system_cot)

cot_output = """
[分析步驟]
1) 主題識別：TODO
2) 要點提取：TODO
3) 重要性排序：TODO
[最終摘要]
TODO（<= 50 字）
""".strip()

# 50字內檢查（僅對「最終摘要」行做粗略偵測）
lines = [ln for ln in cot_output.splitlines() if ln.strip()]
final_lines = [ln for ln in lines if ln.strip().startswith("[最終摘要]") or ln.strip().startswith("最終摘要")]
if final_lines:
    final = final_lines[-1].replace("[最終摘要]", "").strip("：: ")
    n_chars = count_zh_chars(final)
    print(f"最終摘要字數：約 {n_chars} 字（目標 <= 50）")
else:
    print("⚠️ 未偵測到最終摘要段落，請檢查輸出格式。")

save_text("outputs/task2_summary_cot.txt", cot_output)
print("✅ 任務二完成（暫存）。輸出檔：outputs/task2_summary_cot.txt")