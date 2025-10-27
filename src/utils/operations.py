"""
Value Operations Module
Operations on data values (transformations, calculations, etc.)
"""

from typing import Any, Callable, Dict, List, Union
import statistics
from datetime import datetime, timedelta
import re


class ValueOperations:
    """Class for performing operations on values"""
    
    @staticmethod
    def transform(value: Any, operation: str, params: Dict[str, Any] = None) -> Any:
        """
        Apply transformation to a value
        
        Args:
            value: Input value
            operation: Operation name
            params: Operation parameters
            
        Returns:
            Transformed value
        """
        params = params or {}
        
        operations = {
            'uppercase': lambda v: str(v).upper(),
            'lowercase': lambda v: str(v).lower(),
            'capitalize': lambda v: str(v).capitalize(),
            'strip': lambda v: str(v).strip(),
            'abs': lambda v: abs(float(v)),
            'round': lambda v: round(float(v), params.get('decimals', 0)),
            'int': lambda v: int(float(v)),
            'float': lambda v: float(v),
            'str': lambda v: str(v),
            'bool': lambda v: bool(v),
            'reverse': lambda v: str(v)[::-1],
            'length': lambda v: len(str(v)),
            'multiply': lambda v: float(v) * params.get('factor', 1),
            'add': lambda v: float(v) + params.get('amount', 0),
            'subtract': lambda v: float(v) - params.get('amount', 0),
            'divide': lambda v: float(v) / params.get('divisor', 1),
            'power': lambda v: float(v) ** params.get('exponent', 2),
        }
        
        if operation in operations:
            return operations[operation](value)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    @staticmethod
    def aggregate(values: List[Union[int, float]], operation: str) -> Union[int, float]:
        """
        Aggregate a list of numeric values
        
        Args:
            values: List of values
            operation: Aggregation operation
            
        Returns:
            Aggregated result
        """
        operations = {
            'sum': sum,
            'avg': statistics.mean,
            'mean': statistics.mean,
            'median': statistics.median,
            'min': min,
            'max': max,
            'count': len,
            'stdev': statistics.stdev if len(values) > 1 else lambda x: 0,
            'variance': statistics.variance if len(values) > 1 else lambda x: 0,
        }
        
        if operation in operations:
            return operations[operation](values)
        else:
            raise ValueError(f"Unknown aggregation: {operation}")
    
    @staticmethod
    def apply_formula(data: Dict[str, Any], formula: str) -> Any:
        """
        Apply a formula to data
        
        Args:
            data: Dictionary with variable values
            formula: Formula string (e.g., "a + b * 2")
            
        Returns:
            Formula result
        """
        # Create safe evaluation environment
        safe_dict = {
            'abs': abs,
            'round': round,
            'min': min,
            'max': max,
            'sum': sum,
            'len': len,
            '__builtins__': {}
        }
        safe_dict.update(data)
        
        try:
            return eval(formula, safe_dict)
        except Exception as e:
            raise ValueError(f"Error evaluating formula '{formula}': {str(e)}")
    
    @staticmethod
    def filter_values(values: List[Any], condition: Callable[[Any], bool]) -> List[Any]:
        """
        Filter values based on condition
        
        Args:
            values: List of values
            condition: Filter function
            
        Returns:
            Filtered list
        """
        return [v for v in values if condition(v)]
    
    @staticmethod
    def map_values(values: List[Any], mapper: Callable[[Any], Any]) -> List[Any]:
        """
        Map values using a function
        
        Args:
            values: List of values
            mapper: Mapping function
            
        Returns:
            Mapped list
        """
        return [mapper(v) for v in values]
    
    @staticmethod
    def reduce_values(values: List[Any], reducer: Callable[[Any, Any], Any], 
                     initial: Any = None) -> Any:
        """
        Reduce values using a function
        
        Args:
            values: List of values
            reducer: Reduction function
            initial: Initial value
            
        Returns:
            Reduced result
        """
        from functools import reduce
        if initial is not None:
            return reduce(reducer, values, initial)
        return reduce(reducer, values)
    
    @staticmethod
    def convert_units(value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert between units
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            Converted value
        """
        # Length conversions
        length_units = {
            'm': 1,
            'km': 1000,
            'cm': 0.01,
            'mm': 0.001,
            'mi': 1609.34,
            'yd': 0.9144,
            'ft': 0.3048,
            'in': 0.0254,
        }
        
        # Weight conversions
        weight_units = {
            'kg': 1,
            'g': 0.001,
            'mg': 0.000001,
            'lb': 0.453592,
            'oz': 0.0283495,
        }
        
        # Temperature conversions (to Celsius)
        temp_to_celsius = {
            'C': lambda x: x,
            'F': lambda x: (x - 32) * 5/9,
            'K': lambda x: x - 273.15,
        }
        
        # Temperature conversions (from Celsius)
        temp_from_celsius = {
            'C': lambda x: x,
            'F': lambda x: x * 9/5 + 32,
            'K': lambda x: x + 273.15,
        }
        
        # Try length conversion
        if from_unit in length_units and to_unit in length_units:
            meters = value * length_units[from_unit]
            return meters / length_units[to_unit]
        
        # Try weight conversion
        if from_unit in weight_units and to_unit in weight_units:
            kg = value * weight_units[from_unit]
            return kg / weight_units[to_unit]
        
        # Try temperature conversion
        if from_unit in temp_to_celsius and to_unit in temp_from_celsius:
            celsius = temp_to_celsius[from_unit](value)
            return temp_from_celsius[to_unit](celsius)
        
        raise ValueError(f"Cannot convert from {from_unit} to {to_unit}")
    
    @staticmethod
    def calculate_percentage(part: float, total: float, decimals: int = 2) -> float:
        """
        Calculate percentage
        
        Args:
            part: Part value
            total: Total value
            decimals: Number of decimal places
            
        Returns:
            Percentage
        """
        if total == 0:
            return 0
        return round((part / total) * 100, decimals)
    
    @staticmethod
    def calculate_growth_rate(old_value: float, new_value: float, 
                             decimals: int = 2) -> float:
        """
        Calculate growth rate
        
        Args:
            old_value: Old value
            new_value: New value
            decimals: Number of decimal places
            
        Returns:
            Growth rate as percentage
        """
        if old_value == 0:
            return float('inf') if new_value > 0 else 0
        return round(((new_value - old_value) / old_value) * 100, decimals)
    
    @staticmethod
    def interpolate(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
        """
        Linear interpolation
        
        Args:
            x: Input value
            x1, y1: First point
            x2, y2: Second point
            
        Returns:
            Interpolated value
        """
        if x2 == x1:
            return y1
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    
    @staticmethod
    def normalize(values: List[float], min_val: float = 0, max_val: float = 1) -> List[float]:
        """
        Normalize values to a range
        
        Args:
            values: List of values
            min_val: Minimum value of range
            max_val: Maximum value of range
            
        Returns:
            Normalized values
        """
        if not values:
            return []
        
        current_min = min(values)
        current_max = max(values)
        
        if current_max == current_min:
            return [min_val] * len(values)
        
        return [
            min_val + (v - current_min) * (max_val - min_val) / (current_max - current_min)
            for v in values
        ]
