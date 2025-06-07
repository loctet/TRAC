import io
import sys
from box import Box
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import tempfile
from Main import processfile as process_dafsm
from Visual_GraphVix import generate_visual_fsm
import json
import time

app = Flask(__name__)
CORS(app)

# Configure static file serving for WebExamples directory
@app.route('/WebExamples/<path:filename>')
def serve_web_example(filename):
    return send_from_directory('WebExamples', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    try:
        dafs_text = request.json.get('dafs_text')
        if not dafs_text:
            return jsonify({'error': 'No DAFS text provided'}), 400
        
        # Ensure WebExamples directory exists
        os.makedirs('WebExamples', exist_ok=True)
        os.makedirs('WebExamples/images', exist_ok=True)
        
        filename = os.path.join("WebExamples", f"{time.time_ns()}.dafsm")
        
        # Create a temporary file to store the DAFS text
        with open(filename, mode='w') as temp_file:
            temp_file.write(dafs_text)
            
        
        try:
            
            args = {
                "file_name": filename,
                "filetype": "dafsm",
                "non_stop": "1",
                "time_out": 0,
                "check_type": 1                
            }
            
            printed_output = ""
            # Process the DAFS text using the existing backend
            # === Start capturing stdout ===
            original_stdout = sys.stdout
            sys.stdout = io.StringIO()

            # Process the DAFSM
            trGrinder = process_dafsm(Box(args))

            # Capture all print output
            printed_output = sys.stdout.getvalue()

            # Restore stdout
            sys.stdout = original_stdout
            
            generate_visual_fsm(trGrinder.get_full_json_path(), trGrinder.get_full_png_path())
            
            json_transitons = ""
            with open(trGrinder.get_full_json_path()) as f: 
                json_transitons = f.read()
            
            trGrinder.delete_files()
            print(printed_output)
            # Return the relative URL path for the image
            return jsonify({
                'status': 'success',
                'printed_output': printed_output,
                'graph_data': trGrinder.get_full_png_path(),
                'json_transitions': str(json_transitons)
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    #app.run(debug=True, port=5000) 
    app.run(host="0.0.0.0", debug=True, port=5000)