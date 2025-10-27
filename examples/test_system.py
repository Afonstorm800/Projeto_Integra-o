"""
Simple Test Script
Tests core functionality without heavy dependencies
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_data_processing():
    """Test data processing module"""
    print("\n=== Testing Data Processing ===")
    from data_processing import DataProcessor
    
    processor = DataProcessor()
    
    # Test normalization
    text = "  Hello   World!  @#$  "
    result = processor.normalize_text(text)
    print(f"✓ Normalize text: '{text}' -> '{result}'")
    assert "hello" in result and "world" in result, "Text normalization failed"
    
    # Test email validation
    email = "user@example.com"
    is_valid = processor.validate_pattern(email, 'email')
    print(f"✓ Validate email: '{email}' -> {is_valid}")
    assert is_valid == True, "Email validation failed"
    
    # Test phone normalization
    phone = "11987654321"
    result = processor.normalize_phone(phone)
    print(f"✓ Normalize phone: '{phone}' -> '{result}'")
    
    # Test CPF normalization
    cpf = "12345678901"
    result = processor.normalize_cpf(cpf)
    print(f"✓ Normalize CPF: '{cpf}' -> '{result}'")
    assert result == "123.456.789-01", "CPF normalization failed"
    
    # Test data masking
    sensitive = "My email is john.doe@example.com"
    result = processor.mask_sensitive_data(sensitive, 'email')
    print(f"✓ Mask email: '{sensitive}' -> '{result}'")
    
    # Test template composition
    template = "Hello {name}, your order #{order} is ready!"
    data = {"name": "Alice", "order": "12345"}
    result = processor.compose_data(template, data)
    print(f"✓ Compose template: '{result}'")
    assert "Alice" in result and "12345" in result, "Template composition failed"
    
    print("✓ All data processing tests passed!")


def test_serialization():
    """Test serialization module"""
    print("\n=== Testing Serialization ===")
    from serialization import SerializationHandler
    
    handler = SerializationHandler()
    
    # Test data
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "metadata": {
            "version": "1.0",
            "count": 2
        }
    }
    
    # Test JSON
    json_str = handler.json_to_string(data)
    parsed = handler.string_to_json(json_str)
    print(f"✓ JSON serialization: {len(json_str)} chars")
    assert parsed["metadata"]["count"] == 2, "JSON serialization failed"
    
    # Test XML
    xml_str = handler.xml_to_string(data)
    parsed_xml = handler.string_to_xml(xml_str)
    print(f"✓ XML serialization: {len(xml_str)} chars")
    
    # Test YAML
    yaml_str = handler.yaml_to_string(data)
    parsed_yaml = handler.string_to_yaml(yaml_str)
    print(f"✓ YAML serialization: {len(yaml_str)} chars")
    assert parsed_yaml["metadata"]["count"] == 2, "YAML serialization failed"
    
    # Test file operations
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Export to JSON
    json_file = os.path.join(data_dir, 'test_users.json')
    handler.export_json(data, json_file)
    print(f"✓ Exported to: {json_file}")
    
    # Import from JSON
    imported = handler.import_json(json_file)
    print(f"✓ Imported {len(imported['users'])} users")
    assert len(imported['users']) == 2, "JSON import/export failed"
    
    # Export to XML
    xml_file = os.path.join(data_dir, 'test_users.xml')
    handler.export_xml(data, xml_file)
    print(f"✓ Exported to: {xml_file}")
    
    # Export to YAML
    yaml_file = os.path.join(data_dir, 'test_users.yaml')
    handler.export_yaml(data, yaml_file)
    print(f"✓ Exported to: {yaml_file}")
    
    # Test conversion
    output_file = os.path.join(data_dir, 'converted.xml')
    handler.convert(json_file, output_file)
    print(f"✓ Converted JSON to XML: {output_file}")
    
    print("✓ All serialization tests passed!")


def test_jobs():
    """Test job control module"""
    print("\n=== Testing Job Control ===")
    from jobs import Job, Pipeline, JobStatus
    
    # Define test functions
    def load_data(context):
        return {"records": [1, 2, 3, 4, 5]}
    
    def process_data(context):
        records = context.get('job_load_result', {}).get('records', [])
        return {"processed": [x * 2 for x in records]}
    
    def save_data(context):
        processed = context.get('job_process_result', {}).get('processed', [])
        return {"saved_count": len(processed)}
    
    # Create pipeline
    pipeline = Pipeline("test_pipeline")
    
    # Add jobs
    pipeline.add_job(Job("load", load_data))
    pipeline.add_job(Job("process", process_data, depends_on=["load"]))
    pipeline.add_job(Job("save", save_data, depends_on=["process"]))
    
    print(f"✓ Created pipeline with {len(pipeline.jobs)} jobs")
    
    # Get execution order
    order = pipeline.get_execution_order()
    print(f"✓ Execution order: {order}")
    assert order == ["load", "process", "save"], "Execution order is incorrect"
    
    # Run pipeline
    result = pipeline.run()
    print(f"✓ Pipeline executed")
    
    # Check results
    assert result['job_load_result']['records'] == [1, 2, 3, 4, 5], "Load job failed"
    assert result['job_process_result']['processed'] == [2, 4, 6, 8, 10], "Process job failed"
    assert result['job_save_result']['saved_count'] == 5, "Save job failed"
    
    # Get status
    status = pipeline.get_status_summary()
    print(f"✓ Pipeline status: {status['status_counts']}")
    print(f"✓ Total duration: {status['total_duration']:.3f}s")
    
    assert status['status_counts']['success'] == 3, "Not all jobs succeeded"
    
    print("✓ All job control tests passed!")


def test_api_client():
    """Test API client module"""
    print("\n=== Testing API Client ===")
    from api import APIClient
    
    # Create client
    client = APIClient("https://api.github.com")
    print("✓ Created API client")
    
    # Set headers
    client.session.headers.update({"User-Agent": "Test"})
    print("✓ Set headers")
    
    # Test authentication methods
    client.set_api_key("test_key", "X-API-Key")
    assert "X-API-Key" in client.session.headers, "API key not set"
    print("✓ Set API key")
    
    client.set_auth_token("test_token")
    assert "Authorization" in client.session.headers, "Auth token not set"
    print("✓ Set auth token")
    
    print("✓ All API client tests passed!")


def test_value_operations():
    """Test value operations"""
    print("\n=== Testing Value Operations ===")
    from utils import ValueOperations
    
    ops = ValueOperations()
    
    # Test transform
    result = ops.transform(42.567, "round", {"decimals": 2})
    print(f"✓ Transform (round): {result}")
    assert result == 42.57, "Round transformation failed"
    
    result = ops.transform("hello", "uppercase")
    print(f"✓ Transform (uppercase): {result}")
    assert result == "HELLO", "Uppercase transformation failed"
    
    # Test aggregate
    values = [10, 20, 30, 40, 50]
    result = ops.aggregate(values, "avg")
    print(f"✓ Aggregate (avg): {result}")
    assert result == 30, "Average aggregation failed"
    
    result = ops.aggregate(values, "sum")
    print(f"✓ Aggregate (sum): {result}")
    assert result == 150, "Sum aggregation failed"
    
    # Test formula
    data = {"a": 10, "b": 20, "c": 5}
    result = ops.apply_formula(data, "(a + b) * c")
    print(f"✓ Apply formula: {result}")
    assert result == 150, "Formula application failed"
    
    # Test unit conversion
    result = ops.convert_units(100, "cm", "m")
    print(f"✓ Convert units: {result}")
    assert result == 1.0, "Unit conversion failed"
    
    # Test percentage
    result = ops.calculate_percentage(25, 100)
    print(f"✓ Calculate percentage: {result}%")
    assert result == 25.0, "Percentage calculation failed"
    
    # Test growth rate
    result = ops.calculate_growth_rate(100, 150)
    print(f"✓ Calculate growth rate: {result}%")
    assert result == 50.0, "Growth rate calculation failed"
    
    # Test normalize
    values = [10, 20, 30, 40, 50]
    result = ops.normalize(values, 0, 1)
    print(f"✓ Normalize values: {result}")
    assert result[0] == 0.0 and result[-1] == 1.0, "Normalization failed"
    
    print("✓ All value operations tests passed!")


def test_logging():
    """Test logging utilities"""
    print("\n=== Testing Logging ===")
    from utils import setup_logging, get_logger, LogContext
    import logging
    
    # Setup logging
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'test.log')
    
    logger = setup_logging(log_file=log_file, level=logging.INFO)
    print("✓ Setup logging")
    
    # Get named logger
    app_logger = get_logger("TestApp")
    app_logger.info("Test log message")
    print("✓ Created named logger")
    
    # Test log context
    with LogContext(app_logger, "Test Operation"):
        import time
        time.sleep(0.1)
    print("✓ Used log context")
    
    # Verify log file was created
    assert os.path.exists(log_file), "Log file not created"
    print(f"✓ Log file created: {log_file}")
    
    print("✓ All logging tests passed!")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Data Integration System - Test Suite")
    print("=" * 60)
    
    try:
        test_data_processing()
        test_serialization()
        test_jobs()
        test_api_client()
        test_value_operations()
        test_logging()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe Data Integration System is working correctly!")
        print("Check the 'data' folder for generated test files.")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
