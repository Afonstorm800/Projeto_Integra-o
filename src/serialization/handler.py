"""
Serialization Module
Handles data import/export for XML, JSON, and YAML formats
"""

import json
import yaml
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Union
from pathlib import Path


class SerializationHandler:
    """Handler for multiple serialization formats"""
    
    def __init__(self):
        self.supported_formats = ['json', 'xml', 'yaml', 'yml']
    
    # JSON Operations
    def export_json(self, data: Union[Dict, List], filepath: str, 
                   indent: int = 2, ensure_ascii: bool = False) -> None:
        """
        Export data to JSON file
        
        Args:
            data: Data to export
            filepath: Output file path
            indent: Indentation level
            ensure_ascii: Ensure ASCII encoding
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    
    def import_json(self, filepath: str) -> Union[Dict, List]:
        """
        Import data from JSON file
        
        Args:
            filepath: Input file path
            
        Returns:
            Parsed data
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def json_to_string(self, data: Union[Dict, List], indent: int = 2) -> str:
        """Convert data to JSON string"""
        return json.dumps(data, indent=indent, ensure_ascii=False)
    
    def string_to_json(self, json_string: str) -> Union[Dict, List]:
        """Parse JSON string to data"""
        return json.loads(json_string)
    
    # XML Operations
    def export_xml(self, data: Dict, filepath: str, root_name: str = 'root') -> None:
        """
        Export data to XML file
        
        Args:
            data: Data to export
            filepath: Output file path
            root_name: Name of root element
        """
        root = self._dict_to_xml(data, root_name)
        tree = ET.ElementTree(root)
        ET.indent(tree, space='  ')
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
    
    def import_xml(self, filepath: str) -> Dict:
        """
        Import data from XML file
        
        Args:
            filepath: Input file path
            
        Returns:
            Parsed data as dictionary
        """
        tree = ET.parse(filepath)
        root = tree.getroot()
        return self._xml_to_dict(root)
    
    def xml_to_string(self, data: Dict, root_name: str = 'root') -> str:
        """Convert data to XML string"""
        root = self._dict_to_xml(data, root_name)
        ET.indent(root, space='  ')
        return ET.tostring(root, encoding='unicode')
    
    def string_to_xml(self, xml_string: str) -> Dict:
        """Parse XML string to data"""
        root = ET.fromstring(xml_string)
        return self._xml_to_dict(root)
    
    def _dict_to_xml(self, data: Union[Dict, List, Any], root_name: str = 'item') -> ET.Element:
        """Convert dictionary to XML element"""
        element = ET.Element(root_name)
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    child = self._dict_to_xml(value, key)
                    element.append(child)
                else:
                    child = ET.SubElement(element, key)
                    child.text = str(value)
        elif isinstance(data, list):
            for item in data:
                child = self._dict_to_xml(item, 'item')
                element.append(child)
        else:
            element.text = str(data)
        
        return element
    
    def _xml_to_dict(self, element: ET.Element) -> Union[Dict, List, str]:
        """Convert XML element to dictionary"""
        if len(element) == 0:
            return element.text or ''
        
        result = {}
        for child in element:
            child_data = self._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        
        return result
    
    # YAML Operations
    def export_yaml(self, data: Union[Dict, List], filepath: str, 
                   default_flow_style: bool = False) -> None:
        """
        Export data to YAML file
        
        Args:
            data: Data to export
            filepath: Output file path
            default_flow_style: Use flow style
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=default_flow_style, 
                     allow_unicode=True, sort_keys=False)
    
    def import_yaml(self, filepath: str) -> Union[Dict, List]:
        """
        Import data from YAML file
        
        Args:
            filepath: Input file path
            
        Returns:
            Parsed data
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def yaml_to_string(self, data: Union[Dict, List]) -> str:
        """Convert data to YAML string"""
        return yaml.dump(data, allow_unicode=True, sort_keys=False)
    
    def string_to_yaml(self, yaml_string: str) -> Union[Dict, List]:
        """Parse YAML string to data"""
        return yaml.safe_load(yaml_string)
    
    # Generic Operations
    def export(self, data: Union[Dict, List], filepath: str, 
              format: str = None, **kwargs) -> None:
        """
        Export data to file (auto-detect or specify format)
        
        Args:
            data: Data to export
            filepath: Output file path
            format: Format (json, xml, yaml) - auto-detected if None
            **kwargs: Additional arguments for specific exporters
        """
        if format is None:
            format = Path(filepath).suffix.lstrip('.')
        
        format = format.lower()
        
        if format == 'json':
            self.export_json(data, filepath, **kwargs)
        elif format == 'xml':
            self.export_xml(data, filepath, **kwargs)
        elif format in ['yaml', 'yml']:
            self.export_yaml(data, filepath, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_data(self, filepath: str, format: str = None) -> Union[Dict, List]:
        """
        Import data from file (auto-detect or specify format)
        
        Args:
            filepath: Input file path
            format: Format (json, xml, yaml) - auto-detected if None
            
        Returns:
            Parsed data
        """
        if format is None:
            format = Path(filepath).suffix.lstrip('.')
        
        format = format.lower()
        
        if format == 'json':
            return self.import_json(filepath)
        elif format == 'xml':
            return self.import_xml(filepath)
        elif format in ['yaml', 'yml']:
            return self.import_yaml(filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def convert(self, source_file: str, target_file: str, 
               source_format: str = None, target_format: str = None) -> None:
        """
        Convert data from one format to another
        
        Args:
            source_file: Source file path
            target_file: Target file path
            source_format: Source format (auto-detected if None)
            target_format: Target format (auto-detected if None)
        """
        data = self.import_data(source_file, source_format)
        self.export(data, target_file, target_format)
