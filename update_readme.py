import requests
import os

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

# ساختن متن جدید برای اضافه‌کردن به README
new_content = "### Languages ​​used in my repositories\n"
new_content += "| programming language | usage percentage |\n"
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

# اضافه کردن محتوای جدید به محتوای قبلی
final_content = current_content + new_content

# به‌روزرسانی فایل README.md با محتوای جدید
try:
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(final_content)
    print("README.md updated successfully.")
except Exception as e:
    print(f"Failed to update README.md: {e}")
