#!/usr/bin/env python3
"""
Advanced sign.js deobfuscator
"""

import re
import json
from collections import defaultdict

def deobfuscate_sign_js():
    with open('sign.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== Advanced Sign.js Analysis ===\n")
    
    # Extract and map the string array
    string_match = re.search(r"var gY=\[(.*?)\];", content)
    if string_match:
        strings = re.findall(r"'([^']*)'", string_match.group(1))
        print(f"String array size: {len(strings)}")
        
        # Create a mapping for deobfuscation
        string_map = {i: s for i, s in enumerate(strings)}
        
        # Look for key patterns
        key_strings = []
        for i, s in enumerate(strings):
            if any(keyword in s.lower() for keyword in 
                   ['hmac', 'sha', 'crypto', 'hash', 'sign', 'base64', 'encode', 
                    'x-s', 'xs', 'signature', 'a1', 'b1', 'c1', 'd1']):
                key_strings.append((i, s))
        
        print(f"\nKey strings found:")
        for idx, s in key_strings:
            print(f"  [{idx}]: {s[:50]}...")
    
    # Find the main algorithm structure
    print("\n=== Function Analysis ===")
    
    # Extract function X() body
    x_func_match = re.search(r"function X\(\)\{([^}]*)\}", content)
    if x_func_match:
        print("Function X() found")
        x_body = x_func_match.group(1)
        print(f"Length: {len(x_body)} chars")
        
        # Look for string array accesses
        accesses = re.findall(r'gY\[(\d+)\]', x_body)
        print(f"String accesses in X(): {len(accesses)}")
        
        # Find the actual logic
        if accesses:
            print("\nFirst 10 string accesses in X():")
            for i, access in enumerate(accesses[:10]):
                idx = int(access)
                if idx < len(strings):
                    print(f"  gY[{access}] = '{strings[idx]}'")
    
    # Find function O(s,K)
    o_func_match = re.search(r"function O\(s,K\)\{([^}]*)\}", content)
    if o_func_match:
        print("\nFunction O(s,K) found - likely HMAC function")
        o_body = o_func_match.group(1)
        print(f"Length: {len(o_body)} chars")
        
        # Look for key operations
        operations = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*[=+\-*/]', o_body)
        print(f"Operations in O(): {len(set(operations))}")
        
        # Find returns
        returns = re.findall(r'return\s+([^;]+)', o_body)
        if returns:
            print(f"Return in O(): {returns[0][:100]}...")
    
    # Look for the actual signing flow
    print("\n=== Algorithm Flow Analysis ===")
    
    # Find all function calls
    calls = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\(', content)
    call_counts = defaultdict(int)
    for call in calls:
        call_counts[call] += 1
    
    print("Top function calls:")
    for call, count in sorted(call_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
        if call != 'function' and len(call) > 1:
            print(f"  {call}: {count} times")
    
    # Look for timestamp handling
    timestamps = re.findall(r'(?:Date\.now|getTime|timestamp|0x[0-9a-fA-F]+)', content)
    print(f"\nTimestamp/Hex patterns: {len(timestamps)}")
    
    # Search for X-s parameter generation
    xs_patterns = [
        r'X[^a-zA-Z0-9_]*s[^a-zA-Z0-9_]',
        r'xs[^a-zA-Z0-9_]',
        r'X_s',
        r'x-s',
        r'x_s'
    ]
    
    for pattern in xs_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"Pattern '{pattern}': {len(matches)} matches")
    
    # Look for Base64 operations
    b64_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    if b64_table in content:
        print("\nBase64 table found!")
        
        # Find Base64 encoding logic
        b64_patterns = re.findall(r'(?:fromCharCode|charAt|charCodeAt).*?gY\[\d+\]', content)
        print(f"Base64 operations: {len(b64_patterns)}")
    
    # Try to reconstruct the algorithm
    print("\n=== Algorithm Reconstruction ===")
    
    # Find the main entry point
    main_calls = re.findall(r'X\([^)]*\)', content)
    print(f"X() calls: {len(main_calls)}")
    
    # Look for parameter building
    param_builds = re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*?\+.*?gY\[\d+\]', content)
    print(f"Parameter building operations: {len(param_builds)}")
    
    # Find crypto operations
    crypto_ops = re.findall(r'(?:create|update|digest|sign|hash|HMAC|SHA)', content, re.IGNORECASE)
    print(f"Crypto operations found: {len(crypto_ops)}")
    
    return {
        'strings': strings,
        'string_map': string_map,
        'key_strings': key_strings,
        'call_counts': call_counts
    }

if __name__ == "__main__":
    result = deobfuscate_sign_js()