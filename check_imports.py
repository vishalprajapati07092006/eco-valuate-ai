import sys
import subprocess
import os

def trace_imports():
    # Capture imports before loading main app
    initial_modules = set(sys.modules.keys())
    
    print("--> Loading main app...")
    try:
        # Import your FastAPI app
        import main
    except Exception as e:
        print(f"Error importing main.py: {e}")
        return

    # Capture imports after loading main app
    final_modules = set(sys.modules.keys())
    loaded_modules = final_modules - initial_modules

    # Get root module names (e.g., 'transformers.models' -> 'transformers')
    root_loaded = {mod.split('.')[0] for mod in loaded_modules if not mod.startswith('_')}

    print("\n" + "="*40)
    print("PACKAGES ACTIVELY LOADED AT RUNTIME:")
    print("="*40)
    
    # Compare with requirements.txt if present
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            reqs = [line.strip().split("==")[0].split(">=")[0].lower() 
                    for line in f if line.strip() and not line.startswith("#")]

        print(f"\n[?] Checking against requirements.txt...\n")
        used = []
        unused = []
        
        for req in reqs:
            # Simple string matching for top-level packages
            clean_req = req.replace("-", "_")
            if any(clean_req in mod.lower() for mod in root_loaded):
                used.append(req)
            else:
                unused.append(req)

        print("✔ ACTIVELY USED IN CODE:")
        for u in used:
            print(f"  - {u}")

        print("\n❌ LIKELY UNUSED (Candidates for removal):")
        for un in unused:
            print(f"  - {un}")
    else:
        for mod in sorted(root_loaded):
            print(f"  - {mod}")

if __name__ == "__main__":
    trace_imports()