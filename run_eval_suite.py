#!/usr/bin/env python3
"""Runner that orchestrates FastAPI server and executes the full research test suite."""
import os
import sys
import time
import subprocess
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    print("=" * 80)
    print("STARTING INTEGRATED RESEARCH TEST RUNNER")
    print("=" * 80)

    # 1. Start server process
    server_cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    print("Launching FastAPI server on port 8000...")
    proc = subprocess.Popen(server_cmd, cwd=root_dir, env=env)

    try:
        # Wait up to 15s for server to start
        ready = False
        for i in range(30):
            try:
                r = requests.get("http://localhost:8000/", timeout=1.0)
                if r.status_code == 200:
                    ready = True
                    print(f"FastAPI Server ready in {(i+1)*0.5:.1f}s.")
                    break
            except Exception:
                time.sleep(0.5)

        if not ready:
            print("ERROR: FastAPI server failed to start within timeout.")
            return 1

        # 2. Run the full frontend-backend test suite
        import run_frontend_backend_research_test
        run_frontend_backend_research_test.main()
        return 0

    finally:
        print("\nStopping FastAPI background server...")
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        print("Server process terminated.")

if __name__ == "__main__":
    sys.exit(main())
