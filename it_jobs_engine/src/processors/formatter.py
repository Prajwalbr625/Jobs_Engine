from src.models import Job

class ContentFormatter:
    
    @staticmethod
    def format_telegram(job: Job) -> str:
        """
        Formats a job for Telegram with HTML.
        """
        # Telegram supports basic HTML tags: b, i, a, code, pre
        icon = "\U0001F4BC" # Briefcase
        exp_icon = "\U0001F393" # Graduation cap for fresher, maybe something else for exp
        if job.experience_level == "Fresher":
            exp_icon = "\U0001F331" # Seedling
        elif job.experience_level == "Experienced":
            exp_icon = "\U0001F9D1\u200D\U0001F4BB" # Technologist
            
        role_hashtags = f"#{job.role_category.replace(' ', '')} #ITJobs"
        
        msg = (
            f"{icon} <b>{job.title}</b>\n"
            f"<b>Company:</b> {job.company}\n"
            f"<b>Location:</b> {job.location}\n"
            f"{exp_icon} <b>Experience:</b> {job.experience_level}\n\n"
            f"\U0001F517 <a href='{job.apply_url}'><b>APPLY NOW</b></a>\n\n"
            f"{role_hashtags} #{job.source_name.replace('.', '')}"
        )
        return msg

    @staticmethod
    def format_blog(job: Job) -> dict:
        """
        Formats a job for a Blog Post. Returns dict with title and content.
        """
        title = f"{job.title} at {job.company} - {job.location} ({job.experience_level})"
        
        content = f"""
        <h2>Job Opportunity: {job.title}</h2>
        <p><strong>Company:</strong> {job.company}</p>
        <p><strong>Location:</strong> {job.location}</p>
        <p><strong>Experience Level:</strong> {job.experience_level}</p>
        <p><strong>Category:</strong> {job.role_category}</p>
        
        <h3>Job Description</h3>
        <p>A new opportunity has been posted by {job.company}. Click the link below to view full details and apply.</p>
        
        <p><a href="{job.apply_url}" target="_blank" rel="noopener"><strong>Apply Here</strong></a></p>
        
        <hr>
        <p><em>Disclaimer: This job was automatically aggregated from {job.source_name}. verification is recommended.</em></p>
        """
        
        return {
            "title": title,
            "content": content,
            "tags": [job.role_category, job.experience_level, "IT Jobs"]
        }

    @staticmethod
    def format_linkedin(job: Job) -> str:
        """
        Formats a job for LinkedIn.
        """
        msg = (
            f"\U0001F680 New Job Alert: {job.title} at {job.company}!\n\n"
            f"\U0001F4CD Location: {job.location}\n"
            f"\U0001F4BC Experience: {job.experience_level}\n"
            f"\U0001F4BB Role: {job.role_category}\n\n"
            f"Apply here: {job.apply_url}\n\n"
            "#Hiring #Jobs #TechJobs #Career #Opportunity"
        )
        return msg
