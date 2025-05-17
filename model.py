import os
from openai import OpenAI
from util import *


testCaseFormat = '[{"id": "TC001","description": "Description","precondition": "Precondition","steps": ["Step 1","Step 2","Step 3"],"expected_result": "Expected result"}]'
testScriptFormat = '[{"id": "TC001","script": "Script"},{"id": "TC002","script": "Script"}]'

testCasePrompt = """
Act as a QA tester.

From the given input, generate test cases focused only on API field-level validation.

Instructions:
- Include both positive and negative scenarios for each field.
- Each scenario must be its own test case.
- Return the result strictly in JSON format only. Do not include markdown, headers, or commentary.

Use the following JSON structure for the output:

""" + testCaseFormat

testScriptPrompt = """
Act as a QA tester.

Generate Python test scripts using the unittest module to validate field-level input rules for an API.

Instructions:
- Only generate tests for field validation (e.g. required fields, format, max length).
- Each positive or negative scenario must be its own unittest method.
- Each script must be independently executable.
- Assume HTTP status code 400 means validation failure.
- Map each script to its corresponding test case ID.
- Return output strictly in JSON format. Do not include markdown, headers, or explanations.

Use the following JSON structure for the output:

""" + testScriptFormat

def extractText(file):
    base64_images = pdf_to_images(file)
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    # Build content list: one text + multiple image_url entries
    content = [{"type": "text", "text": "Extract everything from the given images."}]
    for b64_img in base64_images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64_img}"
            }
        })

    completion = client.chat.completions.create(
        model="qwen-vl-max",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    print(completion.model_dump_json())
    return completion.choices[0].message.content

def createTestCase(text):
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen3-235b-a22b",
        messages=[{'role': 'system', 'content': testCasePrompt},
                  {'role': 'user', 'content': text}],
        extra_body={"enable_thinking": False},
        response_format={"type": "json_object"},
        )
    print(completion.model_dump_json())
    return completion.choices[0].message.content

def createTestScript(testCases, host, iddText):
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen3-235b-a22b",
        messages=[{'role': 'system', 'content': testScriptPrompt},
                  {'role': 'user', 'content': 'Test cases: ' + testCases + ' , IDD: ' + iddText + ' , host: ' + host}],
        extra_body={"enable_thinking": False},
        response_format={"type": "json_object"},
        )
    print(completion.model_dump_json())
    return completion.choices[0].message.content
