import json
import logging
from datetime import datetime
from typing import Dict, Any, List

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """Set up logger with file and console handlers"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def validate_knime_data(data: Any) -> Dict[str, Any]:
    """
    Validate data structure from Knime workflow
    """
    validation_result = {
        'is_valid': False,
        'errors': [],
        'record_count': 0,
        'data_type': type(data).__name__
    }
    
    try:
        if data is None:
            validation_result['errors'].append('Data cannot be None')
            return validation_result
            
        # Check if data is a list or dict
        if isinstance(data, list):
            validation_result['record_count'] = len(data)
            if len(data) == 0:
                validation_result['errors'].append('Data list is empty')
            else:
                validation_result['is_valid'] = True
                
        elif isinstance(data, dict):
            validation_result['record_count'] = 1
            validation_result['is_valid'] = True
            
        else:
            validation_result['errors'].append(f'Invalid data type: {type(data)}. Expected list or dict')
            
    except Exception as e:
        validation_result['errors'].append(f'Validation error: {str(e)}')
    
    return validation_result

def transform_knime_payload(data: Any, source: str = 'knime') -> Dict[str, Any]:
    """
    Transform Knime data into standardized payload for Node-RED
    """
    payload = {
        'metadata': {
            'source': source,
            'received_at': datetime.now().isoformat(),
            'batch_id': datetime.now().strftime('%Y%m%d_%H%M%S'),
            'version': '1.0'
        },
        'data': data
    }
    
    # Add validation info
    validation = validate_knime_data(data)
    payload['metadata']['validation'] = validation
    
    return payload

def create_error_response(message: str, status_code: int, details: Any = None) -> Dict[str, Any]:
    """Create standardized error response"""
    error_response = {
        'status': 'error',
        'message': message,
        'timestamp': datetime.now().isoformat(),
        'code': status_code
    }
    
    if details:
        error_response['details'] = details
        
    return error_response

def create_success_response(message: str, data: Any = None, **kwargs) -> Dict[str, Any]:
    """Create standardized success response"""
    response = {
        'status': 'success',
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if data is not None:
        response['data'] = data
        
    # Add any additional kwargs
    response.update(kwargs)
    
    return response