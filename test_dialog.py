#!/usr/bin/env python3
"""
Test script to isolate the shortcut editor dialog issue
"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add the dahora_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from dahora_app.ui.shortcut_editor import ShortcutEditorDialog
from dahora_app.ui.styles import Windows11Style

def test_shortcut_editor():
    """Test the shortcut editor dialog"""
    
    def on_save(shortcut_data):
        print(f"Shortcut saved: {shortcut_data}")
        root.quit()
    
    def on_validate_hotkey(hotkey, exclude_id=None):
        print(f"Validating hotkey: {hotkey}")
        return True, "Valid"
    
    # Create main window
    root = tk.Tk()
    Windows11Style.configure_window(root, "Test Main Window", "400x300")
    Windows11Style.configure_styles(root)
    
    # Add a button to open the editor
    def open_editor():
        print("Opening shortcut editor...")
        try:
            editor = ShortcutEditorDialog(
                parent=root,
                shortcut=None,  # New shortcut
                on_save=on_save,
                on_validate_hotkey=on_validate_hotkey
            )
            print("Editor created, calling show()...")
            editor.show()
            print("Editor show() called successfully")
        except Exception as e:
            print(f"Error opening editor: {e}")
            import traceback
            traceback.print_exc()
    
    button = ttk.Button(root, text="Open Shortcut Editor", command=open_editor)
    button.pack(pady=50)
    
    print("Starting main window...")
    root.mainloop()

if __name__ == "__main__":
    test_shortcut_editor()