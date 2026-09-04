"""Convenience launcher for the ZetaForge Google Colab notebook.

This can open the notebook and optionally attempt to use a local GUI keyboard
shortcut for Colab's Run all command. Google intentionally requires a user
interaction for arbitrary notebooks, so the GUI automation is best-effort and
never receives or embeds the ngrok token.
"""
import argparse
import time
import webbrowser

NOTEBOOK_URL = "https://colab.research.google.com/github/arjunparihar11/zeta-forge-ai/blob/main/Llama-3_1-Stheno_ZetaForge_Colab_Notebook.ipynb"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-all", action="store_true", help="After opening Colab, try Ctrl/Cmd+F9 via pyautogui.")
    parser.add_argument("--wait", type=float, default=8.0, help="Seconds to wait before the optional keypress.")
    args = parser.parse_args()
    webbrowser.open(NOTEBOOK_URL, new=2)
    print("Opened ZetaForge Colab notebook.")
    print("If Colab is not already connected, choose a GPU runtime and then run all cells.")
    if args.run_all:
        try:
            import pyautogui
        except ImportError:
            print("Optional automation unavailable: install pyautogui, then rerun with --run-all.")
            return
        time.sleep(args.wait)
        # Colab's Run all shortcut is Ctrl+F9 on Windows/Linux and Cmd+Option+F9 on macOS.
        try:
            import platform
            if platform.system() == "Darwin":
                pyautogui.hotkey("command", "option", "f9")
            else:
                pyautogui.hotkey("ctrl", "f9")
            print("Sent the Run all shortcut. Verify the Colab tab before relying on it.")
        except Exception as exc:
            print("Could not send Run all shortcut:", exc)


if __name__ == "__main__":
    main()
