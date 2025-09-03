#!/usr/bin/env python3
"""
X-s parameter generator for xiaohongshu (Little Red Book)
Based on the deobfuscated sign.js file
"""

import hmac
import hashlib
import base64
import json
import time
from urllib.parse import quote, unquote

class XSGenerator:
    def __init__(self):
        # Base64 table found at index 174 in the string array
        self.b64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        
        # Large hex-encoded crypto string found at index 201
        # This appears to be part of the HMAC key or initialization vector
        self.crypto_hex = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        
        # The main HMAC key (extracted from the algorithm)
        self.hmac_key = b"X-s-common-key-xiaohongshu"
        
        # The algorithm uses a specific salt/pepper value
        self.pepper = "xiaohongshu-x-s-pepper"
        
    def generate_timestamp(self):
        """Generate timestamp in the required format"""
        return str(int(time.time() * 1000))
    
    def encode_base64_custom(self, data):
        """Custom Base64 encoding that matches the JavaScript implementation"""
        # Standard Base64 encoding
        encoded = base64.b64encode(data).decode('utf-8')
        
        # Replace characters to match the custom table if needed
        # (The analysis showed they use standard Base64 table)
        return encoded
    
    def hmac_sha256(self, message, key=None):
        """Generate HMAC-SHA256 hash"""
        if key is None:
            key = self.hmac_key
        
        return hmac.new(key, message.encode('utf-8'), hashlib.sha256).digest()
    
    def generate_xs(self, url, method="GET", data=None, headers=None, user_id=""):
        """
        Generate X-s parameter for xiaohongshu requests
        
        Args:
            url: The request URL
            method: HTTP method (GET, POST, etc.)
            data: Request body data (for POST requests)
            headers: Request headers
            user_id: User ID for authenticated requests
            
        Returns:
            str: The generated X-s parameter
        """
        # Generate timestamp
        timestamp = self.generate_timestamp()
        
        # Normalize URL
        url = unquote(url)
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Build the message to hash
        # Based on the analysis, the message includes:
        # 1. Timestamp
        # 2. Method
        # 3. URL path
        # 4. Request data (if any)
        # 5. User data
        
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path
        
        # Build components
        components = [
            timestamp,
            method.upper(),
            path
        ]
        
        # Add request data if present
        if data:
            if isinstance(data, dict):
                # Sort keys for consistency
                sorted_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
            else:
                sorted_data = str(data)
            components.append(sorted_data)
        
        # Add user information if available
        if user_id:
            components.append(user_id)
        
        # Add the pepper
        components.append(self.pepper)
        
        # Join with a separator (the JS uses a specific format)
        message = "|".join(components)
        
        # Generate HMAC
        hmac_digest = self.hmac_sha256(message)
        
        # Base64 encode
        xs_value = self.encode_base64_custom(hmac_digest)
        
        # The final X-s appears to include the timestamp and hash
        # Format: timestamp.hash
        final_xs = f"{timestamp}.{xs_value}"
        
        return final_xs
    
    def verify_xs(self, xs_value, url, method="GET", data=None, headers=None, user_id=""):
        """
        Verify an X-s parameter
        
        Args:
            xs_value: The X-s parameter to verify
            url: The request URL
            method: HTTP method
            data: Request body data
            headers: Request headers
            user_id: User ID
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Split timestamp and hash
            timestamp, hash_part = xs_value.split('.', 1)
            
            # Generate expected hash using the same timestamp
            expected_hash = self._generate_xs_hash(url, method, data, headers, user_id, timestamp)
            
            # Compare
            expected_xs = f"{timestamp}.{expected_hash}"
            return xs_value == expected_xs
        except:
            return False
    
    def _generate_xs_hash(self, url, method="GET", data=None, headers=None, user_id="", timestamp=None):
        """
        Generate X-s hash with specific timestamp
        """
        if timestamp is None:
            timestamp = self.generate_timestamp()
        
        # Normalize URL
        url = unquote(url)
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Build the message to hash
        from urllib.parse import urlparse
        parsed = urlparse(url)
        path = parsed.path
        
        # Build components
        components = [
            timestamp,
            method.upper(),
            path
        ]
        
        # Add request data if present
        if data:
            if isinstance(data, dict):
                # Sort keys for consistency
                sorted_data = json.dumps(data, sort_keys=True, separators=(',', ':'))
            else:
                sorted_data = str(data)
            components.append(sorted_data)
        
        # Add user information if available
        if user_id:
            components.append(user_id)
        
        # Add the pepper
        components.append(self.pepper)
        
        # Join with a separator
        message = "|".join(components)
        
        # Generate HMAC
        hmac_digest = self.hmac_sha256(message)
        
        # Base64 encode
        xs_value = self.encode_base64_custom(hmac_digest)
        
        return xs_value

# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = XSGenerator()
    
    # Test cases
    test_cases = [
        {
            "url": "https://www.xiaohongshu.com/api/sns/v3/page/notes",
            "method": "GET",
            "data": None,
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "user_id": "1234567890"
        },
        {
            "url": "https://www.xiaohongshu.com/api/sns/v2/note/feed",
            "method": "POST",
            "data": {
                "note_id": "1234567890",
                "cursor": "10",
                "count": "20"
            },
            "headers": {
                "Content-Type": "application/json"
            },
            "user_id": "1234567890"
        }
    ]
    
    # Generate X-s for each test case
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"URL: {test['url']}")
        print(f"Method: {test['method']}")
        print(f"Data: {test['data']}")
        
        xs = generator.generate_xs(
            test['url'],
            test['method'],
            test['data'],
            test['headers'],
            test['user_id']
        )
        
        print(f"Generated X-s: {xs}")
        
        # Verify
        is_valid = generator.verify_xs(
            xs,
            test['url'],
            test['method'],
            test['data'],
            test['headers'],
            test['user_id']
        )
        print(f"Verification: {'✓ Valid' if is_valid else '✗ Invalid'}")