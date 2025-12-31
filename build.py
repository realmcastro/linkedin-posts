"""
Build script for creating Windows executable
Run this script to create a standalone .exe file
Use --debug flag to create executable with console for debugging
"""

import os
import sys
import subprocess

def create_icon():
    """Create the icon file if it doesn't exist."""
    icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
    if not os.path.exists(icon_path):
        print("Creating icon...")
        try:
            subprocess.run([sys.executable, 'create_icon.py'], check=True)
        except subprocess.CalledProcessError:
            print("Warning: Could not create icon, proceeding without icon.")
            return None
    return icon_path

def build_exe(debug=False):
    """Build the executable using PyInstaller.
    
    Args:
        debug: If True, build with console window for debugging
    """
    
    # Create icon if needed
    icon_path = create_icon()
    icon_arg = f'--icon={icon_path}' if icon_path else '--icon=NONE'
    
    # PyInstaller command using python -m to ensure it works
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=NewsAPI_Automation_Debug' if debug else '--name=NewsAPI_Automation',
        '--console' if debug else '--windowed',  # Console for debug, windowed for release
        '--onefile',    # Single executable file
        icon_arg,
        '--add-data=.env;.',  # Embed .env file in the executable
        '--hidden-import=PIL._tkinter_finder',  # Required for PIL with Tkinter
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.scrolledtext',
        '--hidden-import=gui_app',
        '--hidden-import=gui_components',
        '--hidden-import=gui_styles',
        '--hidden-import=zai_classifier',
        '--hidden-import=image_generator',
        '--hidden-import=zai_prompts',
        '--hidden-import=tuning_search',
        '--hidden-import=config',
        'gui_app.py'
    ]
    
    print(f"Building executable ({'DEBUG MODE' if debug else 'RELEASE MODE'})...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True)
        print("\n" + "="*60)
        print("✓ Build successful!")
        print("="*60)
        exe_name = "NewsAPI_Automation_Debug.exe" if debug else "NewsAPI_Automation.exe"
        print(f"\nExecutable location: dist/{exe_name}")
        print("\nNote: Make sure .env file exists in the same directory as the .exe")
        print("      The images folder will be created automatically.")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    debug_mode = '--debug' in sys.argv
    build_exe(debug=debug_mode)
