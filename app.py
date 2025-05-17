import subprocess
import uuid
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from model import *

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/generateTestCase", methods=['POST'])
def generateTestCase():
    requirementFile = request.files.get('requirementFile')
    text = extractText(requirementFile)
    return createTestCase(text)

@app.route("/generateTestScript", methods=['POST'])
def generateTestScript():
    testCases = request.form.get('testCases')
    print(testCases)
    host = request.form.get('host')
    iddText = extractText(request.files.get('iddFile'))
    return createTestScript(testCases, host, iddText)

@app.route("/executeTestScript", methods=["POST"])
def execute_test_script():
    code_string = request.data.decode("utf-8")

    # Generate a unique filename to avoid collisions
    filename = f"temp_script_{uuid.uuid4().hex}.py"
    filepath = os.path.join("/tmp", filename)

    # Save the code to a temporary Python file
    with open(filepath, "w") as file:
        file.write(code_string)

    # Execute the script and capture output and errors
    result = subprocess.run(
        ["python3", filepath],
        capture_output=True,
        text=True
    )

    # Clean up: remove the temporary script
    os.remove(filepath)

    # Return status and output
    return jsonify({
        "status": "success" if result.returncode == 0 else "failed",
        "stdout": result.stdout,
        "stderr": result.stderr
    }), 200
