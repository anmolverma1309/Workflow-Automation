import os
import random
import subprocess
from datetime import datetime, timedelta, timezone


QUOTES = [
    "Small steps every day lead to big results.",
    "Discipline is choosing what you want most over what you want now.",
    "Progress, not perfection.",
    "Consistency turns effort into achievement.",
    "Focus on the process and the results will follow.",
    "Great things are built one commit at a time.",
    "Momentum is created by showing up daily.",
    "Keep going. You are closer than you think.",
    "Work quietly and let the results make noise.",
    "Done today is better than perfect someday.",
]


def run(cmd, env=None):
    subprocess.run(cmd, check=True, env=env)


def main():
    min_commits = int(os.environ.get("MIN_COMMITS", "1"))
    max_commits = int(os.environ.get("MAX_COMMITS", "3"))
    max_commits = max(1, min(20, max_commits))
    min_commits = max(1, min(min_commits, max_commits))

    ist = timezone(timedelta(hours=5, minutes=30))
    today = datetime.now(ist).date()

    count = random.randint(min_commits, max_commits)
    hours = random.sample(range(8, 21), k=min(count, 13))
    minutes = [random.randint(0, 59) for _ in range(count)]
    times = []
    for i in range(count):
        hour = hours[i % len(hours)]
        times.append(datetime(today.year, today.month, today.day, hour, minutes[i], tzinfo=ist))
    times.sort()

    readme_path = os.path.join(os.getcwd(), "README.md")
    for dt in times:
        quote = random.choice(QUOTES)
        message = f"Quote update: {quote[:50]}"
        readme_line = f"{dt.strftime('%Y-%m-%d %H:%M')} - \"{quote}\""
        with open(readme_path, "a", encoding="utf-8") as handle:
            handle.write(readme_line + "\n")
        run(["git", "add", "README.md"])
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = dt.isoformat()
        env["GIT_COMMITTER_DATE"] = dt.isoformat()
        run(["git", "commit", "-m", message], env=env)


if __name__ == "__main__":
    main()
