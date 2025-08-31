#!/bin/bash
#
# نسخه‌ای از complement را دریافت می‌کند که بهترین تطابق را با ساخت فعلی دارد.
#
# The tarball is unpacked into `./complement`.
#این اسکریپت شِل (bash) وظیفه دانلود و استخراج یک نسخه خاص از پروژه Complement (یک ابزار تست برای سرورهای Matrix): 
 # را دارد، به گونه‌ای که با شاخه یا نسخه فعلی پروژه شما تطابق داشته باشد. در ادامه توضیح خط به خط و کارکرد کلی آن آمده است
 #این اسکریپت یک نسخه مناسب از Complement را از گیت‌هاب دانلود می‌کند و آن را در پوشهٔ ./complement استخراج می‌کند. 
 #انتخاب نسخه بر اساس شاخه فعلی گیت‌هاب (در محیط CI/CD مثل GitHub Actions) انجام می‌شود.

set -e
#    اگر هر دستوری در اسکریپت با خطا مواجه شود، اجرای اسکریپت متوقف می‌شود (fail-fast). 

mkdir -p complement
#    پوشه complement را ایجاد می‌کند (اگر وجود نداشته باشد). 
     

for BRANCH_NAME in "$GITHUB_HEAD_REF" "$GITHUB_BASE_REF" "${GITHUB_REF#refs/heads/}" "HEAD"; do
  # Skip empty branch names and merge commits.
  if [[ -z "$BRANCH_NAME" || $BRANCH_NAME =~ ^refs/pull/.* ]]; then
    continue
  fi

  (wget -O - "https://github.com/matrix-org/complement/archive/$BRANCH_NAME.tar.gz" | tar -xz --strip-components=1 -C complement) && break
done
