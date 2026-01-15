import os
import shutil
from jinja2 import Environment, FileSystemLoader, Template
from src.utils.logger import logger
from src.models import Job
from src.processors.formatter import ContentFormatter
from src.db import DatabaseManager
from datetime import datetime

class StaticSiteGenerator:
    def __init__(self, output_dir="docs"):
        self.output_dir = output_dir
        self.db = DatabaseManager()
        
    def build(self):
        logger.info("Starting Static Site Build...")
        
        # 1. Clean/Create Output Dir
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        # 2. Fetch Jobs
        rows = self.db._get_connection().execute("SELECT * FROM jobs ORDER BY fetched_at DESC").fetchall()
        jobs = []
        for row in rows:
            jobs.append(Job(
                title=row[2],
                company=row[3],
                location=row[4],
                experience_level=row[5],
                role_category=row[6],
                apply_url=row[7],
                source_name=row[8],
                fetched_at=row[9],
                job_hash=row[1]
            ))
            
        # 3. Generate Index Page
        self._generate_index(jobs)
        
        # 4. Generate Job Detail Pages
        for job in jobs:
            self._generate_job_page(job)
            
        # 5. Copy Assets (if any) - None for now as CSS is inline
        
        logger.info(f"Static Site Build Complete. Generated {len(jobs)} pages in '{self.output_dir}/'")

    def _get_layout(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="Find the best IT jobs: {{ title }}">
    <style>
        :root { --primary: #2563eb; --text-main: #1f2937; --text-muted: #6b7280; --bg: #f9fafb; --card-bg: #ffffff; }
        body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text-main); line-height: 1.6; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        header { margin-bottom: 40px; border-bottom: 2px solid #e5e7eb; padding-bottom: 20px; }
        h1 { font-size: 2.25rem; font-weight: 800; color: #111827; margin: 0; }
        .subtitle { color: var(--text-muted); font-size: 1.1rem; }
        .card { background: var(--card-bg); border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); padding: 24px; margin-bottom: 20px; transition: transform 0.2s; }
        .card:hover { transform: translateY(-2px); }
        .card h2 { margin-top: 0; color: var(--primary); }
        .card-meta { display: flex; gap: 15px; color: var(--text-muted); font-size: 0.9rem; margin-bottom: 15px; }
        .tag { background: #dbeafe; color: #1e40af; padding: 2px 10px; border-radius: 9999px; font-weight: 500; font-size: 0.8rem; }
        a.read-more, .btn { display: inline-block; padding: 8px 16px; background: var(--primary); color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 0.9rem; }
        .back-link { display: inline-block; margin-bottom: 20px; color: var(--text-muted); text-decoration: none; }
        .ad-slot { background: #eee; padding: 20px; text-align: center; margin: 20px 0; border: 1px dashed #ccc; color: #666; }
        .filters { margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; }
        .filter-btn { padding: 5px 10px; background: #e5e7eb; color: #374151; text-decoration: none; border-radius: 5px; font-size: 0.85rem; }
        .filter-btn:hover { background: #d1d5db; }
    </style>
    <!-- GLOBAL ADSENSE CODE HERE -->
    <!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script> -->
</head>
<body>
    <div class="container">
        {{ content }}
        
        <footer style="margin-top: 50px; text-align: center; color: #9ca3af; font-size: 0.8rem;">
            <p>&copy; 2026 IT Jobs Alert Engine. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
"""

    def _generate_index(self, jobs):
        # In a static site, true filtering (search) usually requires client-side JS or generating separate pages per category.
        # For MVP, we generate one main index with all jobs (Client-side JS could act filtering).
        
        job_html_list = ""
        for job in jobs[:50]: # Limit to 50 recent on homepage to keep build fast
            job_html_list += f"""
            <div class="card">
                <div class="card-meta">
                    <span>{str(job.fetched_at)[:10]}</span>
                    <span class="tag">{job.role_category}</span>
                    <span class="tag">{job.experience_level}</span>
                </div>
                <h2><a href="job_{job.job_hash}.html" style="text-decoration: none; color: inherit;">{job.title}</a></h2>
                <p><strong>{job.company}</strong> &bull; {job.location}</p>
                <a href="job_{job.job_hash}.html" class="read-more">View Details</a>
            </div>
            """
            
        content = f"""
        <header>
            <h1>IT Jobs Alert Engine</h1>
            <p class="subtitle">Curated Tech Opportunities. Updated Hourly.</p>
        </header>
        
        <!-- AD SLOT HEADER -->
        <div class="ad-slot">
            <p>Advertisement Space (Header)</p>
        </div>
        
        <div class="filters">
            <span>Quick Filters (Coming Soon in V2):</span>
            <span class="filter-btn">Remote</span>
            <span class="filter-btn">Bangalore</span>
            <span class="filter-btn">Python</span>
        </div>
        
        <div class="job-list">
            {job_html_list}
        </div>
        """
        
        template = Template(self._get_layout())
        html = template.render(title="IT Jobs Alert Engine - Latest Jobs", content=content)
        
        with open(f"{self.output_dir}/index.html", "w") as f:
            f.write(html)

    def _generate_job_page(self, job):
        blog_data = ContentFormatter.format_blog(job)
        
        content = f"""
        <a href="index.html" class="back-link">&larr; Back to Jobs</a>
        
        <!-- AD SLOT IN-ARTICLE -->
        <div class="ad-slot">
            <p>Advertisement Space (Top of Job)</p>
        </div>
        
        <div class="card">
            <h1>{blog_data['title']}</h1>
            <div class="post-content">
                {blog_data['content']}
            </div>
        </div>
        
        <!-- AD SLOT BOTTOM -->
        <div class="ad-slot">
            <p>Advertisement Space (Bottom)</p>
        </div>
        """
        
        template = Template(self._get_layout())
        html = template.render(title=f"{job.title} at {job.company}", content=content)
        
        with open(f"{self.output_dir}/job_{job.job_hash}.html", "w") as f:
            f.write(html)
