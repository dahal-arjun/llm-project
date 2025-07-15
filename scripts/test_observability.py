#!/usr/bin/env python
"""
Test script for observability features.
This script sends requests to the API and logs the responses.
"""

import requests
import json
import logging
import os
import time
import argparse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("observability-test")

def test_api(base_url):
    """Test the API endpoints and log the responses."""
    logger.info(f"Testing API at {base_url}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        logger.info(f"Root endpoint response: {response.status_code} - {response.json()}")
    except Exception as e:
        logger.error(f"Error testing root endpoint: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        logger.info(f"Health endpoint response: {response.status_code} - {response.json()}")
    except Exception as e:
        logger.error(f"Error testing health endpoint: {e}")
    
    # Test collections endpoint
    try:
        response = requests.get(f"{base_url}/collections")
        logger.info(f"Collections endpoint response: {response.status_code} - {response.json()}")
    except Exception as e:
        logger.error(f"Error testing collections endpoint: {e}")
    
    # Create a test collection
    try:
        collection_name = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        response = requests.post(f"{base_url}/collections/{collection_name}")
        logger.info(f"Create collection response: {response.status_code} - {response.json()}")
    except Exception as e:
        logger.error(f"Error creating collection: {e}")

def main():
    parser = argparse.ArgumentParser(description="Test API observability")
    parser.add_argument("--url", default="http://localhost:8081", help="Base URL of the API")
    args = parser.parse_args()
    
    test_api(args.url)

if __name__ == "__main__":
    main() 