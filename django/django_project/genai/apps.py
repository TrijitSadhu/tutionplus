"""
GenAI App Configuration
"""

from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class GenaiConfig(AppConfig):
    """Configuration for GenAI app"""
    
    name = 'genai'
    verbose_name = 'GenAI Content Generation System'
    
    def ready(self):
        """Initialize the GenAI app"""
        logger.info("GenAI Content Generation System initialized")
        
        # You can add signal handlers here if needed
        # from . import signals  # if you create a signals.py file
