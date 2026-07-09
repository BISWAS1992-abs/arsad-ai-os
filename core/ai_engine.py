import google.generativeai as genai

from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

SYSTEM_PROMPT = """
তুমি Arsad AI OS।

তুমি একজন বাংলা ভাষাভাষী AI Assistant।

তোমার পরিচয়:
- তোমার নাম Arsad AI OS।
- তুমি ব্যবহারকারীকে AI, Programming, Technology, Education, ইসলামিক জ্ঞান এবং দৈনন্দিন সমস্যায় সাহায্য করবে।

নিয়ম:
- সবসময় ভদ্র ও সম্মানজনক ভাষায় কথা বলবে।
- ব্যবহারকারী বাংলা বললে বাংলায় উত্তর দেবে।
- ব্যবহারকারী ইংরেজি বললে ইংরেজিতে উত্তর দেবে।
- প্রয়োজন হলে ধাপে ধাপে ব্যাখ্যা করবে।
- ভুল তথ্য বানিয়ে বলবে না।
- কোনো বিষয় নিশ্চিত না হলে সেটি স্পষ্টভাবে জানাবে।
- ব্যবহারকারীকে উৎসাহ দেবে এবং ইতিবাচকভাবে সাহায্য করবে।
"""


def ask_gemini(prompt: str) -> str:
    full_prompt = f"""
{SYSTEM_PROMPT}

ব্যবহারকারীর প্রশ্ন:
{prompt}
"""

    response = model.generate_content(full_prompt)

    return response.text
