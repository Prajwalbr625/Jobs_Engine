import urllib.parse
from bs4 import BeautifulSoup
from src.fetchers.base import BaseFetcher
from src.models import Job
from src.processors.categorizer import JobCategorizer
from src.utils.logger import logger

class PythonOrgFetcher(BaseFetcher):
    def __init__(self):
        super().__init__("Python.org", "https://www.python.org/jobs/")
        
    def fetch_jobs(self):
        jobs = []
        html = self.fetch_page(self.base_url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, "html.parser")
        job_list = soup.find("ol", class_="list-recent-jobs")
        
        if not job_list:
            logger.warning("Could not find job list on Python.org")
            return []
            
        for item in job_list.find_all("li"):
            try:
                title_tag = item.find("span", class_="listing-company-name").find("a")
                title = title_tag.text.strip()
                apply_path = title_tag["href"]
                # Use urllib.parse.urljoin to handle relative vs absolute paths correctly
                apply_url = urllib.parse.urljoin(self.base_url, apply_path)
                
                company_tag = item.text.strip().split("\n")
                # Python.org structure is a bit nested, let's parse carefully
                # Structure:
                # <span class="listing-company-name">
                #    <a href="...">Title</a><br/>
                #    Company Name
                # </span>
                # But looking at real python.org structure it might be slightly different. 
                # Let's adjust based on typical structure.
                # Actually, the 'listing-company-name' contains the title anchor and company text.
                
                company_text = item.find("span", class_="listing-company-name").get_text(strip=True)
                # company_text usually looks like "Job TitleCompany Name" if no space.
                # Let's try to extract company name by removing title.
                company = company_text.replace(title, "").strip()
                
                location = item.find("span", class_="listing-location").text.strip()
                
                # Categorize
                role, experience = JobCategorizer.categorize(title)
                
                job = Job(
                    title=title,
                    company=company,
                    location=location,
                    apply_url=apply_url,
                    source_name=self.source_name,
                    role_category=role,
                    experience_level=experience
                )
                jobs.append(job)
            except Exception as e:
                logger.error(f"Error parsing job item: {e}")
                continue
                
        logger.info(f"Fetched {len(jobs)} jobs from Python.org")
        return jobs
