#!/usr/bin/env python3
"""Quick test for custom base64 encoding"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generators"))
from xhs_common_generator import encode_xs_common, _encode_utf8, _b64_encode

# Test 1: basic encoding
test_json = '{"s0":"win32","s1":"","x0":"test"}'
result = encode_xs_common(test_json)
print(f"Input:  {test_json}")
print(f"Output: {result}")
print(f"Starts with eyJ (standard b64): {result.startswith('eyJ')}")
print(f"First 3 chars: {result[:3]}")
print()

# Test 2: verify encodeUtf8
bytes_list = _encode_utf8('{"test":1}')
print(f"encodeUtf8 bytes: {bytes_list}")
print(f"Expected:         {[123, 34, 116, 101, 115, 116, 34, 58, 49, 125]}")
print()

# Test 3: full x-s-common payload
payload = {
    "s0": "win32", "s1": "", "x0": "17720051434350D61ed46e",
    "x1": "PC", "x2": "PC", "x3": "xhs-pc-web", "x4": "4.79.0",
    "x5": "17720051434354F5efc", "x6": "", "x7": "",
    "x8": "1772005143435fDDEAc7A",
    "x9": "adbad0acf7af7787ddaa1b57731e0053",
    "x10": 328, "x11": "normal"
}
json_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
result2 = encode_xs_common(json_str)
print(f"Full payload result: {result2[:60]}...")
print(f"Length: {len(result2)}")
print(f"NOT standard base64: {not result2.startswith('eyJ')}")
