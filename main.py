from anthropic import Anthropic
from dotenv import load_dotenv
import os
import sys
import json
import subprocess

load_dotenv(override=True)

SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"), api_key=os.getenv("ANTHROPIC_API_KEY"))

TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]


def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"

def agent_loop(history: list):
    while True:
        # 1.model API with tools enabled
        response = client.messages.create(
            model=MODEL,
            system=SYSTEM,
            messages=history,
            max_tokens=8000,
            tools=TOOLS,
        )

        # print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))

        # 2.save model output into history
        outputs = []
        for block in response.content:
            if block.type == "text":
                outputs.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                outputs.append({"type": "tool_use", "id": block.id, "name": block.name, "input": block.input})

        history.append({"role": "assistant", "content": outputs})

        # 3.判断是否结束本轮对话，或需要继续执行工具，或直接输出文本结果
        if response.stop_reason == "end_turn":
            return "".join([b.text for b in response.content if b.type == "text"])

        # 4.工具调用和收集结果
        results = []
        for block in response.content:
            if block.type == "tool_use":
                cmd = block.input["command"]
                out = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300, cwd=os.getcwd())
                print(f"\033[33m$ {cmd}\033[0m")
                output = out.stdout + out.stderr
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})

        # 5.将工具结果加入对话历史，继续下一轮对话
        history.append({"role": "user", "content": results})


if __name__ == "__main__":
    MODEL = os.getenv("MODEL_ID")
    print(f"Model: {MODEL}")

    messages = []

    if len(sys.argv) > 1:
        messages.append({"role": "user", "content": sys.argv[1]})

        out = agent_loop(messages)

        print(out)


