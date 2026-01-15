from config.settings import ALLOWED_LOCATIONS, BLOCKED_LOCATIONS
from src.utils.logger import logger

class LocationFilter:
    @staticmethod
    def is_allowed(location_str: str) -> bool:
        """
        Returns True if the location is allowed based on settings.
        Algorithm:
        1. If BLOCKED_LOCATIONS match -> False
        2. If ALLOWED_LOCATIONS is empty -> True (Allow all)
        3. If ALLOWED_LOCATIONS match -> True
        4. Else -> False
        """
        if not location_str:
            return False
            
        loc_normalized = location_str.lower()
        
        # 1. Check Blocklist
        if BLOCKED_LOCATIONS:
            for blocked in BLOCKED_LOCATIONS:
                if blocked.lower() in loc_normalized:
                    logger.info(f"Filtered out job location '{location_str}' (Blocked: {blocked})")
                    return False
        
        # 2. Check Whitelist
        if not ALLOWED_LOCATIONS:
            return True
            
        for allowed in ALLOWED_LOCATIONS:
            if allowed.lower() in loc_normalized:
                return True
                
        logger.info(f"Filtered out job location '{location_str}' (Not in allowed list)")
        return False
