from src.fetchers.python_org import PythonOrgFetcher
from src.db import DatabaseManager

def test_fetch():
    print("Testing PythonOrgFetcher...")
    fetcher = PythonOrgFetcher()
    jobs = fetcher.fetch_jobs()
    
    print(f"Found {len(jobs)} jobs.")
    if jobs:
        print(f"First job: {jobs[0]}")
    
    print("Saving to DB...")
    db = DatabaseManager()
    saved_count = 0
    for job in jobs:
        if db.save_job(job):
            saved_count += 1
            
    print(f"Saved {saved_count} new jobs to DB.")

if __name__ == "__main__":
    test_fetch()
