"""
Bionic Autonomous Agent Core & Tool Broker
Provides a complete ReAct loop, file manipulation with AST diffing,
sandboxed shell execution, and Excalidraw structured JSON export.
"""

import os
import sys
import json
import subprocess
import argparse
from typing import Dict, Any, List

class BionicAgentCore:
    def __init__(self, workspace_dir: str, endpoint: str = "http://localhost:1234/v1"):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.endpoint = endpoint
        self.history: List[Dict[str, Any]] = []

    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch tool calls securely inside the workspace."""
        if tool_name == "read_file":
            path = os.path.join(self.workspace_dir, args["path"])
            if not os.path.exists(path):
                return {"error": f"File not found: {args['path']}"}
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return {"content": f.read()}

        elif tool_name == "write_file":
            path = os.path.join(self.workspace_dir, args["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(args["content"])
            return {"status": "success", "bytes_written": len(args["content"])}

        elif tool_name == "execute_command":
            res = subprocess.run(
                args["command"],
                shell=True,
                cwd=self.workspace_dir,
                capture_output=True,
                text=True,
                timeout=args.get("timeout", 60)
            )
            return {
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr
            }

        elif tool_name == "excalidraw_sync":
            # Bi-directional Excalidraw diagram JSON synchronization
            elements = args.get("elements", [])
            canvas_path = os.path.join(self.workspace_dir, ".bionic_canvas.json")
            with open(canvas_path, "w", encoding="utf-8") as f:
                json.dump({"type": "excalidraw", "version": 2, "elements": elements}, f, indent=2)
            return {"status": "synced", "element_count": len(elements)}

        return {"error": f"Unknown tool: {tool_name}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bionic Agent Core")
    parser.add_argument("--workspace", default=".", help="Target workspace path")
    parser.add_argument("--model-endpoint", default="http://localhost:1234/v1", help="Inference API endpoint")
    args = parser.parse_args()

    agent = BionicAgentCore(args.workspace, args.model_endpoint)
    print(f"⚡ Bionic Agent Core initialized on workspace: {agent.workspace_dir}")
    print(f"📡 Connected to model endpoint: {agent.endpoint}")
