"""
Integration Demo
Demonstrates a realistic data integration scenario
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processing import DataProcessor
from serialization import SerializationHandler
from jobs import Job, Pipeline
from utils import setup_logging, LogContext, ValueOperations
import logging


def demo_scenario():
    """
    Real-world scenario: Processing customer data from multiple sources
    1. Load data from JSON
    2. Normalize and cleanse data
    3. Transform values
    4. Export to multiple formats
    5. Generate report
    """
    
    print("\n" + "=" * 70)
    print("DEMO: Customer Data Integration Pipeline")
    print("=" * 70)
    
    # Setup logging
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(log_dir, exist_ok=True)
    setup_logging(log_file=os.path.join(log_dir, 'demo.log'), level=logging.INFO)
    logger = logging.getLogger("Demo")
    
    with LogContext(logger, "Customer Data Integration"):
        
        # Sample customer data with inconsistencies
        raw_data = {
            "customers": [
                {
                    "id": 1,
                    "name": "  JOÃO   SILVA  ",
                    "email": "joao.silva@example.com",
                    "phone": "11987654321",
                    "cpf": "12345678901",
                    "revenue": "1500.50"
                },
                {
                    "id": 2,
                    "name": "Maria  Santos",
                    "email": "MARIA@EXAMPLE.COM",
                    "phone": "(21) 98765-4321",
                    "cpf": "123.456.789-09",
                    "revenue": "2800.75"
                },
                {
                    "id": 3,
                    "name": "Pedro Costa  ",
                    "email": "pedro.costa@example.com",
                    "phone": "11 9 8765-4321",
                    "cpf": "98765432100",
                    "revenue": "3200.00"
                }
            ]
        }
        
        print("\n📥 Step 1: Loading raw data...")
        print(f"   Loaded {len(raw_data['customers'])} customer records")
        
        # Job 1: Load and parse data
        def load_data(context):
            logger.info("Loading customer data")
            return {"raw_data": raw_data}
        
        # Job 2: Normalize data
        def normalize_data(context):
            logger.info("Normalizing customer data")
            processor = DataProcessor()
            raw = context['job_load_result']['raw_data']
            
            normalized_customers = []
            for customer in raw['customers']:
                normalized = {
                    "id": customer['id'],
                    "name": processor.normalize_text(customer['name'], lowercase=False),
                    "email": processor.normalize_text(customer['email'], lowercase=True),
                    "phone": processor.normalize_phone(customer['phone']),
                    "cpf": processor.normalize_cpf(customer['cpf']),
                    "revenue": float(customer['revenue'])
                }
                normalized_customers.append(normalized)
            
            print("\n🔄 Step 2: Normalizing data...")
            print(f"   ✓ Normalized names (removed extra spaces)")
            print(f"   ✓ Normalized emails (lowercase)")
            print(f"   ✓ Normalized phone numbers")
            print(f"   ✓ Normalized CPF format")
            print(f"   ✓ Converted revenue to numeric")
            
            return {"normalized_data": normalized_customers}
        
        # Job 3: Calculate metrics
        def calculate_metrics(context):
            logger.info("Calculating metrics")
            ops = ValueOperations()
            customers = context['job_normalize_result']['normalized_data']
            
            revenues = [c['revenue'] for c in customers]
            
            metrics = {
                "total_customers": len(customers),
                "total_revenue": ops.aggregate(revenues, "sum"),
                "average_revenue": ops.aggregate(revenues, "avg"),
                "max_revenue": ops.aggregate(revenues, "max"),
                "min_revenue": ops.aggregate(revenues, "min")
            }
            
            print("\n📊 Step 3: Calculating metrics...")
            print(f"   Total Customers: {metrics['total_customers']}")
            print(f"   Total Revenue: R$ {metrics['total_revenue']:,.2f}")
            print(f"   Average Revenue: R$ {metrics['average_revenue']:,.2f}")
            print(f"   Max Revenue: R$ {metrics['max_revenue']:,.2f}")
            print(f"   Min Revenue: R$ {metrics['min_revenue']:,.2f}")
            
            return {"metrics": metrics}
        
        # Job 4: Export to multiple formats
        def export_data(context):
            logger.info("Exporting data")
            handler = SerializationHandler()
            customers = context['job_normalize_result']['normalized_data']
            metrics = context['job_metrics_result']['metrics']
            
            export_data = {
                "customers": customers,
                "metrics": metrics,
                "report_date": "2024-10-09"
            }
            
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            
            # Export to JSON
            json_file = os.path.join(output_dir, 'customer_report.json')
            handler.export_json(export_data, json_file)
            
            # Export to XML
            xml_file = os.path.join(output_dir, 'customer_report.xml')
            handler.export_xml(export_data, xml_file)
            
            # Export to YAML
            yaml_file = os.path.join(output_dir, 'customer_report.yaml')
            handler.export_yaml(export_data, yaml_file)
            
            print("\n💾 Step 4: Exporting data...")
            print(f"   ✓ Exported to JSON: {json_file}")
            print(f"   ✓ Exported to XML: {xml_file}")
            print(f"   ✓ Exported to YAML: {yaml_file}")
            
            return {"exports_completed": True}
        
        # Job 5: Generate privacy report
        def generate_privacy_report(context):
            logger.info("Generating privacy report")
            processor = DataProcessor()
            customers = context['job_normalize_result']['normalized_data']
            
            privacy_report = []
            for customer in customers:
                masked = {
                    "id": customer['id'],
                    "name": customer['name'],
                    "email": processor.mask_sensitive_data(customer['email'], 'email'),
                    "phone": processor.mask_sensitive_data(customer['phone'], 'phone'),
                    "cpf": processor.mask_sensitive_data(customer['cpf'], 'cpf'),
                    "revenue": f"R$ {customer['revenue']:,.2f}"
                }
                privacy_report.append(masked)
            
            print("\n🔒 Step 5: Privacy report (masked data)...")
            for customer in privacy_report:
                print(f"   Customer #{customer['id']}: {customer['name']}")
                print(f"     Email: {customer['email']}")
                print(f"     Phone: {customer['phone']}")
                print(f"     CPF: {customer['cpf']}")
                print(f"     Revenue: {customer['revenue']}")
            
            return {"privacy_report": privacy_report}
        
        # Create and execute pipeline
        print("\n⚙️  Creating integration pipeline...")
        pipeline = Pipeline("customer_integration")
        
        pipeline.add_job(Job("load", load_data))
        pipeline.add_job(Job("normalize", normalize_data, depends_on=["load"]))
        pipeline.add_job(Job("metrics", calculate_metrics, depends_on=["normalize"]))
        pipeline.add_job(Job("export", export_data, depends_on=["normalize", "metrics"]))
        pipeline.add_job(Job("privacy", generate_privacy_report, depends_on=["normalize"]))
        
        print(f"   Created pipeline with {len(pipeline.jobs)} jobs")
        print(f"   Execution order: {' → '.join(pipeline.get_execution_order())}")
        
        print("\n🚀 Executing pipeline...")
        result = pipeline.run()
        
        # Display summary
        status = pipeline.get_status_summary()
        print("\n" + "=" * 70)
        print("✅ PIPELINE EXECUTION COMPLETED")
        print("=" * 70)
        print(f"Total jobs: {status['total_jobs']}")
        print(f"Successful: {status['status_counts']['success']}")
        print(f"Failed: {status['status_counts']['failed']}")
        print(f"Total duration: {status['total_duration']:.3f}s")
        
        print("\n📁 Generated files:")
        print("   - data/customer_report.json")
        print("   - data/customer_report.xml")
        print("   - data/customer_report.yaml")
        print("   - data/demo.log")
        
        print("\n" + "=" * 70)
        print("✨ Integration demo completed successfully!")
        print("=" * 70)
        
        return result


if __name__ == "__main__":
    try:
        demo_scenario()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
