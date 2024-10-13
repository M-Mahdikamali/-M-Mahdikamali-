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
repos_url = f"https://api.github.com/users/{USERNAME}/repos"
repos_response = requests.get(repos_url, headers=headers)

# بررسی اینکه آیا درخواست موفق بوده است یا خیر
if repos_response.status_code == 200:
    repos = repos_response.json()
else:
    print(f"Failed to fetch repos: {repos_response.status_code} - {repos_response.text}")
    repos = []

# متغیری برای نگهداری اطلاعات زبان‌ها
languages_total = {}

# دریافت اطلاعات زبان‌های هر ریپوزیتوری
for repo in repos:
    if isinstance(repo, dict) and "languages_url" in repo:
        languages_url = repo["languages_url"]
        
        # دریافت زبان‌های هر ریپوزیتوری
        languages_response = requests.get(languages_url, headers=headers)
        if languages_response.status_code == 200:
            languages = languages_response.json()
            
            # جمع‌آوری کل بایت‌های زبان‌ها
            for language, bytes_used in languages.items():
                if language in languages_total:
                    languages_total[language] += bytes_used
                else:
                    languages_total[language] = bytes_used
        else:
            print(f"Failed to fetch languages for {repo['name']}: {languages_response.status_code} - {languages_response.text}")
    else:
        print(f"Unexpected format for repo: {repo}")

# محاسبه مجموع کل بایت‌ها برای محاسبه درصد
total_bytes = sum(languages_total.values())

if total_bytes == 0:
    print("No languages found in the repositories.")
    exit(1)

# ساختن محتوای جدید برای زبان‌ها
new_content = "\n\n### Languages ​​used in my repositories\n\n"
new_content += "| Programming language | Usage percentage |\n"
new_content += "|-------------------|---------------|\n"

for language, bytes_used in languages_total.items():
    percentage = (bytes_used / total_bytes) * 100
    new_content += f"| {language} | {percentage:.2f}% |\n"

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
pattern = re.compile(f"{start_marker}.*?{end_marker}", re.DOTALL)

# محتوای جدید با بلوک جدید
new_block = f"{start_marker}\n{new_content}\n{end_marker}"

# جایگزین کردن بلوک قدیمی با بلوک جدید
if pattern.search(current_content):
    updated_content = pattern.sub(new_block, current_content)
else:
    # اگر نشانه‌ها پیدا نشدند، بلوک را به انتهای فایل اضافه می‌کنیم
    updated_content = current_content + "\n" + new_block

# نوشتن محتوای جدید در فایل README.md
try:
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(updated_content)
    print("README.md updated successfully.")
except Exception as e:
    print(f"Failed to update README.md: {e}")
