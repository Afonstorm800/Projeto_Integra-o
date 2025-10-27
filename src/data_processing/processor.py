"""
Data Processing Module
Provides utilities for data normalization, cleansing, and composition using Regular Expressions
"""

import re
from typing import Any, Callable, Dict, List, Optional, Union


class DataProcessor:
    """Main class for data processing operations using regular expressions"""
    
    def __init__(self):
        self.patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[\d\s\-\(\)]{10,}$',
            'url': r'^https?://[^\s/$.?#].[^\s]*$',
            'cpf': r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
            'cnpj': r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
            'zipcode': r'^\d{5}-?\d{3}$',
            'date_iso': r'^\d{4}-\d{2}-\d{2}$',
            'credit_card': r'^\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}$'
        }
    
    def normalize_text(self, text: str, remove_special: bool = True, 
                      lowercase: bool = True, remove_extra_spaces: bool = True) -> str:
        """
        Normalize text by cleaning and standardizing it
        
        Args:
            text: Input text to normalize
            remove_special: Remove special characters
            lowercase: Convert to lowercase
            remove_extra_spaces: Remove extra whitespace
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        result = text
        
        if remove_extra_spaces:
            result = re.sub(r'\s+', ' ', result).strip()
        
        if remove_special:
            result = re.sub(r'[^\w\s@.-]', '', result)
        
        if lowercase:
            result = result.lower()
        
        return result
    
    def validate_pattern(self, text: str, pattern_name: str) -> bool:
        """
        Validate if text matches a predefined pattern
        
        Args:
            text: Text to validate
            pattern_name: Name of the pattern to use
            
        Returns:
            True if valid, False otherwise
        """
        if pattern_name not in self.patterns:
            raise ValueError(f"Unknown pattern: {pattern_name}")
        
        pattern = self.patterns[pattern_name]
        return bool(re.match(pattern, text))
    
    def extract_pattern(self, text: str, pattern: str, group: int = 0) -> List[str]:
        """
        Extract all matches of a pattern from text
        
        Args:
            text: Input text
            pattern: Regular expression pattern
            group: Group number to extract (0 for entire match)
            
        Returns:
            List of matches
        """
        matches = re.finditer(pattern, text)
        return [match.group(group) for match in matches]
    
    def replace_pattern(self, text: str, pattern: str, replacement: str) -> str:
        """
        Replace all occurrences of a pattern in text
        
        Args:
            text: Input text
            pattern: Regular expression pattern
            replacement: Replacement string
            
        Returns:
            Modified text
        """
        return re.sub(pattern, replacement, text)
    
    def cleanse_data(self, data: Union[str, List, Dict], 
                    operations: List[Dict[str, Any]]) -> Union[str, List, Dict]:
        """
        Apply a series of cleansing operations to data
        
        Args:
            data: Input data (string, list, or dict)
            operations: List of operations to apply
            
        Returns:
            Cleansed data
        """
        if isinstance(data, str):
            return self._cleanse_string(data, operations)
        elif isinstance(data, list):
            return [self.cleanse_data(item, operations) for item in data]
        elif isinstance(data, dict):
            return {key: self.cleanse_data(value, operations) 
                   for key, value in data.items()}
        return data
    
    def _cleanse_string(self, text: str, operations: List[Dict[str, Any]]) -> str:
        """Apply cleansing operations to a string"""
        result = text
        for op in operations:
            op_type = op.get('type')
            if op_type == 'replace':
                result = self.replace_pattern(result, op['pattern'], op['replacement'])
            elif op_type == 'normalize':
                result = self.normalize_text(result, **op.get('params', {}))
            elif op_type == 'extract':
                matches = self.extract_pattern(result, op['pattern'])
                result = matches[0] if matches else result
        return result
    
    def normalize_phone(self, phone: str) -> str:
        """Normalize phone number to standard format"""
        digits = re.sub(r'\D', '', phone)
        if len(digits) >= 10:
            if len(digits) == 11:
                return f"+{digits[:2]} ({digits[2:4]}) {digits[4:9]}-{digits[9:]}"
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        return phone
    
    def normalize_cpf(self, cpf: str) -> str:
        """Normalize CPF to standard format"""
        digits = re.sub(r'\D', '', cpf)
        if len(digits) == 11:
            return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
        return cpf
    
    def normalize_cnpj(self, cnpj: str) -> str:
        """Normalize CNPJ to standard format"""
        digits = re.sub(r'\D', '', cnpj)
        if len(digits) == 14:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
        return cnpj
    
    def normalize_zipcode(self, zipcode: str) -> str:
        """Normalize Brazilian zipcode to standard format"""
        digits = re.sub(r'\D', '', zipcode)
        if len(digits) == 8:
            return f"{digits[:5]}-{digits[5:]}"
        return zipcode
    
    def mask_sensitive_data(self, text: str, data_type: str = 'email') -> str:
        """
        Mask sensitive data for privacy
        
        Args:
            text: Input text containing sensitive data
            data_type: Type of data to mask (email, phone, cpf, credit_card)
            
        Returns:
            Masked text
        """
        if data_type == 'email':
            return re.sub(r'([a-zA-Z0-9._%+-]{2})[a-zA-Z0-9._%+-]*@', r'\1***@', text)
        elif data_type == 'phone':
            return re.sub(r'(\d{2})\d+(\d{4})', r'\1*****\2', text)
        elif data_type == 'cpf':
            return re.sub(r'(\d{3})\.\d{3}\.(\d{3}-\d{2})', r'\1.***.***-**', text)
        elif data_type == 'credit_card':
            return re.sub(r'(\d{4})[\s-]?\d{4}[\s-]?\d{4}[\s-]?(\d{4})', 
                         r'\1-****-****-\2', text)
        return text
    
    def compose_data(self, template: str, data: Dict[str, Any]) -> str:
        """
        Compose data using a template with placeholders
        
        Args:
            template: Template string with {key} placeholders
            data: Dictionary with values to replace
            
        Returns:
            Composed string
        """
        result = template
        for key, value in data.items():
            pattern = r'\{' + re.escape(key) + r'\}'
            result = re.sub(pattern, str(value), result)
        return result
