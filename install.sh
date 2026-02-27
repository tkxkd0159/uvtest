#!/usr/bin/env bash
set -euo pipefail

APP_REPO="git+https://github.com/tkxkd0159/uvtest"
TOOL_ENV_NAME="uvtest"
UV_INSTALLED_NOW=0

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  UV_INSTALLED_NOW=1
fi

if [ "${UV_INSTALLED_NOW}" -eq 1 ]; then
  echo "Checking for uv (5 times, every 0.25s)..."
  for attempt in 1 2 3 4 5; do
    if command -v uv >/dev/null 2>&1; then
      break
    fi

    if [ -x "${HOME}/.local/bin/uv" ]; then
      export PATH="${HOME}/.local/bin:${PATH}"
    fi

    if command -v uv >/dev/null 2>&1; then
      break
    fi

    echo "uv not found yet (${attempt}/5)"
    sleep 0.25
  done
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Error: uv was not found after installation."
  echo "Open a new shell and run this script again, or add ~/.local/bin to PATH."
  exit 1
fi

echo "Installing app from ${APP_REPO}..."
uv tool install "${APP_REPO}"

TOOL_PYTHON="$(uv tool dir)/${TOOL_ENV_NAME}/bin/python"
if [ -x "${TOOL_PYTHON}" ]; then
  echo "Installing Playwright Chromium in tool virtual environment..."
  NODE_OPTIONS=--no-deprecation PLAYWRIGHT_BROWSERS_PATH=0 "${TOOL_PYTHON}" -m playwright install chromium
else
  echo "Warning: tool virtualenv python not found at ${TOOL_PYTHON}"
  echo "Skipping Chromium install."
fi

echo "Done."
