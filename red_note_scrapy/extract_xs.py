#!/usr/bin/env python3
"""
Extract X-s parameter generation logic from sign.js
"""

import re
import json

def extract_xs_logic():
    with open('sign.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("=== X-s Parameter Extraction ===\n")
    
    # Find all Xs-related patterns
    xs_patterns = re.findall(r"(X'.s\[\w+\]|Xs\w*\s*[=,;]})", content)
    print(f"Found {len(xs_patterns)} Xs-related patterns")
    
    # Extract the string array first
    string_match = re.search(r"var gY=\[(.*?)\];", content)
    strings = []
    if string_match:
        strings = re.findall(r"'([^']*)'", string_match.group(1))
        print(f"Extracted {len(strings)} strings from array")
    
    # Look for the actual Xs generation
    print("\nSearching for Xs assignment patterns...")
    
    # Find Xs property access
    xs_access_patterns = [
        r"Xs.*?=",
        r"X'.s.*?=",
        r"xs.*?=",
        r"X_s.*?="
    ]
    
    for pattern in xs_access_patterns:
        matches = re.findall(pattern, content)
        if matches:
            print(f"\nPattern '{pattern}': {len(matches)} matches")
            for i, match in enumerate(matches[:3]):
                print(f"  {i+1}. {match[:100]}...")
    
    # Look for function calls that might generate Xs
    print("\nLooking for Xs generation functions...")
    
    # Find function definitions that might be related
    func_patterns = re.findall(r"function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*Xs[^}]*\}", content, re.DOTALL)
    print(f"Functions containing Xs: {len(func_patterns)}")
    
    # Search for the main algorithm flow
    print("\nAnalyzing algorithm structure...")
    
    # Find return statements that might include Xs
    return_patterns = re.findall(r"return\s+[^;]*Xs[^;]*", content)
    print(f"Return statements with Xs: {len(return_patterns)}")
    
    # Look for object creation with Xs
    object_patterns = re.findall(r"\{[^}]*Xs[^}]*\}", content)
    print(f"Object definitions with Xs: {len(object_patterns)}")
    
    # Extract the signing algorithm step by step
    print("\nExtracting signing algorithm...")
    
    # Find the main signing function
    main_func = re.search(r"function X\(\)\{([^}]*)\}", content)
    if main_func:
        print("Found main function X()")
        x_body = main_func.group(1)
        
        # Look for key steps in the algorithm
        steps = []
        
        # Find string array accesses
        string_accesses = re.findall(r'gY\[(\d+)\]', x_body)
        print(f"String accesses in main function: {len(string_accesses)}")
        
        # Look for the actual Xs generation
        xs_gen = re.search(r"X'.s\[\w+\]\s*=\s*([^;,]+)", x_body)
        if xs_gen:
            print(f"Xs generation found: {xs_gen.group(1)[:100]}...")
    
    # Try to understand the parameter structure
    print("\nAnalyzing parameter structure...")
    
    # Look for X-s-common patterns
    common_patterns = re.findall(r"X[^a-zA-Z0-9_]*s[^a-zA-Z0-9_]*common", content, re.IGNORECASE)
    print(f"X-s-common patterns: {len(common_patterns)}")
    
    # Look for X-t patterns (timestamp)
    xt_patterns = re.findall(r"X[^a-zA-Z0-9_]*t[^a-zA-Z0-9_]", content, re.IGNORECASE)
    print(f"X-t patterns: {len(xt_patterns)}")
    
    # Create a simplified deobfuscation map
    print("\nCreating deobfuscation map...")
    
    # Map key strings
    key_mappings = {}
    for i, s in enumerate(strings):
        if len(s) > 10 and any(c in s for c in ['=', '&', '?', '/', ':']):
            key_mappings[i] = s
    
    print(f"Found {len(key_mappings)} potentially important strings")
    
    # Save the analysis
    analysis = {
        'string_count': len(strings),
        'xs_patterns': len(xs_patterns),
        'key_mappings': key_mappings,
        'functions_with_xs': len(func_patterns),
        'return_with_xs': len(return_patterns)
    }
    
    with open('xs_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print("\nAnalysis saved to xs_analysis.json")
    
    return strings, key_mappings

if __name__ == "__main__":
    strings, mappings = extract_xs_logic()