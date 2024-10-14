import requests
import os
import re

# دریافت توکن از متغیر محیطی
GITHUB_TOKEN = os.getenv('GH_PAT')
USERNAME = "M-Mahdikamali"  # نام کاربری گیت‌هاب شما

# بررسی اینکه آیا توکن به درستی تنظیم شده است
if GITHUB_TOKEN is None:
    print("GITHUB_TOKEN is not set. Please check your environment variables.")
    exit(1)

# هدرها برای احراز هویت
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# دریافت لیست ریپوزیتوری‌های کاربر
repos_url = f"https://api.github.com/user/repos?visibility=all"
repos_response = requests.get(repos_url, headers=headers)

# بررسی وضعیت و محتوای پاسخ API
print(repos_response.status_code)  # وضعیت پاسخ
print(repos_response.json())       # محتوای پاسخ

# بررسی اینکه آیا درخواست موفق بوده است یا خیر
if repos_response.status_code == 200:
    repos = repos_response.json()
else:
    print(f"Failed to fetch repos: {repos_response.status_code} - {repos_response.text}")
    repos = []

# متغیری برای نگهداری تعداد پروژه‌ها به ازای هر زبان
languages_count = {}

# دریافت اطلاعات زبان‌های هر ریپوزیتوری
for repo in repos:
    if isinstance(repo, dict) and "languages_url" in repo:
        languages_url = repo["languages_url"]
        
        # دریافت زبان‌های هر ریپوزیتوری
        languages_response = requests.get(languages_url, headers=headers)
        if languages_response.status_code == 200:
            languages = languages_response.json()
            
            # اطمینان از اینکه هر زبان یک بار شمارش شود
            for language in languages.keys():
                languages_count[language] = languages_count.get(language, 0) + 1
        else:
            print(f"Failed to fetch languages for {repo['name']}: {languages_response.status_code} - {languages_response.text}")
    else:
        print(f"Unexpected format for repo: {repo}")


# محاسبه مجموع کل پروژه‌ها
total_projects = sum(languages_count.values())
print(languages_count)
if total_projects == 0:
    print("No languages found in the repositories.")
    exit(1)

# ساختن محتوای جدید برای زبان‌ها و وسط‌چین کردن جدول
new_content = """
<div align="center">

### Languages ​​used in my repositories

| Programming language | Usage percentage |
|-------------------|---------------|
"""
# محاسبه درصد تعداد پروژه‌ها برای هر زبان با سه رقم اعشار و گرد کردن به نزدیکترین مقدار
for language, count in languages_count.items():
    percentage = round((count / total_projects) * 100, 2)  # گرد کردن به دو رقم اعشار
    new_content += f"| {language} | {percentage:.2f}% |\n"  # نمایش با دو رقم اعشار

new_content += "</div>\n"

# خواندن محتوای فعلی فایل README.md
try:
    with open("README.md", "r", encoding="utf-8") as readme_file:
        current_content = readme_file.read()
except FileNotFoundError:
    current_content = ""

# جایگزین کردن محتوای جدید بین نشانه‌های مشخص‌شده
start_marker = "<!-- LANGUAGES_SECTION_START -->"
end_marker = "<!-- LANGUAGES_SECTION_END -->"

# الگوی regex برای پیدا کردن بلوک بین نشانه‌ها
pattern = re.compile(f"{start_marker}(.*?){end_marker}", re.DOTALL)

# پیدا کردن محتوای فعلی بین بلوک‌ها
match = pattern.search(current_content)
if match:
    current_block_content = match.group(1).strip()
else:
    current_block_content = ""

# اگر بلوک خالی است یا تغییر کرده، محتوای جدید را جایگزین می‌کنیم
if not current_block_content:
    print("Block is empty, adding new content.")
    updated_content = pattern.sub(f"{start_marker}\n{new_content}\n{end_marker}", current_content)
elif current_block_content == new_content.strip():
    print("Content is already up-to-date, no changes needed.")
else:
    print("Content has changed, updating block.")
    updated_content = pattern.sub(f"{start_marker}\n{new_content}\n{end_marker}", current_content)

# نوشتن محتوای جدید در فایل README.md
try:
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(updated_content)
    print("README.md updated successfully.")
    
    # اضافه کردن کد برای چاپ محتوای نهایی فایل README.md
    print("Updated README.md content:\n")
    print(updated_content)  # چاپ محتوای نهایی برای بررسی
    
except Exception as e:
    print(f"Failed to update README.md: {e}")

