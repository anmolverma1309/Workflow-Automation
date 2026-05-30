import os
import random
import subprocess
from datetime import datetime, timedelta, timezone


def run(cmd, env=None):
    subprocess.run(cmd, check=True, env=env)


def main():
    min_commits = int(os.environ.get("MIN_COMMITS", "4"))
    max_commits = int(os.environ.get("MAX_COMMITS", "10"))
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
        message = dt.strftime("Contribution: %Y-%m-%d %H:%M")
        with open(readme_path, "a", encoding="utf-8") as handle:
            handle.write(message + "\n\n")
        run(["git", "add", "README.md"])
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = dt.isoformat()
        env["GIT_COMMITTER_DATE"] = dt.isoformat()
        run(["git", "commit", "-m", message], env=env)


if __name__ == "__main__":
    main()
