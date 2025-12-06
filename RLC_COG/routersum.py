#!/usr/bin/env python3
# coding=utf-8
#
# Permission is  hereby  granted,  free  of  charge,  to  any  person
# obtaining a copy of  this  software  and  associated  documentation
# files  (the  "Software"),  to  deal   in   the   Software   without
# restriction, including without limitation the rights to use,  copy,
# modify, merge, publish, distribute, sublicense, and/or sell  copies
# of the Software, and to permit persons  to  whom  the  Software  is
# furnished to do so.
#
# The above copyright notice and  this  permission  notice  shall  be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT  WARRANTY  OF  ANY  KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES  OF
# MERCHANTABILITY,   FITNESS   FOR   A   PARTICULAR    PURPOSE    AND
# NONINFRINGEMENT.  IN  NO  EVENT  SHALL  THE  AUTHORS  OR  COPYRIGHT
# OWNER(S) BE LIABLE FOR  ANY  CLAIM,  DAMAGES  OR  OTHER  LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING  FROM,
# OUT OF OR IN CONNECTION WITH THE  SOFTWARE  OR  THE  USE  OR  OTHER
# DEALINGS IN THE SOFTWARE.
#
######################################################################

import subprocess, threading, re, os, sys, inspect, shutil, argparse, random, math, json, fnmatch, requests
rows, columns = os.popen('stty size', 'r').read().split() #http://goo.gl/cD4CFf
#"pydoc -p 1234" will start a HTTP server on port 1234, allowing you  to  browse
#the documentation at "http://localhost:1234/" in your preferred Web browser.
cwf = os.path.abspath(inspect.getfile(inspect.currentframe())) # Current Working File
cwfd = os.path.dirname(cwf) # Current Working File Path

from openai import OpenAI

# Read the secret key from the file
with open("secret.key", "r") as f:
    secret_k = f.read().strip()
    client = OpenAI( base_url="https://openrouter.ai/api/v1",
        api_key=  f.read().strip(), )

def file2sum(file_path):
    # 1. Validate Input
    if not os.path.exists(file_path):
        return f"Error: File {file_path} not found."

    # 2. Load File Content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

    # 3. Load Config (for Model Name)
    # We look for cog_cfg.json in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cfg_path = os.path.join(script_dir, "cog_cfg.json")
    model_name = "gpt-oss-20b" # Default fallback
    
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r') as f:
                cfg = json.load(f)
                # navigate: projectConfig -> JuniorLLM
                model_name = cfg.get("projectConfig", {}).get("JuniorLLM", model_name)
        except:
            pass # keep default if config fails

    # 4. Prepare API Call
    requests_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {secret_k}",
        "Content-Type": "application/json"
    }

    # We ask the model to include reasoning and keep it short
    prompt = "Provide a markdown code escaped 111 chars or less summary of this file."

    payload = {
        "model": model_name,
        "include_reasoning": True, # Required for some models to output the 'reasoning' field
        "messages": [
          {
            "role": "system",
            "content": "role: you are a junior level engineer, preparing short summaries of files in a large project"
          },
          {
            "role": "user",
            "content": "in 111 chars or less summarize the following file:\n```\n#include<stdio.h>\n#include<math.h>\n\nint main() {\n    float a, b, c, determinant, r1, r2, real, imag;\n    printf(\"\\n\\nEnter coefficients a, b and c: \\n\\n\\n\");\n    scanf(\"%f%f%f\", &a, &b, &c);\n\n    determinant == b*b - 4*a*c; \n    if (determinant > 0) {\n        r1 = (-b + sqrt(determinant))/2*a;\n        r2 = (-b - sqrt(determinant))/2*a;\n        printf(\"\\n\\n\\nRoots are: %.2f and %.2f \", r1, r2);\n    } else if (determinant == 0) {  \n        r1 = r2 = -b/(2*a);\n        printf(\"\\n\\n\\nRoots are: %.2f and %.2f \", r1, r2);\n    } else {\n        real = -b/(2*a);\n        imag = sqrt(-determinant)/(2*a);\n        printf(\"\\n\\n\\nRoots are %.2f + i%.2f and %.2f - i%.2f \", real, imag, real, imag);\n    }\n    return 0;\n}\n```"
          },
          {
            "role": "assistant",
            "content": "summary:\n\n```C program to calculate and display real or complex roots of a quadratic equation using coefficients.```",
            "reasoning": "The user requested a concise summary of a C program. The program reads coefficients of a quadratic equation, computes the determinant, and based on its value, calculates and prints either two real roots, one repeated real root, or two complex roots. The assistant generated a short summary that captures this functionality within the character limit."
          },
            {"role": "user", "content": f"File: {os.path.basename(file_path)}\n\nContent:\n{code_content}\n\n{prompt}"}
        ]
    }

    # 5. Execute Request
    try:
        response = requests.post(requests_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"API Error: {str(e)}"

    # 6. Parse and Format Output
    try:
        # Extract the assistant's message
        message = data['choices'][0]['message']
        content = message.get('content', '').strip()
        
        # Extract reasoning (based on your log file structure)
        reasoning = message.get('reasoning', 'Analysis complete.')
        
        # Construct the simulated interaction string
        # Note: We escape the backticks for the output string
        output_str = (
            f"User: Please provide a markdown code escaped 111 chars or less summary of `{os.path.basename(file_path)}`.\n\n"
            f"Assistant:\n"
            f"<think>\n{reasoning}\n</think>\n\n"
            f"```\n{content}\n```"
        )
        return output_str

    except (KeyError, IndexError) as e:
        return f"Error parsing JSON response: {str(e)}"

print(file2sum(cwfd + "/RLC_COG.ui"))

