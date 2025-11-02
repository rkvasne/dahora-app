# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dahora App is a Windows system tray application that copies the current date and time to the clipboard in the format `[DD.MM.AAAA-HH:MM]`. Version 0.0.2. The application features an intuitive interface with toast notifications, single instance prevention, clipboard history, and follows modern Windows design patterns.

## Architecture

The application is built as a single Python script (`dahora_app.py`) with the following key components:

### Core Functionality
- **System Tray Integration**: Uses `pystray` to create a system tray icon with a custom-drawn clock design
- **Global Hotkey**: Implements global keyboard shortcuts using `keyboard` library (Ctrl+Shift+Q)
- **Clipboard Operations**: Uses `pyperclip` for clipboard management
- **Notifications**: 2-second Windows toast notifications that auto-dismiss
- **Clipboard History**: Maintains last 100 clipboard items with timestamp tracking
- **Usage Counter**: Tracks how many times the app has been triggered

### Key Functions
- `generate_datetime_string()`: Creates formatted datetime string
- `copy_datetime()`: Copies to clipboard and triggers notifications with source detection
- `show_toast_notification()`: Handles 2-second toast notifications with auto-dismiss
- `setup_icon()`: Creates system tray icon with menu structure including clipboard history
- `setup_hotkey_listener()`: Configures global hotkey in separate thread
- `check_single_instance()`: Prevents multiple instances with Windows mutex
- `show_about()`: Shows modal window with application information
- `monitor_clipboard()`: Monitors clipboard changes and adds to history
- `get_recent_clipboard_items()`: Returns recent items for menu integration

### Platform-Specific Features
- **Windows Integration**: Uses `win32api`, `win32con`, `win32event` for Windows-specific functionality
- **Single Instance Prevention**: Robust instance detection using Windows mutex with user notification
- **Notification Fallbacks**: Priority order: win32gui modal (About) → winotify toast → pystray notification → console output
- **Icon Generation**: Uses existing `icon.ico` file from project root with fallback creation if missing

## Build and Development Commands

### Installation and Setup
```bash
# Install dependencies (Windows)
./instalar.bat

# Manual installation
pip install -r requirements.txt
```

### Running the Application
```bash
# Run from source
python dahora_app.py

# Build executable
python build.py
```

### Development Dependencies
The project requires Python 3.8+ and the following packages:
- `pystray>=0.19.5` - System tray functionality
- `pyperclip>=1.8.2` - Clipboard operations
- `Pillow>=10.0.0` - Image generation for custom icon
- `keyboard>=0.13.5` - Global hotkeys
- `winotify>=0.15` - Windows toast notifications
- `pywin32>=306` - Windows API integration

## Build Configuration

The build process uses PyInstaller with a custom spec file (`dahora_app.spec`):

- **Build Script**: `build.py` - Automated build process with dependency checks
- **PyInstaller Config**: `dahora_app.spec` - Configuration for single-file executable
- **Output**: `dist/dahora_app.exe` - Standalone Windows executable

## Code Structure Notes

### Import Organization
- Conditional imports for Windows-specific modules with availability flags
- Graceful degradation when optional features are unavailable
- Thread management for non-blocking operations

### Error Handling
- Comprehensive try-catch blocks for all Windows API calls
- Multiple fallback mechanisms for notifications and UI feedback
- Single instance prevention with proper cleanup and mutex management

### Thread Management
- Hotkey listener runs in daemon thread
- Notifications spawn separate threads to avoid blocking
- Proper resource cleanup on application exit including mutex handle

## Application Behavior

The application runs in the system tray and responds to:

### Mouse Interactions
- **Left Click**: Shows instructions toast ("Menu de opções disponível")
- **Right Click**: Opens context menu with options
- **No Double Click Action**: Removed in current version (fallback to copy only)

### Menu Options
- **Copiar Data/Hora (Ctrl+Shift+Q)**: Copies current date/time with notification
- **--- Histórico Recente ---**: Direct menu items with recent 5 clipboard items (click to copy)
- **Limpar Histórico**: Clears clipboard history
- **Sobre**: Opens modal window with application information
- **Sair**: Exits the application

### Global Hotkey
- **Ctrl+Shift+Q**: Copies date/time from any application with notification

### Clipboard History
- Maintains last 100 clipboard items with timestamps
- Auto-monitors clipboard changes
- Shows recent 5 items in right-click menu
- Click menu items to copy from history
- Clear history option in menu

### Output Format
Always `[DD.MM.AAAA-HH:MM]` (e.g., `[25.12.2024-14:30]`)

### Message Sources
Notifications show source-specific messages:
- Menu items: "Menu: [item_text]"
- Hotkey: "Atalho"
- Fallback: "Fallback"

## Key Design Decisions

### Single Instance Prevention
- Uses global Windows mutex to prevent multiple instances
- Shows toast notification when attempting to run second instance
- Proper mutex cleanup on application exit

### Notification Strategy
- 2-second duration for quick feedback
- Modal window for "About" to allow user to read at their own pace
- Multiple fallback methods for different Windows environments

### User Interface
- Left click shows instructions (not copy action)
- Right click provides full menu access
- Hotkey provides fastest access
- Clear visual feedback for all actions