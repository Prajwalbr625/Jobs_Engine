import time
import schedule
import argparse
from src.utils.logger import logger
from src.db import DatabaseManager
from src.fetchers.python_org import PythonOrgFetcher
from src.fetchers.linkedin import LinkedInFetcher
from src.fetchers.naukri import NaukriFetcher
from src.processors.filters import LocationFilter
from src.processors.formatter import ContentFormatter
from src.publishers.telegram import TelegramPublisher
from src.publishers.blog import BlogPublisher
from src.publishers.linkedin import LinkedInPublisher
from config.settings import FETCH_INTERVAL_MINUTES

def run_cycle():
    logger.info("Starting job fetch cycle...")
    
    # 1. Initialize DB
    db = DatabaseManager()
    
    # 2. Fetch Jobs
    fetchers = [
        # PythonOrgFetcher(), # Can comment out to speed up or focus on specific source
        LinkedInFetcher(),
        # NaukriFetcher()
    ]
    new_jobs_count = 0
    
    for fetcher in fetchers:
        jobs = fetcher.fetch_jobs()
        for job in jobs:
            # Apply Location Filter
            if not LocationFilter.is_allowed(job.location):
                continue
                
            if db.save_job(job):
                new_jobs_count += 1
    
    if new_jobs_count == 0:
        logger.info("No new jobs found this cycle, but checking for pending jobs...")
        # return  <-- Removed to allow processing pending jobs

    # 3. Process Pending Jobs
    pending_jobs = db.get_pending_jobs()
    logger.info(f"Processing {len(pending_jobs)} pending jobs...")
    
    # Initialize Publishers
    telegram = TelegramPublisher()
    blog = BlogPublisher()
    linkedin = LinkedInPublisher()
    
    # Note: pending_jobs returns tuples from sqlite.
    # We should ideally fetch them as objects or dicts. 
    # For MVP, let's just re-fetch or assume index positions.
    # Schema: id, job_hash, title, company, location, experience_level, 
    #         role_category, apply_url, source_name, fetched_at, is_published, ...
    
    # To fix this, let's update db.py to return dicts or objects, 
    # OR map manually here. 
    # Let's simple query again or just use row indexing.
    # Indices: 0-id, 1-hash, 2-title, 3-company, 4-location, 5-exp, 6-role, 7-url, 8-source
    
    for row in pending_jobs:
        job_hash = row[1]
        
        # Reconstruct Job object loosely for formatters
        # Ideally we load back into Job model
        from src.models import Job
        job = Job(
            title=row[2],
            company=row[3],
            location=row[4],
            experience_level=row[5],
            role_category=row[6],
            apply_url=row[7],
            source_name=row[8],
            job_hash=job_hash
        )
        
        # Publish
        tele_msg = ContentFormatter.format_telegram(job)
        tele_status = "SUCCESS" if telegram.publish(tele_msg) else "SKIPPED/FAILED"
        
        blog_data = ContentFormatter.format_blog(job)
        blog_status = "SUCCESS" if blog.publish(blog_data["title"], blog_data["content"], blog_data["tags"]) else "SKIPPED/FAILED"
        
        li_msg = ContentFormatter.format_linkedin(job)
        li_status = "SUCCESS" if linkedin.publish(li_msg) else "SKIPPED/FAILED"
        
        # Mark as published
        db.mark_published(job_hash, tele_status, blog_status)

        if new_jobs_count > 0:
            logger.info("New jobs found, triggering static site build...")
            from src.processors.static_generator import StaticSiteGenerator
            generator = StaticSiteGenerator()
            generator.build()
            
    logger.info("Cycle completed.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    args = parser.parse_args()

    if args.once:
        run_cycle()
    else:
        logger.info(f"Scheduler started. Running every {FETCH_INTERVAL_MINUTES} minutes.")
        schedule.every(FETCH_INTERVAL_MINUTES).minutes.do(run_cycle)
        
        # Run immediately on start
        run_cycle()
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()
