from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import os
from datetime import datetime
from configs import config
from utils.helpers import (
    setup_logger, validate_knime_data, transform_knime_payload,
    create_error_response, create_success_response
)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])

# Enable CORS
CORS(app)

# Setup logging
os.makedirs('logs', exist_ok=True)
logger = setup_logger('flask_api', app.config['LOG_FILE'], app.config['LOG_LEVEL'])

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        'message': 'Knime to Node-RED API Gateway',
        'version': '1.0',
        'endpoints': {
            'health': '/api/health (GET)',
            'forward_data': '/api/forward-to-nodered (POST)',
            'batch_process': '/api/batch-process (POST)',
            'status': '/api/status (GET)'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Test Node-RED connection
        node_red_health_url = f"{app.config['NODE_RED_URL']}/health"
        node_red_response = requests.get(node_red_health_url, timeout=5)
        node_red_status = 'connected' if node_red_response.status_code == 200 else 'disconnected'
    except:
        node_red_status = 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Flask API Gateway',
        'node_red': node_red_status,
        'environment': 'development' if app.config['DEBUG'] else 'production'
    })

@app.route('/api/forward-to-nodered', methods=['POST'])
def forward_to_nodered():
    """
    Receive data from Knime and forward to Node-RED
    Expected JSON payload from Knime
    """
    logger.info("Received request to forward data to Node-RED")
    
    try:
        # Get and validate JSON data
        if not request.is_json:
            return jsonify(create_error_response(
                'Content-Type must be application/json', 
                400
            )), 400
        
        data = request.get_json()
        
        if data is None:
            return jsonify(create_error_response(
                'Invalid JSON data in request body',
                400
            )), 400
        
        # Validate data structure
        validation = validate_knime_data(data)
        if not validation['is_valid']:
            return jsonify(create_error_response(
                'Data validation failed',
                400,
                details=validation
            )), 400
        
        logger.info(f"Validated data: {validation['record_count']} records, type: {validation['data_type']}")
        
        # Transform payload for Node-RED
        payload = transform_knime_payload(data, 'knime_etl_workflow')
        
        # Forward to Node-RED
        node_red_url = f"{app.config['NODE_RED_URL']}{app.config['NODE_RED_ENDPOINT']}"
        
        logger.info(f"Forwarding data to Node-RED: {node_red_url}")
        
        response = requests.post(
            node_red_url,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=app.config['NODE_RED_TIMEOUT']
        )
        
        # Handle Node-RED response
        if response.status_code == 200:
            logger.info(f"Successfully forwarded data to Node-RED. Response: {response.status_code}")
            
            try:
                node_red_data = response.json()
            except:
                node_red_data = response.text
            
            return jsonify(create_success_response(
                'Data successfully forwarded to Node-RED',
                data={
                    'records_processed': validation['record_count'],
                    'node_red_status': response.status_code,
                    'node_red_response': node_red_data
                },
                validation=validation
            )), 200
            
        else:
            logger.error(f"Node-RED returned error status: {response.status_code}")
            return jsonify(create_error_response(
                f'Node-RED returned status {response.status_code}',
                502,
                details={
                    'node_red_response': response.text,
                    'node_red_status': response.status_code
                }
            )), 502
            
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Node-RED. Service may be down.")
        return jsonify(create_error_response(
            'Cannot connect to Node-RED service. Please ensure Node-RED is running.',
            503
        )), 503
        
    except requests.exceptions.Timeout:
        logger.error("Request to Node-RED timed out.")
        return jsonify(create_error_response(
            'Node-RED request timeout. Service may be overloaded.',
            504
        )), 504
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify(create_error_response(
            f'Internal server error: {str(e)}',
            500
        )), 500

@app.route('/api/batch-process', methods=['POST'])
def batch_process():
    """
    Process batch data with enhanced validation and logging
    """
    logger.info("Received batch process request")
    
    try:
        # Get JSON data
        data = request.get_json()
        
        if data is None:
            return jsonify(create_error_response(
                'Invalid or missing JSON data',
                400
            )), 400
        
        # Enhanced validation
        validation = validate_knime_data(data)
        
        if not validation['is_valid']:
            return jsonify(create_error_response(
                'Batch data validation failed',
                400,
                details=validation
            )), 400
        
        logger.info(f"Batch validation passed: {validation['record_count']} records")
        
        # Create batch payload
        batch_payload = transform_knime_payload(data, 'knime_batch')
        batch_id = batch_payload['metadata']['batch_id']
        
        # Forward to Node-RED
        node_red_url = f"{app.config['NODE_RED_URL']}{app.config['NODE_RED_ENDPOINT']}"
        
        response = requests.post(
            node_red_url,
            json=batch_payload,
            headers={'Content-Type': 'application/json'},
            timeout=app.config['NODE_RED_TIMEOUT']
        )
        
        if response.status_code == 200:
            logger.info(f"Batch {batch_id} successfully processed")
            
            return jsonify(create_success_response(
                f'Batch {batch_id} processed successfully',
                data={
                    'batch_id': batch_id,
                    'records_processed': validation['record_count'],
                    'node_red_status': response.status_code
                },
                batch_metadata=batch_payload['metadata']
            )), 200
        else:
            logger.error(f"Batch {batch_id} failed with Node-RED status: {response.status_code}")
            return jsonify(create_error_response(
                f'Batch processing failed. Node-RED status: {response.status_code}',
                502
            )), 502
            
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}", exc_info=True)
        return jsonify(create_error_response(
            f'Batch processing failed: {str(e)}',
            500
        )), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get API status and statistics"""
    return jsonify({
        'status': 'operational',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'forward_to_nodered': 'active',
            'batch_process': 'active',
            'health': 'active'
        },
        'node_red': {
            'url': app.config['NODE_RED_URL'],
            'endpoint': app.config['NODE_RED_ENDPOINT'],
            'timeout': app.config['NODE_RED_TIMEOUT']
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify(create_error_response('Endpoint not found', 404)), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(create_error_response('Method not allowed', 405)), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(create_error_response('Internal server error', 500)), 500

if __name__ == '__main__':
    logger.info("Starting Flask API server...")
    logger.info(f"Node-RED URL: {app.config['NODE_RED_URL']}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG'],
        threaded=True
    )