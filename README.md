# 🚀 Alibaba Cloud Malaysia AI Hackathon 2025

## 🧪 Testing Buddy

**Testing Buddy** is an AI-powered assistant designed to streamline the software testing process. Built for the Alibaba Cloud Malaysia AI Hackathon 2025, it focuses on generating and executing automated test scripts from input documentation with minimal human intervention.

---

## ✅ Current Features

- **Test Case Generation**
  - Accepts functional requirements and IDD documents
  - Extracts field-level validation rules
  - Automatically generates positive and negative test cases in JSON format

- **Test Script Generation**
  - Converts test cases into standalone Python `unittest` scripts
  - Maps each test case ID to its corresponding test method
  - Uses HTTP status codes (e.g., 400 for validation failure) as assertion basis

- **Test Execution**
  - Executes generated test scripts dynamically
  - Returns structured execution results and error logs via API

- **API Interface**
  - Flask-based backend with endpoints for:
    - `/generateTestScript` – generate Python test code
    - `/executeTestScript` – execute and return result of test code
    - `/api/fund-transfer` – sample test target endpoint

---

## 🌱 Future Enhancements

- **Smart Mapping & NLP Improvements**
  - Improve natural language understanding to support more complex IDDs
  - Automatically infer relationships between data fields and business rules

- **Front-End UI**
  - Develop a user-friendly web interface to upload documents, view generated scripts, and trigger executions

- **Test Coverage Analysis**
  - Integrate tools to visualize which parts of the API or data fields are tested

- **Database Integration**
  - Store test cases, results, and logs in a persistent store for audit and traceability

- **Multi-Framework Support**
  - Extend script generation to support Pytest, Postman/Newman, or Karate DSL

- **CI/CD Integration**
  - Hook into GitHub Actions or Jenkins for continuous validation

- **Security Testing**
  - Generate basic security and injection tests automatically based on input structure
