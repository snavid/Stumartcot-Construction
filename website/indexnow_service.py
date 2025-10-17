import requests
import logging
from typing import List, Optional
from flask import current_app

logger = logging.getLogger(__name__)

class IndexNowService:
    """Service for submitting URLs to IndexNow API for search engine indexing"""
    
    def __init__(self):
        self.api_endpoint = "https://api.indexnow.org/indexnow"
        self.domain = "stumarcot.co.tz"
        self.api_key = "ad293330bfa04dea8c2efb331d1ccfa7"
        self.base_url = f"https://{self.domain}"
    
    def submit_url(self, url: str) -> bool:
        """
        Submit a single URL to IndexNow API
        
        Args:
            url: The URL to submit (can be relative or absolute)
            
        Returns:
            bool: True if submission was successful, False otherwise
        """
        try:
            # Ensure URL is absolute
            if not url.startswith('http'):
                url = f"{self.base_url}{url}"
            
            payload = {
                "host": self.domain,
                "key": self.api_key,
                "urlList": [url]
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 202]:
                logger.info(f"IndexNow submission successful for URL: {url}")
                return True
            else:
                logger.warning(f"IndexNow submission failed for URL: {url}. Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"IndexNow submission error for URL: {url}. Error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in IndexNow submission for URL: {url}. Error: {str(e)}")
            return False
    
    def submit_urls(self, urls: List[str]) -> bool:
        """
        Submit multiple URLs to IndexNow API
        
        Args:
            urls: List of URLs to submit (can be relative or absolute)
            
        Returns:
            bool: True if submission was successful, False otherwise
        """
        try:
            # Ensure all URLs are absolute
            absolute_urls = []
            for url in urls:
                if not url.startswith('http'):
                    url = f"{self.base_url}{url}"
                absolute_urls.append(url)
            
            payload = {
                "host": self.domain,
                "key": self.api_key,
                "urlList": absolute_urls
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=10,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 202]:
                logger.info(f"IndexNow batch submission successful for {len(urls)} URLs")
                return True
            else:
                logger.warning(f"IndexNow batch submission failed. Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"IndexNow batch submission error. Error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in IndexNow batch submission. Error: {str(e)}")
            return False
    
    def notify_product_change(self, product_id: Optional[int] = None, action: str = "update") -> None:
        """
        Notify IndexNow about product-related changes
        
        Args:
            product_id: ID of the product (None for general product changes)
            action: Type of action ('add', 'update', 'delete')
        """
        urls_to_notify = [
            "/products",  # Products listing page
            "/sitemap_products.xml"  # Product sitemap
        ]
        
        if product_id:
            urls_to_notify.append(f"/product-single/{product_id}")
        
        # Submit URLs asynchronously (non-blocking)
        try:
            self.submit_urls(urls_to_notify)
        except Exception as e:
            logger.error(f"Error notifying IndexNow about product {action}: {str(e)}")
    
    def notify_category_change(self, category_id: Optional[int] = None, action: str = "update") -> None:
        """
        Notify IndexNow about category-related changes
        
        Args:
            category_id: ID of the category (None for general category changes)
            action: Type of action ('add', 'update', 'delete')
        """
        urls_to_notify = [
            "/categories",  # Categories listing page
            "/sitemap_categories.xml"  # Category sitemap
        ]
        
        if category_id:
            urls_to_notify.append(f"/category/{category_id}")
        
        # Submit URLs asynchronously (non-blocking)
        try:
            self.submit_urls(urls_to_notify)
        except Exception as e:
            logger.error(f"Error notifying IndexNow about category {action}: {str(e)}")
    
    def notify_site_update(self) -> None:
        """
        Notify IndexNow about general site updates (sitemap, home page)
        """
        urls_to_notify = [
            "/",  # Home page
            "/sitemap.xml",  # Main sitemap
            "/sitemap_index.xml"  # Sitemap index
        ]
        
        try:
            self.submit_urls(urls_to_notify)
        except Exception as e:
            logger.error(f"Error notifying IndexNow about site update: {str(e)}")

# Create a global instance
indexnow_service = IndexNowService()
