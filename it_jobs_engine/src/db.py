import sqlite3
from config.settings import DB_PATH
from src.utils.logger import logger
from src.models import Job

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_hash TEXT UNIQUE,
            title TEXT,
            company TEXT,
            location TEXT,
            experience_level TEXT,
            role_category TEXT,
            apply_url TEXT,
            source_name TEXT,
            fetched_at TIMESTAMP,
            is_published BOOLEAN DEFAULT 0,
            telegram_status TEXT DEFAULT NULL,
            blog_status TEXT DEFAULT NULL,
            linkedin_status TEXT DEFAULT NULL
        );
        """
        try:
            with self._get_connection() as conn:
                conn.execute(query)
                logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def save_job(self, job: Job) -> bool:
        """
        Saves a job if it doesn't already exist.
        Returns True if saved, False if duplicate.
        """
        if not job.job_hash:
            job.generate_hash()
            
        query = """
        INSERT INTO jobs (
            job_hash, title, company, location, experience_level, 
            role_category, apply_url, source_name, fetched_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self._get_connection() as conn:
                conn.execute(query, (
                    job.job_hash, job.title, job.company, job.location,
                    job.experience_level, job.role_category, job.apply_url,
                    job.source_name, job.fetched_at
                ))
            logger.info(f"Saved new job: {job.title} at {job.company}")
            return True
        except sqlite3.IntegrityError:
            # Duplicate job hash
            return False
        except Exception as e:
            logger.error(f"Error saving job: {e}")
            return False
            
    def get_pending_jobs(self):
        """Fetch jobs that haven't been published yet."""
        query = "SELECT * FROM jobs WHERE is_published = 0"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            # Convert rows to dict or objects if needed, for MVP returning raw rows is fine or simple dicts
            return rows

    def mark_published(self, job_hash, telegram_status=None, blog_status=None):
        query = """
        UPDATE jobs 
        SET is_published = 1, telegram_status = ?, blog_status = ? 
        WHERE job_hash = ?
        """
        try:
            with self._get_connection() as conn:
                conn.execute(query, (telegram_status, blog_status, job_hash))
            logger.info(f"Marked job {job_hash} as published.")
        except Exception as e:
            logger.error(f"Failed to update publish status for {job_hash}: {e}")
