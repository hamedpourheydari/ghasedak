#!/usr/bin/env python


import json
import os


def set_output(key: str, value: str):

    with open(os.environ["GITHUB_OUTPUT"], "at") as f:
        print(f"{key}={value}", file=f)


IS_PR = os.environ["GITHUB_REF"].startswith("refs/pull/")

# ابتدا وظایف آزمایشی مختلف را محاسبه کنید
#برای درخواست‌های ادغام (PRs)، ما هر نوع آزمون را فقط با قدیمی‌ترین نسخهٔ پایتون که پشتیبانی می‌شود اجرا می‌کنیم (که در حال حاضر پایتون 3.9 است).

trial_sqlite_tests = [
    {
        "python-version": "3.9",
        "database": "sqlite",
        "extras": "all",
    }
]

if not IS_PR:
    trial_sqlite_tests.extend(
        {
            "python-version": version,
            "database": "sqlite",
            "extras": "all",
        }
        for version in ("3.10", "3.11", "3.12", "3.13")
    )

trial_postgres_tests = [
    {
        "python-version": "3.9",
        "database": "postgres",
        "postgres-version": "13",
        "extras": "all",
    }
]

if not IS_PR:
    trial_postgres_tests.append(
        {
            "python-version": "3.13",
            "database": "postgres",
            "postgres-version": "17",
            "extras": "all",
        }
    )

trial_no_extra_tests = [
    {
        "python-version": "3.9",
        "database": "sqlite",
        "extras": "",
    }
]

print("::group::Calculated trial jobs")
print(
    json.dumps(
        trial_sqlite_tests + trial_postgres_tests + trial_no_extra_tests, indent=4
    )
)
print("::endgroup::")

test_matrix = json.dumps(
    trial_sqlite_tests + trial_postgres_tests + trial_no_extra_tests
)
set_output("trial_test_matrix", test_matrix)


 # ابتدا وظایف مختلف sytest را محاسبه کنید.
#
# برای هر نوع آزمون، فقط در صورت ادغام (PRs) روی bullseye اجرا می‌شود.


sytest_tests = [
    {
        "sytest-tag": "bullseye",
    },
    {
        "sytest-tag": "bullseye",
        "postgres": "postgres",
    },
    {
        "sytest-tag": "bullseye",
        "postgres": "multi-postgres",
        "workers": "workers",
    },
    {
        "sytest-tag": "bullseye",
        "postgres": "multi-postgres",
        "workers": "workers",
        "reactor": "asyncio",
    },
]

if not IS_PR:
    sytest_tests.extend(
        [
            {
                "sytest-tag": "bullseye",
                "reactor": "asyncio",
            },
            {
                "sytest-tag": "bullseye",
                "postgres": "postgres",
                "reactor": "asyncio",
            },
            {
                "sytest-tag": "testing",
                "postgres": "postgres",
            },
        ]
    )


print("::group::Calculated sytest jobs")
print(json.dumps(sytest_tests, indent=4))
print("::endgroup::")

test_matrix = json.dumps(sytest_tests)
set_output("sytest_test_matrix", test_matrix)
