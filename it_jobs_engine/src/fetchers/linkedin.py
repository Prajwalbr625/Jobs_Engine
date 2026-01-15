import requests
from bs4 import BeautifulSoup
from src.fetchers.base import BaseFetcher
from src.models import Job
from src.processors.categorizer import JobCategorizer
from src.utils.logger import logger
import urllib.parse

class LinkedInFetcher(BaseFetcher):
    def __init__(self):
        # Public jobs search URL
        super().__init__("LinkedIn", "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%20Engineer&location=India&start=0")
        
    def fetch_jobs(self):
        jobs = []
        logger.info("Starting LinkedIn static fetch...")
        
        # LinkedIn strict about headers
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

        try:
            # Note: We use the 'seeMoreJobPostings' API endpoint which returns HTML fragments of job cards.
            # It's cleaner than the full search page.
            response = requests.get(self.base_url, headers=headers, timeout=10, verify=False)
            
            if response.status_code != 200:
                logger.warning(f"LinkedIn fetch failed with status {response.status_code}")
                return []
                
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("li")
            
            logger.info(f"Found {len(job_cards)} potential job cards on LinkedIn")
            
            for card in job_cards:
                try:
                    title_tag = card.find("h3", class_="base-search-card__title")
                    company_tag = card.find("h4", class_="base-search-card__subtitle")
                    location_tag = card.find("span", class_="job-search-card__location")
                    link_tag = card.find("a", class_="base-card__full-link")
                    
                    if not (title_tag and company_tag and link_tag):
                        continue
                        
                    title = title_tag.get_text(strip=True)
                    company = company_tag.get_text(strip=True)
                    location = location_tag.get_text(strip=True) if location_tag else "Remote"
                    apply_url = link_tag["href"]
                    
                    # Clean URL
                    if "?" in apply_url:
                        apply_url = apply_url.split("?")[0]
                        
                    role, experience = JobCategorizer.categorize(title)
                    
                    job = Job(
                        title=title,
                        company=company,
                        location=location,
                        apply_url=apply_url,
                        source_name="LinkedIn",
                        role_category=role,
                        experience_level=experience
                    )
                    jobs.append(job)
                except Exception as e:
                    continue
                    
        except Exception as e:
            logger.error(f"Error fetching LinkedIn: {e}")
            
        logger.info(f"Fetched {len(jobs)} jobs from LinkedIn")
        return jobs
