"""
LLM Provider Module
Handles interaction with Gemini Pro, OpenAI and other LLM APIs
"""

import json
import logging
from typing import Dict, List, Any, Optional
from genai.config import (
    DEFAULT_LLM_PROVIDER,
    GROQ_API_KEY, GROQ_MODEL, GROQ_TEMPERATURE, GROQ_MAX_OUTPUT_TOKENS,
    GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_OUTPUT_TOKENS,
    OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE
)

logger = logging.getLogger(__name__)

class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, model: str = None):
        self.model = model or GEMINI_MODEL
        self.temperature = GEMINI_TEMPERATURE
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from a prompt"""
        raise NotImplementedError
    
    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate JSON response from the model"""
        raise NotImplementedError


class GroqProvider(LLMProvider):
    """Groq Cloud provider"""
    
    def __init__(self, api_key: str = GROQ_API_KEY, model: str = GROQ_MODEL):
        super().__init__(model)
        self.api_key = api_key
        self.model = model
        self.temperature = GROQ_TEMPERATURE
        self.max_output_tokens = GROQ_MAX_OUTPUT_TOKENS
        
        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
        except ImportError:
            logger.error("groq library not installed. Install with: pip install groq")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {str(e)}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Groq API
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters
        
        Returns:
            Generated text from the model
        """
        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                max_tokens=self.max_output_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API Error: {str(e)}")
            raise
    
    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate JSON response from the model"""
        json_prompt = f"""{prompt}

IMPORTANT: Your response MUST be valid JSON only. Do not include any markdown formatting or explanations."""
        
        response_text = self.generate(json_prompt, **kwargs)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response_text}")
            return {}


class GeminiProvider(LLMProvider):
    """Google Gemini Pro provider"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL):
        super().__init__(model)
        self.api_key = api_key
        self.model = model
        self.temperature = GEMINI_TEMPERATURE
        self.max_output_tokens = GEMINI_MAX_OUTPUT_TOKENS
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(self.model)
        except ImportError:
            logger.warning("google-generativeai library not installed or Python < 3.8. Falling back to OpenAI.")
            raise ImportError("Gemini requires Python 3.8+. Falling back to OpenAI.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            raise
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Gemini Pro API
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters
        
        Returns:
            Generated text from the model
        """
        try:
            response = self.client.generate_content(
                prompt,
                generation_config={
                    'temperature': self.temperature,
                    'max_output_tokens': self.max_output_tokens,
                    **kwargs
                }
            )
            return response.text
        
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            raise
    
    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate JSON response from the model"""
        # Add JSON instruction to prompt
        json_prompt = f"""{prompt}

IMPORTANT: Your response MUST be valid JSON only. Do not include any markdown formatting or explanations."""
        
        response_text = self.generate(json_prompt, **kwargs)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response_text}")
            return {}


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider (BACKUP)"""
    
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        super().__init__(model)
        self.api_key = api_key
        self.model = model
        self.temperature = OPENAI_TEMPERATURE
        
        try:
            import openai
            openai.api_key = api_key
            self.client = openai
        except ImportError:
            logger.error("openai library not installed. Install with: pip install openai")
            raise
    
    def generate(self, prompt: str, response_format: str = "text", **kwargs) -> str:
        """
        Generate text using OpenAI API
        
        Args:
            prompt: The prompt to send to the model
            response_format: 'text' or 'json' for JSON mode
            **kwargs: Additional parameters to pass to the API
        
        Returns:
            Generated text from the model
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                **kwargs
            }
            
            if response_format == "json":
                params["response_format"] = {"type": "json_object"}
            
            response = self.client.ChatCompletion.create(**params)
            
            return response.choices[0].message["content"]
        
        except Exception as e:
            logger.error(f"OpenAI API Error: {str(e)}")
            raise
    
    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate JSON response from the model"""
        response_text = self.generate(prompt, response_format="json", **kwargs)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response_text}")
            return {}


class MockLLMProvider(LLMProvider):
    """Mock provider for testing without API calls"""
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Return mock data for testing"""
        return "Mock response for testing"
    
    def generate_json(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Return mock JSON data for testing"""
        return {
            "question": "Sample Question",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A"
        }


def get_llm_provider(provider: str = None, **kwargs) -> LLMProvider:
    """
    Get an LLM provider instance
    
    Args:
        provider: 'groq' (default), 'gemini', 'openai', 'mock', etc.
        **kwargs: Additional parameters for the provider
    
    Returns:
        LLMProvider instance
    """
    provider = provider or DEFAULT_LLM_PROVIDER
    
    if provider.lower() == "groq":
        try:
            return GroqProvider(**kwargs)
        except ImportError:
            logger.warning(f"Groq not available. Falling back to Gemini.")
            return GeminiProvider(**kwargs)
    elif provider.lower() == "gemini":
        try:
            return GeminiProvider(**kwargs)
        except ImportError:
            logger.warning(f"Gemini not available (requires Python 3.8+). Falling back to OpenAI.")
            return OpenAIProvider(**kwargs)
    elif provider.lower() == "openai":
        return OpenAIProvider(**kwargs)
    elif provider.lower() == "mock":
        return MockLLMProvider(**kwargs)
    else:
        raise ValueError(f"Unknown provider: {provider}")


# Default instance (uses config setting)
default_llm = get_llm_provider()
