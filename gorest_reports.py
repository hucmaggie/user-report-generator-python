import requests
import sys
from collections import Counter

BASE_URL = "https://gorest.co.in/public/v2/users"
PER_PAGE = 100

def fetch_all_users():
    """Page through the GoRest API until no more users are returned."""
    users = []
    page = 1
    while True:
        resp = requests.get(BASE_URL, params={"page": page, "per_page": PER_PAGE})
        resp.raise_for_status()
        page_users = resp.json()
        if not page_users:
            break
        users.extend(page_users)
        page += 1
    return users

def q1_active_test(users):
    """Q1: Print active users with .test emails as CSV (id,email,name,gender)."""
    print("id,email,name,gender")
    for u in users:
        status = u.get("status", "").lower()
        email  = u.get("email", "").lower()
        if status == "active" and email.endswith(".test"):
            # sanitize name to avoid embedded commas/newlines
            name   = u.get("name", "").replace("\n", " ").replace(",", " ")
            gender = u.get("gender", "")
            print(f'{u["id"]},{u["email"]},{name},{gender}')

def q2_suffix_counts(users):
    """Q2: Count email domain suffixes and print CSV (suffix,count)."""
    counter = Counter()
    for u in users:
        email = u.get("email", "").lower()
        if "@" not in email or "." not in email.split("@",1)[1]:
            continue
        suffix = email.rsplit(".", 1)[1]
        counter[suffix] += 1

    print("Domain,count")
    for suffix, count in counter.items():
        print(f"{suffix},{count}")

def main():
    users = fetch_all_users()
    # Q1
    print("=== Question 1 ===", file=sys.stderr)
    q1_active_test(users)
    print("\n=== Question 2 ===", file=sys.stderr)
    q2_suffix_counts(users)

if __name__ == "__main__":
    main()