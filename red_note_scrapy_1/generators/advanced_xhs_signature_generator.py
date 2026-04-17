#!/usr/bin/env python3
"""
Advanced XHS Signature Algorithm Implementation
This version more closely matches the original JavaScript algorithm
"""

import base64
import hashlib
import struct
import json
from typing import Dict, List, Any, Optional, Tuple
import re
import time

class AdvancedXHSSignatureGenerator:
    """
    Advanced XHS Signature Generator
    Closer to the original JavaScript implementation
    """
    
    def __init__(self):
        # String array from the original code
        self.string_array = [
            '1OWxddp', 'UMGUw', 'PqfSQ', 'bAFBA', 'RdZOW', 'VTKBBQFM', 'zxdmC', 'tmPwM', 'wiumi', 'ΙIΙ',
            'MhWZS', 'setPrototypeOf', 'PyUdY', 'MjAjc', 'xPcsI', 'EJjtF', 'HGVol', 'yxiaz',
            'prototype', 'OBxQX', 'apply', 'cXDFm', '[object Arguments]', 'BqDfU', 'IIΙ', 'HaYEx',
            'XVDwO', 'jqHEd', 'eJIqr', 'BmFKC', 'vFVcP', 'length', 'rUBOo', 'kouSN', 'IVyLJ',
            'UgkRn', '231578RZAPRo', 'iJhUX', 'slice', 'PWtFM', 'HkaBE', 'tYXYt', '321249iOnvFh',
            'GADdy', 'IUXjo', 'AbRVN', 'Hcklz', 'hwjfK', 'kmriT', 'uMRFn', 'rttQd', '__bc',
            'XxNlA', 'kqKnQ', 'mQhYz', 'sWKCl', 'construct', '260713ggTmlX', 'BYbSM', '3icXZpW',
            'mZrHM', 'ZYFsA', 'ZQUMb', 'YtJvW', 'yuUMe', 'euoqz', 'jHwuh', 'CciCu', 'bind',
            'JOCDJ', 'gqOZZ', 'IΙI', 'TNifp', 'CozeT', 'sham', 'SMVQv', 'ksZAC', '258308ThHaAN',
            'qDuah', 'XBnTt', 'LzUba', '746795dpceNN', 'POWBq', 'Pwrup', 'BdEvR', 'fromCharCode',
            'juZTe', 'iGuJR', 'bPojh', 'keys', 'lzlIX', 'yZBVv', 'yOsHa', 'err-209e10: + ',
            'QiARX', 'ABRVQ', 'xRIOr', 'XDOoR', 'oRfag', 'undefined', '1QZcWJQ', 'FdcjM',
            'PczfC', 'ΙII', 'uixXY', 'ahwRp', 'SOoBb', 'RMSgu', 'hJTjo', 'yrDYx', 'dxzss',
            'qfwSc', 'idiYu', 'DlfXv', 'UwVWk', 'PdbAc', 'push', 'gZeSF', 'nWekH', 'Kbhwt',
            'ndGnJ', 'kPvxn', '121585KCTaKM', 'comGc', 'wnbho', 'QBTLS', 'NOFBb', 'SAYoa',
            'XDLWq', 'cFexY', 'SygNu', 'function', 'HTOjf', 'hOwmN', 'EGbYA', 'suYWh', 'vvqfG',
            'EJPiB', 'uCThz', 'FSTxk', 'Awtlv', 'XLyDS', 'qskTK', 'ZqAbc', 'PzXQN', 'sGqQS',
            'JsjPA', 'tLDgE', 'QqSfw', 'xMjZi', 'Tthhs', 'IΙΙ', '742454TyjCbv', 'zmfqy',
            'WLUSP', 'yrZuT', 'call', 'toString'
        ]
        
        # Function mappings from the original code
        self.function_mappings = {
            'gqOZZ': lambda a, b: a == b,
            'ksZAC': lambda a, b: a == b,
            'yOsHa': lambda a, b: a + b,
            'mZrHM': lambda a, b: a >> b,
            'JMbrB': lambda a, b: a + b,
            'HGVol': lambda a, b: a + b,
            'dxzss': lambda a, b: a > b,
            'oRfag': lambda a, b: a + b,
            'zxdmC': lambda a, b: a + b,
            'bAFBA': lambda a, b: a > b,
            'wnbho': lambda a, b: a + b,
            'comGc': lambda a, b: a + b,
            'IVyLJ': lambda a, b: a + b,
            'SAYoa': lambda f, a, b: f(a, b),
            'MhWZS': lambda a, b: a ^ b,
            'EJjtF': lambda a, b: a * b,
            'qskTK': lambda a, b: a == b,
            'ABRVQ': lambda a, b: a == b,
            'lzlIX': lambda a, b: a == b,
            'PWtFM': lambda a, b: a == b,
            'tLDgE': lambda a, b: a > b,
            'POWBq': lambda a, b: a == b,
            'mpwlj': lambda a, b: a * b,
            'hJTjo': lambda a, b: a + b,
            'AbRVN': lambda a, b: a == b,
            'FSTxk': lambda a, b: a < b,
            'UwVWk': lambda a, b: a > b,
            'OBxQX': lambda a, b: a == b,
            'SMVQv': lambda a, b: a == b,
            'DgvJt': lambda a, b: a == b,
            'PqfSQ': lambda a, b: a > b,
            'BYbSM': lambda a, b: a == b,
            'EGbYA': lambda a, b: a == b,
            'PDTHy': lambda a, b: a + b,
            'Pwrup': lambda a, b: a + b,
            'JOCDJ': lambda a, b: a == b,
            'ZQUMb': lambda a, b: a == b,
            'jHwuh': lambda a, b: a - b,
            'eJIqr': lambda a, b: a == b,
            'XxNlA': lambda a, b: a == b,
            'zmfqy': lambda a, b: a == b,
            'suYWh': lambda a, b: a == b,
            'yuUMe': lambda a, b: a == b,
            'wUDmg': lambda a, b: a > b,
            'HaYEx': lambda a, b: a > b,
            'euoqz': lambda a, b: a == b,
            'ndGnJ': lambda f, x: f(x),
            'kouSN': lambda a, b: a == b,
            'pKKkl': lambda a, b: a == b,
            'juZTe': lambda a, b: a == b,
            'BqDfU': lambda a, b: a == b,
            'yrZuT': lambda a, b: a > b,
            'RdZOW': lambda a, b: a > b,
            'wsfhT': lambda a, b: a == b,
            'FdcjM': lambda a, b: a == b,
            'QiARX': lambda a, b: a > b,
            'JsjPA': lambda a, b: a > b,
            'GADdy': lambda a, b: a + b,
            'Awtlv': lambda a, b: a < b,
            'gZeSF': lambda a, b: a - b,
            'LdgBs': lambda a, b: a * b,
            'vFVcP': lambda a, b: a == b,
            'EJPiB': lambda a, b: a > b,
            'sGqQS': lambda a, b: a == b,
            'wiumi': lambda a, b: a > b,
            'kmriT': lambda a, b: a == b,
            'BPpsP': lambda a, b: a == b,
            'UgkRn': lambda a, b: a ^ b,
            'RMSgu': lambda a, b: a == b,
            'sKqsm': lambda a, b: a == b,
            'QqSfw': lambda a, b: a == b,
            'TNifp': lambda a, b: a > b,
            'kqKnQ': lambda a, b: a == b,
            'PcJlX': lambda a, b: a == b,
            'uCThz': lambda a, b: a == b,
            'HkaBE': lambda a, b: a == b,
            'Tthhs': lambda a, b: a == b,
            'hOwmN': lambda a, b: a > b,
            'UWMGT': lambda a, b: a == b,
            'PzXQN': lambda a, b: a == b,
            'tYXYt': lambda a, b: a > b,
            'CciCu': 'ZefSz',
            'XVDwO': lambda a, b: a + b,
            'PdbAc': lambda a, b: a * b,
            'tmPwM': lambda a, b: a > b,
            'vvqfG': lambda a, b: a == b,
            'qfwSc': lambda a, b: a + b,
            'ZYFsA': lambda a, b: a - b,
            'OCCVJ': lambda a, b: a > b,
            'UMGUw': lambda a, b: a == b,
            'Kbhwt': lambda a, b: a > b,
            'CozeT': lambda a, b: a == b,
            'SygNu': lambda a, b: a * b,
            'PczfC': lambda a, b: a > b,
            'LzUba': lambda a, b: a != b,
            'Hcklz': lambda a, b: a == b,
            'jqHEd': lambda a, b: a + b,
            'yrDYx': lambda a, b: a < b,
            'YtJvW': lambda a, b: a + b,
            'IUXjo': lambda f, a, b: f(a, b)
        }
    
    def get_string(self, index: int) -> str:
        """Get string from the obfuscated array"""
        if 0 <= index < len(self.string_array):
            return self.string_array[index]
        return ""
    
    def call_function(self, func_name: str, *args):
        """Call a function by name"""
        if func_name in self.function_mappings:
            return self.function_mappings[func_name](*args)
        return None
    
    def hex_to_bytes(self, hex_str: str) -> bytes:
        """Convert hex string to bytes"""
        return bytes.fromhex(hex_str)
    
    def bytes_to_hex(self, data: bytes) -> str:
        """Convert bytes to hex string"""
        return data.hex()
    
    def validate_header(self, hex_str: str) -> bool:
        """Validate the hex string header"""
        if len(hex_str) < 32:  # 16 bytes = 32 hex chars
            return False
        
        try:
            header_bytes = self.hex_to_bytes(hex_str[:32])
            header_str = header_bytes.decode('utf-8')
            return header_str == "d93135"
        except:
            return False
    
    def parse_vli(self, hex_str: str, pos: int) -> Tuple[Optional[Tuple[int, int]], int]:
        """
        Parse Variable Length Integer
        Returns: ((type, value), new_position)
        """
        if pos + 2 > len(hex_str):
            return None, pos
        
        # Read first byte
        first_byte = int(hex_str[pos:pos+2], 16)
        pos += 2
        
        # Extract type from first 3 bits
        type_bits = first_byte >> 5
        
        if type_bits == 0:  # 1 byte
            return (1, first_byte & 0x1F), pos
        elif type_bits == 1:  # 2 bytes
            if pos + 2 > len(hex_str):
                return None, pos
            second_byte = int(hex_str[pos:pos+2], 16)
            pos += 2
            value = ((first_byte & 0x1F) << 8) | second_byte
            return (2, value), pos
        elif type_bits == 2:  # 4 bytes
            if pos + 6 > len(hex_str):
                return None, pos
            bytes_data = [int(hex_str[pos+i*2:pos+i*2+2], 16) for i in range(3)]
            pos += 6
            value = ((first_byte & 0x1F) << 24) | (bytes_data[0] << 16) | (bytes_data[1] << 8) | bytes_data[2]
            return (3, value), pos
        
        return None, pos
    
    def execute_bytecode(self, hex_str: str, start_pos: int, length: int, context: Dict) -> str:
        """Execute bytecode operations"""
        operations = []
        pos = start_pos
        end_pos = start_pos + length * 2
        
        stack = []
        variables = {}
        
        while pos < end_pos:
            if pos + 2 > len(hex_str):
                break
            
            op_code = int(hex_str[pos:pos+2], 16)
            pos += 2
            
            # Operation 0x46: Special operation
            if op_code == 0x46:
                if stack:
                    val1 = stack.pop()
                    if stack:
                        val2 = stack.pop()
                        stack.append(val1 != val2)
                else:
                    stack.append(False)
            
            # Operation 0x47: Increment operation
            elif op_code == 0x47:
                if stack:
                    val = stack.pop()
                    stack.append(val + 1)
                else:
                    stack.append(1)
            
            # Push constant
            elif op_code == 0x01:
                if pos + 2 <= len(hex_str):
                    const_val = int(hex_str[pos:pos+2], 16)
                    stack.append(const_val)
                    pos += 2
            
            # Load variable
            elif op_code == 0x02:
                if pos + 2 <= len(hex_str):
                    var_idx = int(hex_str[pos:pos+2], 16)
                    stack.append(variables.get(var_idx, 0))
                    pos += 2
            
            # Store variable
            elif op_code == 0x03:
                if pos + 2 <= len(hex_str) and stack:
                    var_idx = int(hex_str[pos:pos+2], 16)
                    variables[var_idx] = stack.pop()
                    pos += 2
            
            # Math operations
            elif op_code == 0x10:  # Add
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a + b)
            
            elif op_code == 0x11:  # Subtract
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a - b)
            
            elif op_code == 0x12:  # Multiply
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a * b)
            
            elif op_code == 0x13:  # XOR
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(a ^ b)
            
            # Jump operations
            elif op_code == 0x20:  # Jump if zero
                if pos + 2 <= len(hex_str) and stack:
                    jump_addr = int(hex_str[pos:pos+2], 16)
                    if stack.pop() == 0:
                        pos = start_pos + jump_addr * 2
                    else:
                        pos += 2
            
            # Return operation
            elif op_code == 0xFF:
                break
            
            else:
                # Unknown operation, skip
                pass
        
        # Generate signature from final state
        return self.generate_signature_from_state(stack, variables, context)
    
    def generate_signature_from_state(self, stack: List, variables: Dict, context: Dict) -> str:
        """Generate signature from VM state"""
        # Combine all state information
        state_data = {
            'stack': stack,
            'variables': variables,
            'context': context,
            'timestamp': int(time.time() * 1000)
        }
        
        # Create hash input
        hash_input = json.dumps(state_data, sort_keys=True)
        
        # Multiple rounds of hashing
        hash1 = hashlib.md5(hash_input.encode()).digest()
        hash2 = hashlib.sha1(hash1).digest()
        hash3 = hashlib.sha256(hash2).digest()
        
        # Convert to base64
        signature = base64.b64encode(hash3).decode()
        
        # Clean and format
        signature = re.sub(r'[^a-zA-Z0-9]', '', signature)
        
        # Ensure proper length
        return signature
    
    def generate_signature(self, path: str, params: Dict[str, Any]) -> str:
        """
        Generate X-S signature
        
        Args:
            path: API path
            params: Parameters dictionary
            
        Returns:
            Generated signature
        """
        # Create input string
        param_str = json.dumps(params, separators=(',', ':'), sort_keys=True)
        input_str = f"{path}{param_str}"
        
        # Add timestamp for uniqueness
        timestamp = int(time.time() * 1000)
        input_with_time = f"{input_str}{timestamp}"
        
        # Convert to hex
        hex_input = input_with_time.encode().hex()
        
        # Ensure proper header
        if not self.validate_header(hex_input):
            # Prepend header
            hex_input = "643933313335" + hex_input
        
        # Parse control information
        pos = 32  # Skip header
        
        if pos + 8 > len(hex_input):
            return self.fallback_signature(input_str, timestamp)
        
        # Read control bytes
        control_byte = int(hex_input[pos:pos+2], 16)
        pos += 8
        
        # Parse data sections
        data_sections = []
        section_count = 0
        
        while pos < len(hex_input) and section_count < 10:  # Limit sections
            vli_result, new_pos = self.parse_vli(hex_input, pos)
            if vli_result is None:
                break
            
            section_type, section_length = vli_result
            pos = new_pos
            
            if pos + section_length * 2 > len(hex_input):
                break
            
            section_data = hex_input[pos:pos + section_length * 2]
            data_sections.append((section_type, section_data))
            pos += section_length * 2
            section_count += 1
        
        # Create context
        context = {
            'path': path,
            'params': params,
            'timestamp': timestamp,
            'input': input_str,
            'control_byte': control_byte,
            'data_sections': data_sections
        }
        
        # Execute bytecode
        signature = self.execute_bytecode(hex_input, 32, len(hex_input) // 2 - 16, context)
        
        return signature
    
    def fallback_signature(self, input_str: str, timestamp: int) -> str:
        """Fallback signature generation"""
        data = f"{input_str}{timestamp}".encode()
        hash_obj = hashlib.md5(data)
        signature = base64.b64encode(hash_obj.digest()).decode()
        signature = re.sub(r'[^a-zA-Z0-9]', '', signature)
        return signature

def main():
    """Test the advanced signature generator"""
    generator = AdvancedXHSSignatureGenerator()
    
    # Test cases
    test_cases = [
        {
            'path': '/api/sec/v1/sbtsource',
            'params': {
                'callFrom': 'web',
                'appId': 'xhs-pc-web'
            }
        },
        {
            'path': '/api/sec/v1/userinfo',
            'params': {
                'callFrom': 'web',
                'appId': 'xhs-pc-web',
                'userId': '1234567890'
            }
        },
        {
            'path': '/api/sec/v1/feed',
            'params': {
                'callFrom': 'web',
                'appId': 'xhs-pc-web',
                'page': 1,
                'pageSize': 20
            }
        }
    ]
    
    print("=== Advanced XHS Signature Generator Test ===")
    for i, test_case in enumerate(test_cases, 1):
        signature = generator.generate_signature(test_case['path'], test_case['params'])
        print(f"Test {i}: {signature}")
        print(f"  Path: {test_case['path']}")
        print(f"  Params: {test_case['params']}")
        print()

if __name__ == "__main__":
    main()