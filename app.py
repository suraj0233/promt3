# app.py
from flask import Flask, render_template, request, jsonify
import subprocess
import os
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_integration', methods=['POST'])
def create_integration():
    account_id = request.form.get('account_id')
    
    if not account_id:
        return jsonify({'error': 'Account ID is required'}), 400
    
    try:
        # Create a temporary terraform.tfvars file
        with open('terraform.tfvars', 'w') as f:
            f.write(f'aws_account_id = "{account_id}"')
        
        # Initialize Terraform
        subprocess.run(['terraform', 'init'], check=True)
        
        # Plan the changes
        plan_result = subprocess.run(
            ['terraform', 'plan', '-out=tfplan'],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Apply the changes
        apply_result = subprocess.run(
            ['terraform', 'apply', 'tfplan'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return jsonify({
            'success': True,
            'message': f'Successfully created AWS integration for account {account_id}'
        })
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': f'Failed to create integration: {e.stderr}'
        }), 500
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
