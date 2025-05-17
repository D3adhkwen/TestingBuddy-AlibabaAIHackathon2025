from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

@app.route('/api/fund-transfer', methods=['POST'])
def fund_transfer():
    try:
        data = request.get_json()

        # Extract and validate fields
        transfer = data.get("transfer", {})
        recipient = data.get("recipient", {})

        # Basic validations
        required_fields = ["type", "amount", "reference_id"]
        for field in required_fields:
            if not transfer.get(field):
                return error_response("MISSING_FIELD", f"Missing transfer.{field}")

        if transfer["type"] == "ibg" and not recipient.get("bank_code"):
            return error_response("MISSING_FIELD", "recipient.bank_code is required for IBG")

        if not recipient.get("account_number") or len(recipient["account_number"]) != 12:
            return error_response("INVALID_ACCOUNT", "Recipient account number is invalid")

        # Business logic stubs (can be expanded later)
        if transfer["amount"] <= 0:
            return error_response("INVALID_AMOUNT", "Transfer amount must be positive")

        effective_date = transfer.get("date", datetime.today().strftime('%Y-%m-%d'))

        # Simulate transaction ID
        transaction_id = f"TRX{uuid.uuid4().hex[:10].upper()}"

        return jsonify({
            "status": "success",
            "transaction_id": transaction_id,
            "message": "Transfer scheduled",
            "effective_date": effective_date
        })

    except Exception as e:
        return error_response("INTERNAL_ERROR", str(e))


def error_response(code, message):
    return jsonify({
        "status": "error",
        "code": code,
        "message": message
    }), 400


if __name__ == '__main__':
    app.run(debug=True)
