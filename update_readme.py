import requests
import os

# دریافت توکن از متغیر محیطی
GITHUB_TOKEN = os.getenv('GH_PAT')
USERNAME = "M-Mahdikamali"  # نام کاربری گیت‌هاب شما

# هدرها برای احراز هویت
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# دریافت لیست ریپوزیتوری‌های کاربر
repos_url = f"https://api.github.com/users/M-Mahdikamali/repos"
repos_response = requests.get(repos_url, headers=headers)

# بررسی اینکه آیا درخواست موفق بوده است یا خیر
if repos_response.status_code == 200:
    repos = repos_response.json()
else:
    print(f"Failed to fetch repos: {repos_response.status_code}")
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
            print(f"Failed to fetch languages for {repo['name']}: {languages_response.status_code}")
    else:
        print(f"Unexpected format for repo: {repo}")

# محاسبه مجموع کل بایت‌ها برای محاسبه درصد
total_bytes = sum(languages_total.values())

# ساختن متن برای README
readme_content = "### زبان‌های استفاده‌شده در ریپوزیتوری‌های من\n\n"
readme_content += "| زبان برنامه‌نویسی | درصد استفاده |\n"
readme_content += "|-------------------|---------------|\n"

for language, bytes_used in languages_total.items():
    percentage = (bytes_used / total_bytes) * 100
    readme_content += f"| {language} | {percentage:.2f}% |\n"

# به‌روزرسانی فایل README.md
with open("README.md", "w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)
