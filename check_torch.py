import sys
print(f"Python executable: {sys.executable}")
print("Checking for PyTorch...")
try:
    import torch
    print(f"PyTorch installed - version {torch.__version__}")
except ImportError:
    print("PyTorch is NOT installed")
