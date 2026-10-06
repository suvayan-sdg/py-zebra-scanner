# py-zebra-scanner

Emulates a Zebra barcode scanner using your webcam: reads QR codes via OpenCV + pyzbar,
then types the decoded value into whatever text field has focus (as if typed from a
hardware scanner), followed by Enter.

## Requirements

- Python 3.9+ (tested on 3.14)
- macOS, with a webcam
- [zbar](https://github.com/mchehab/zbar) native library (pyzbar is a Python wrapper around it)

## Setup

1. Install the native zbar library (macOS, via Homebrew):
   ```bash
   brew install zbar
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

```bash
python zebra_emulator.py
```

A window will open showing your webcam feed. When it detects a QR code, it waits 3
seconds (giving you time to click into the target text field), then types the decoded
value followed by Enter.

Press `q` in the camera window to quit.

### macOS permissions

The first time you run it, macOS will prompt for **Camera** access for your terminal
app (Terminal, iTerm, VS Code, etc.) — allow it. Keyboard typing also requires
**Accessibility** permission for the same app: go to
**System Settings → Privacy & Security → Accessibility** and enable it if typing
doesn't work.

## Notes

- Only QR codes are decoded (other barcode symbologies are disabled in code).
- Not currently tested on Windows/Linux — `pynput` keyboard emulation and camera
  backend selection (`cv2.CAP_AVFOUNDATION`) are macOS-specific in this version.
