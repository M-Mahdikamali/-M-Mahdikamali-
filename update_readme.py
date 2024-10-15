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
<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/><br>
  <img src="https://komarev.com/ghpvc/?username=M-Mahdikamali&style=flat-square&color=blue" alt=""/>
</div>

### :hammer_and_wrench: Languages and Tools :
<div>
  <img src="https://github.com/devicons/devicon/blob/master/icons/java/java-original-wordmark.svg" title="Java" alt="Java" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/jupyter/jupyter-original-wordmark.svg" title="Material UI" alt="Material UI" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/numpy/numpy-plain.svg" title="Numpy" alt="Spring" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/nextjs/nextjs-original.svg" title="NextJs" alt="React" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/android/android-plain-wordmark.svg" title="Android" alt="Flutter" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pandas/pandas-original.svg" title="Pandas" alt="Redux " width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/pycharm/pycharm-original.svg"  title="Pycharm" alt="CSS" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/intellij/intellij-original.svg" title="Intellij" alt="HTML" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/javascript/javascript-original.svg" title="JavaScript" alt="JavaScript" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/firebase/firebase-plain-wordmark.svg" title="Firebase" alt="Firebase" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/xcode/xcode-original.svg" title="Xcode"  alt="Gatsby" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" title="MySQL"  alt="MySQL" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/apple/apple-original.svg" title="IOS" alt="NodeJS" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/ubuntu/ubuntu-original.svg" title="Ubuntu" alt="AWS" width="40" height="40"/>&nbsp;
  <img src="https://github.com/devicons/devicon/blob/master/icons/git/git-original-wordmark.svg" title="Git" **alt="Git" width="40" height="40"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/cplusplus/cplusplus-plain.svg" title="C++" **alt="Git" width="40" height="40"/>
</div>

---

### :fire: My Stats :
<div align="center">
  <a href="https://git.io/streak-stats">
    <img src="https://streak-stats.demolab.com?user=M-Mahdikamali&theme=radical&border_radius=22&mode=weekly" alt="GitHub Streak">
  </a>
  <br>
  <br>
  <br>
</div>
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

try:
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(new_content)
    print("README.md updated successfully.")
    
    # اضافه کردن کد برای چاپ محتوای نهایی فایل README.md
    print("Updated README.md content:\n")
    print(new_content)  # چاپ محتوای نهایی برای بررسی

except Exception as e:
    print(f"Failed to update README.md: {e}")
