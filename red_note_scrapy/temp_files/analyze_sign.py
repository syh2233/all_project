#!/usr/bin/env python3
"""
sign.js deobfuscator and analyzer
"""

import re
import json
from collections import defaultdict

def analyze_sign_js():
    with open('sign.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== Sign.js Analysis ===\n")
    
    # Extract string array
    string_match = re.search(r"var gY=\[(.*?)\];", content)
    if string_match:
        strings = re.findall(r"'([^']*)'", string_match.group(1))
        print(f"String array size: {len(strings)}")
        print(f"First 20 strings: {strings[:20]}")
        print()
        
        # Look for crypto-related strings
        crypto_strings = [s for s in strings if any(keyword in s.lower() for keyword in 
                         ['hmac', 'sha', 'crypto', 'hash', 'sign', 'base64', 'encode'])]
        print(f"Crypto-related strings: {crypto_strings}")
        print()
    
    # Find function definitions
    functions = re.findall(r"function\s+(\w+)\s*\([^)]*\)", content)
    print(f"Named functions: {functions}")
    print()
    
    # Find variable assignments
    assignments = re.findall(r"var\s+(\w+)\s*=", content)
    print(f"Variables: {assignments[:20]}")
    print()
    
    # Analyze control flow
    returns = re.findall(r"return\s+([^;]+)", content)
    print(f"Return statements found: {len(returns)}")
    
    # Look for specific patterns
    patterns = {
        'string concatenation': len(re.findall(r'\+\s*gY\[', content)),
        'function calls': len(re.findall(r'\w+\(', content)),
        'array accesses': len(re.findall(r'gY\[\d+\]', content)),
        'hex numbers': len(re.findall(r'0x[0-9a-fA-F]+', content))
    }
    
    print("\nPattern counts:")
    for pattern, count in patterns.items():
        print(f"  {pattern}: {count}")
    
    # Try to decode the algorithm
    print("\n=== Algorithm Analysis ===")
    
    # Look for the main function logic
    main_func = re.search(r"function X\(\)\{([^}]*)\}", content)
    if main_func:
        print("Main function X() found")
        print("Body length:", len(main_func.group(1)))
    
    # Check for encoded/encrypted content
    if 'hmac' in content.lower():
        print("\nHMAC is present but likely encoded")
        # Look for base64 patterns
        b64_pattern = re.search(r'[A-Za-z0-9+/=]{20,}', content)
        if b64_pattern:
            print("Base64-like pattern found")

if __name__ == "__main__":
    analyze_sign_js()