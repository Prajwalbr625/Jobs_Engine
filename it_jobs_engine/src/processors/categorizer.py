import re

class JobCategorizer:
    
    PATTERNS_ROLES = {
        "Backend": [r"backend", r"python", r"django", r"flask", r"node", r"java", r"golang", r"ruby"],
        "Frontend": [r"frontend", r"react", r"angular", r"vue", r"javascript", r"typescript", r"css", r"html"],
        "Full Stack": [r"full\s*stack", r"full-stack"],
        "DevOps": [r"devops", r"aws", r"cloud", r"docker", r"kubernetes", r"terraform", r"ci/cd"],
        "Data/AI": [r"data", r"machine learning", r"ai", r"analytics", r"pandas", r"numpy", r"tensor", r"pytorch"],
        "QA/Automation": [r"qa", r"quality assurance", r"automation", r"tester", r"selenium", r"pytest"],
    }
    
    PATTERNS_EXP = {
        "Fresher": [r"fresher", r"entry level", r"junior", r"graduate", r"0-", r"0\+ years", r"intern"],
        "Experienced": [r"senior", r"lead", r"principal", r"architect", r"[2-9]\+ years", r"10\+ years"],
    }

    @staticmethod
    def categorize(title: str, description: str = "") -> tuple[str, str]:
        """
        Returns (Role Category, Experience Level)
        """
        text = f"{title} {description}".lower()
        
        role = "Software Engineer"
        for category, patterns in JobCategorizer.PATTERNS_ROLES.items():
            if any(re.search(p, text) for p in patterns):
                role = category
                break  # Simplistic first-match wins
                
        experience = "Unknown"
        # Check Fresher first as it's more specific sometimes
        if any(re.search(p, text) for p in JobCategorizer.PATTERNS_EXP["Fresher"]):
            experience = "Fresher"
        elif any(re.search(p, text) for p in JobCategorizer.PATTERNS_EXP["Experienced"]):
            experience = "Experienced"
            
        return role, experience
