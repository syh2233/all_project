#!/usr/bin/env python3
"""
Example usage of the X-s generator for xiaohongshu web scraping
"""

import requests
import json
from xs_generator import XSGenerator

def example_api_call():
    """Example of making an API call with X-s parameter"""
    
    # Initialize the X-s generator
    xs_gen = XSGenerator()
    
    # Example API endpoint
    url = "https://www.xiaohongshu.com/api/sns/v3/page/notes"
    
    # Request parameters
    params = {
        "page": 1,
        "page_size": 20,
        "sort": "time"
    }
    
    # Headers (you need to get these from your browser)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.xiaohongshu.com/",
        "Origin": "https://www.xiaohongshu.com",
        # Add other required headers like cookie, authorization, etc.
    }
    
    # Generate X-s parameter
    # Note: You may need to include your actual user_id if required
    xs_value = xs_gen.generate_xs(
        url=url + "?" + "&".join([f"{k}={v}" for k, v in params.items()]),
        method="GET",
        user_id=""  # Add your user_id if needed
    )
    
    # Add X-s to headers
    headers["X-s"] = xs_value
    
    try:
        # Make the request
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            print("Request successful!")
            print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"Request failed with status {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error making request: {e}")

def example_post_request():
    """Example of making a POST request with X-s parameter"""
    
    # Initialize the X-s generator
    xs_gen = XSGenerator()
    
    # Example API endpoint
    url = "https://www.xiaohongshu.com/api/sns/v2/note/feed"
    
    # Request data
    data = {
        "note_id": "1234567890",
        "cursor": "10",
        "count": "20"
    }
    
    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # Add other required headers
    }
    
    # Generate X-s parameter
    xs_value = xs_gen.generate_xs(
        url=url,
        method="POST",
        data=data,
        user_id=""  # Add your user_id if needed
    )
    
    # Add X-s to headers
    headers["X-s"] = xs_value
    
    try:
        # Make the request
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("POST request successful!")
            print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"POST request failed with status {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error making POST request: {e}")

if __name__ == "__main__":
    print("=== X-s Generator Usage Examples ===\n")
    
    print("1. GET request example:")
    example_api_call()
    
    print("\n2. POST request example:")
    example_post_request()
    
    print("\nNote: These examples may not work without proper authentication and cookies.")
    print("You need to extract valid cookies and other headers from your browser session.")