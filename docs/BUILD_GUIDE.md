# 🛠️ Bionic Step-by-Step Build & Recreation Guide

This guide walks you through building the full Bionic agent harness and visual workspace from scratch.

---

## 1. System Components

1. **Frontend App (`web/`)**: React 19 + TailwindCSS + `@excalidraw/excalidraw` + `xterm.js` packaged via **Tauri v2**.
2. **Agent Core (`src/agent_core.py`)**: Python ReAct controller that executes file diffs, runs bash commands, and writes Excalidraw element JSON.
3. **Inference Engine (`src/mlx_inference_bridge.py`)**: Connects to Apple Silicon MLX server (`mlx_lm.server`) or `llama-server`.
4. **Voice Service (`src/voxtral_stt.py`)**: Offline speech-to-text dictation service.

---

## 2. Step-by-Step Setup

### Step A: Initialize Inference
```bash
# On macOS (Apple Silicon):
pip install mlx-lm
python -m mlx_lm.server --model mlx-community/Qwen2.5-Coder-32B-Instruct-4bit --port 1234

# On Linux (NVIDIA CUDA):
llama-server -m qwen2.5-coder-32b-instruct.Q4_K_M.gguf --port 1234 -c 32768 --n-gpu-layers 99
```

### Step B: Launch the ReAct Agent Loop
```bash
python src/agent_core.py --workspace . --model-endpoint http://localhost:1234/v1
```

### Step C: Launch the Visual Workspace
```bash
cd web
npm install
npm run dev
```

### Step D: Build Tauri Desktop Binary
```bash
npm run tauri build
```
Outputs native binaries for macOS (`.dmg` / `.app`), Linux (`.deb` / `.AppImage`), and Windows (`.msi`).

---

## 3. Netlify Deployment
To deploy the interactive web deliverable:
```bash
npx netlify-cli deploy --prod --dir .
```
