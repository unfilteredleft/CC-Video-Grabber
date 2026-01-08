# 🐍 IMPORTS GALORE - All the modules we need to make this magic happen! 🪄
import os          # 💻 System operations (paths, folders, environment stuff)
import sys         # ⚙️ System-specific functions (EXE handling, paths)
import time        # ⏰ Time delays and timestamps for our log entries
import shutil      # 📦 File operations (cut/paste our precious videos)
import threading   # 🧵 Background tasks to keep UI smooth as butter 🧈
import winsound    # 🔊 Success jingles to celebrate our grabs! 🎉
import ctypes      # 🛠️ Low-level Windows API for unlocking stubborn files
import vlc         # 🎬 VLC media player integration for video preview
import tkinter as tk   # 🖼️ Standard GUI library for our beautiful interface
from tkinter import ttk, messagebox, simpledialog, filedialog  # UI components galore
from tkinter.scrolledtext import ScrolledText  # 📜 Scrolled text widget for help
from watchdog.observers import Observer   # 🕵️ Real-time folder monitoring superhero
from watchdog.events import FileSystemEventHandler  # Event handler for file changes
import logging       # 📝 Advanced logging for debugging (optional, but good practice)
from pathlib import Path   # 🛣️ Modern path handling (better than os.path in many ways)
import platform       # 🖥️ Platform detection for OS-specific features
import subprocess     # 🚀 Running external commands (like opening VLC installer)
import webbrowser     # 🌐 Opening web pages (help documentation)
import json          # 📋 JSON handling for settings persistence
from datetime import datetime  # 📅 Date/time operations for logging
import math          # 📐 Math operations for animations
import random        # 🎲 Random number generation

# --- 🚀 RUNTIME INITIALIZATION (For EXE Portability) ---
# This section ensures our bundled EXE can find all its pieces! 🧩
if getattr(sys, 'frozen', False):
    # 🎒 We're running as a PyInstaller EXE - need special path handling
    base_dir = sys._MEIPASS  # 📂 Temporary folder where EXE extracts itself
    os.environ['VLC_PLUGIN_PATH'] = os.path.join(base_dir, 'plugins')  # 🎬 Tell VLC where its plugins are
    if os.name == 'nt':  # 🪟 If we're on Windows...
        # Add our extraction folder to DLL search path (Python 3.10+ needs this!)
        os.add_dll_directory(base_dir)

# --- 🛡️ GLOBAL CONSTANTS - The backbone of our application! ---
APP_NAME = "CapCut Draft Grabber"
FILE_ATTRIBUTE_NORMAL = 0x80
ADMIN_REQUIRED = os.name == 'nt'
VERSION = "2.1.0"
SETTINGS_FILE = "settings.json"  # 📁 New settings file for persistence

# --- 🎵 ASCII SPLASH SCREEN & JINGLE SYSTEM ---
ASCII_LOGO = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ╔╗ ╔╗    ╔╗      ╔╗      ╔╗      ╔╗      ╔╗               ║
║    ║║ ║║    ║║      ║║      ║║      ║║      ║║               ║
║    ║║ ║║╔══╝║║╔╗╔╗╔╗║╚╗     ║║╔╗   ║║╔╗╔╗╔╗║║╔══╝══╗        ║
║    ║╚═╝║╔╗╔╗║║║║║║║║╔╗     ║║╠╝   ║║║║║║║║║╔╗╔╗║║╔╗╔╗═╝        ║
║    ║╗  ║║║╚╝║║║║║║║║║╚╝     ║║║    ║║║║║║║║║║║╚╝║║║╚╝║          ║
║    ╚╝  ╚╝╚══╝╚╝╚╝╚╝╚╝╚══╝     ╚╝╚═╗ ╚╝╚╝╚╝╚╝╚╝╚══╝╚╝╚══╝          ║
║                                   ╚╝                           ║
║                    Draft Grabber v2.1.0                        ║
║                                                              ║
║                     By Andy Benson 2025                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

class SoundManager:
    """Enhanced sound system for jingles and notifications."""
    
    def __init__(self):
        self.enabled = True
        self.volume = 1.0
        self.test_sound_system()
    
    def test_sound_system(self):
        """Test if sound is available."""
        try:
            winsound.Beep(1000, 50)
            self.enabled = True
            return True
        except:
            self.enabled = False
            return False
    
    def play_startup_jingle(self):
        """Play a dramatic startup jingle with ascending notes."""
        if not self.enabled:
            return
        
        try:
            # Dramatic startup sequence: C4 -> E4 -> G4 -> C5 (ascending arpeggio)
            notes = [
                (262, 150),  # C4 for 150ms
                (330, 150),  # E4 for 150ms  
                (392, 150),  # G4 for 150ms
                (523, 300)   # C5 for 300ms (grand finale!)
            ]
            
            for freq, duration in notes:
                winsound.Beep(freq, duration)
                time.sleep(50)  # Brief pause between notes
        except:
            pass  # Silent fail if sound issues
    
    def play_success_jingle(self):
        """Play success jingle when file is grabbed."""
        if not self.enabled:
            return
        
        try:
            # Victory fanfare: C6 -> E6 -> G6 -> C7 -> E7
            notes = [
                (1046, 100),  # C6
                (1319, 100),  # E6
                (1568, 100),  # G6
                (2093, 150),  # C7
                (2637, 200)   # E7 (climax!)
            ]
            
            for freq, duration in notes:
                winsound.Beep(freq, duration)
                time.sleep(30)
        except:
            pass
    
    def play_found_jingle(self):
        """Play jingle when file is found."""
        if not self.enabled:
            return
        
        try:
            # Discovery fanfare: Two quick rising notes
            winsound.Beep(880, 80)   # A5
            time.sleep(40)
            winsound.Beep(1175, 120) # D6
        except:
            pass
    
    def play_error_jingle(self):
        """Play error jingle."""
        if not self.enabled:
            return
        
        try:
            # Error sound: Descending notes
            winsound.Beep(400, 150)  # Low G4
            winsound.Beep(330, 150)  # E4
        except:
            pass

class SplashScreen:
    """ASCII splash screen with scrolling text."""
    
    def __init__(self, parent=None):
        self.parent = parent or tk.Tk()
        self.sound = SoundManager()
        self.window = None
        self.running = False
        
    def show_splash(self):
        """Show the splash screen with animation."""
        # Create splash window
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Toplevel()
        self.window.title("CapCut Draft Grabber - Starting...")
        self.window.geometry("60x15")  # Small initial size
        
        # Remove decorations
        if hasattr(self.window, 'overrideredirect'):
            self.window.overrideredirect(True)
        
        # Center on screen
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (200 // 2)
        self.window.geometry(f"600x200+{x}+{y}")
        
        # Create text widget for ASCII art
        self.text = tk.Text(self.window, bg='black', fg='lime', 
                           font=('Courier', 10), wrap=tk.NONE)
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # Insert logo
        self.text.insert('1.0', ASCII_LOGO)
        
        # Start animations
        self.running = True
        self.animate_text()
        
        # Play startup jingle
        self.sound.play_startup_jingle()
        
        # Auto-close after 5 seconds
        self.window.after(5000, self.close_splash)
        
        return self.window
    
    def animate_text(self):
        """Animate scrolling text in the logo."""
        if not self.running or not self.window.winfo_exists():
            return
        
        # Add scrolling banner effect
        scroll_text = "★ ★ ★ ★ ★   CAPCUT DRAFT GRABBER - ANDY BENSON 2025   ★ ★ ★ ★ ★"
        current_text = self.text.get('12.0', '13.0')
        
        # Create scrolling effect
        if current_text.strip():
            # Remove first character and add new one at end
            new_text = current_text[1:] + scroll_text[len(current_text)-1:]
        else:
            new_text = scroll_text[:60]  # Start with full text
        
        self.text.delete('12.0', '13.0')
        self.text.insert('12.0', new_text)
        
        # Schedule next animation frame
        if self.running:
            self.window.after(200, self.animate_text)
    
    def close_splash(self):
        """Close splash screen."""
        self.running = False
        if self.window and self.window.winfo_exists():
            self.window.destroy()

# --- 🎭 SOUND SYSTEM INITIALIZATION ---
SOUND_MANAGER = SoundManager()
SOUND_AVAILABLE = SOUND_MANAGER.enabled

# --- 🎬 VLC DETECTION & VALIDATION ---
def check_vlc_installation():
    """Check if VLC is installed and available."""
    try:
        instance = vlc.Instance('--no-xlib')
        instance.release()
        return True, "VLC is installed and ready!"
    except Exception as e:
        return False, str(e)

VLC_AVAILABLE, VLC_MESSAGE = check_vlc_installation()

# --- 📝 SETTINGS MANAGER - Better than config.txt! ---
class SettingsManager:
    """Manages application settings with JSON persistence."""
    
    DEFAULT_SETTINGS = {
        "monitor_folder": "C:\\Users\\edith\\Downloads\\__Capcut Drafts\\CapCut Drafts",
        "output_folder": "C:\\Users\\edith\\Downloads",
        "file_extension": ".mp4",
        "enable_sound": True,
        "enable_preview": True,
        "auto_start": False,
        "minimize_to_tray": False,
        "show_notifications": True,
        "retry_attempts": 100,
        "retry_delay": 100,  # milliseconds
        "log_file": "capcut_grabber.log",
        "enable_logging": True,
        "theme": "dark",  # dark or light
        "window_geometry": "800x650+100+100",
        "enable_startup_jingle": True,
        "enable_success_jingle": True,
        "enable_found_jingle": True,
        "enable_error_jingle": True,
        "jingle_volume": 1.0
    }
    
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file or create defaults."""
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                settings = self.DEFAULT_SETTINGS.copy()
                settings.update(loaded)
                return settings
            else:
                return self.DEFAULT_SETTINGS.copy()
        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to load settings:\n{e}")
            return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to JSON file."""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to save settings:\n{e}")
            return False
    
    def get(self, key, default=None):
        """Get setting value with optional default."""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value."""
        self.settings[key] = value
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?\nThis cannot be undone!"):
            self.settings = self.DEFAULT_SETTINGS.copy()
            self.save_settings()

# --- 🎵 SUCCESS JINGLE - Celebrate every successful grab! 🎊---
def play_success_jingle():
    """Enhanced success jingle with sound manager integration."""
    SOUND_MANAGER.play_success_jingle()

# --- 🎵 FILE FOUND JINGLE - When file is detected! ---
def play_found_jingle():
    """Play jingle when file is found."""
    SOUND_MANAGER.play_found_jingle()

# --- 🎵 ERROR JINGLE - When something goes wrong ---
def play_error_jingle():
    """Play error jingle."""
    SOUND_MANAGER.play_error_jingle()

# --- 🛠️ PERMISSION GUARD - The file unlocker superhero! 🦸‍♂️---
def check_admin_privileges():
    """Check if we're running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def force_unlocked_attributes(path):
    """Force file/folder attributes to 'Normal' to override CapCut's file locking."""
    try:
        ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_NORMAL)
    except Exception as e:
        print(f"Attribute unlock failed for {path}: {e}")

def attribute_guard_loop(monitor_path, stop_event, log_func=None):
    """Background thread that continuously unlocks files in monitor folder."""
    while not stop_event.is_set():
        if os.path.exists(monitor_path):
            try:
                for root, dirs, files in os.walk(monitor_path):
                    force_unlocked_attributes(root)
                    for d in dirs:
                        force_unlocked_attributes(os.path.join(root, d))
                    for f in files:
                        force_unlocked_attributes(os.path.join(root, f))
            except Exception as e:
                if log_func:
                    log_func(f"🔒 Attribute guard error: {e}")
        time.sleep(0.5)
    
    if log_func:
        log_func("🛡️ Attribute guard deactivated")

# --- 🎬 MEDIA PREVIEWER - Your personal video theater! 🎥---
class MediaPlayer:
    """Media player window using VLC for previewing grabbed videos."""
    def __init__(self, parent, file_path, auto_play=True):
        global VLC_AVAILABLE, VLC_MESSAGE
        if not VLC_AVAILABLE:
            messagebox.showerror("VLC Not Found", 
                f"VLC Media Player is not installed or working:\n{VLC_MESSAGE}\n\n"
                "🎬 Please install VLC from: https://videolan.org")
            return
        
        self.root = tk.Toplevel(parent)
        self.root.title(f"🎥 Preview: {os.path.basename(file_path)}")
        self.root.geometry("800x600")
        
        self.video_frame = tk.Frame(self.root, bg='black')
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        try:
            self.instance = vlc.Instance('--no-xlib')
            self.player = self.instance.media_player_new()
            self.player.set_hwnd(self.video_frame.winfo_id())
            
            self.media = self.instance.media_new(file_path)
            self.player.set_media(self.media)
            
            if auto_play:
                self.player.play()
                time.sleep(0.5)
                
        except Exception as e:
            messagebox.showerror("VLC Error", 
                f"Failed to load preview:\n{e}\n\n"
                "💡 Tip: Install VLC Media Player from videolan.org")
            self.root.destroy()

# --- 🕵️ MONITORING HANDLER - Our file system detective! 🕵️‍♀️---
class CapCutHandler(FileSystemEventHandler):
    """Enhanced file system event handler with comprehensive jingles."""
    def __init__(self, log_func, rename_func, output_folder, file_ext, enable_sound, retry_attempts=100, retry_delay=100):
        self.log_func = log_func
        self.rename_func = rename_func
        self.output_folder = output_folder
        self.file_ext = file_ext
        self.enable_sound = enable_sound
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay

    def on_created(self, event):
        """Called when a new file is created in the monitored folder."""
        if not event.is_directory and event.src_path.lower().endswith(self.file_ext):
            filename = os.path.basename(event.src_path)
            
            # Play found jingle when file is detected
            if self.enable_sound:
                play_found_jingle()
            
            self.log_func(f"🎯 New file detected: {filename}")
            self.log_msg(f"🎵 Playing found jingle...")
            self.safe_move(event.src_path)
    
    def log_msg(self, message):
        """Logging helper method."""
        self.log_func(message)
    
    def safe_move(self, src):
        """Enhanced file move with comprehensive jingles and logging."""
        filename = os.path.basename(src)
        dest = os.path.join(self.output_folder, filename)
        
        os.makedirs(self.output_folder, exist_ok=True)
        
        for i in range(1, self.retry_attempts + 1):
            try:
                force_unlocked_attributes(src)
                shutil.move(src, dest)
                
                # Log success with celebration
                self.log_func(f"✅ Successfully grabbed: {filename}")
                self.log_msg(f"🎉 SUCCESS! File moved to: {dest}")
                
                # Play success jingle
                if self.enable_sound:
                    play_success_jingle()
                    self.log_msg(f"🎵 Playing success jingle!")
                
                # Offer rename
                self.rename_func(dest)
                
                # Additional celebration log
                self.log_msg(f"🌟 MISSION ACCOMPLISHED! File '{filename}' safely secured!")
                return
                
            except Exception as e:
                if i < self.retry_attempts:
                    # Progress indicator for retries
                    if i % 10 == 0:  # Every 10 attempts
                        self.log_msg(f"⏳ Still trying... Attempt {i}/{self.retry_attempts}")
                    time.sleep(self.retry_delay / 1000)
                else:
                    # Final failure
                    self.log_msg(f"❌ Failed to grab {filename}: {e}")
                    if self.enable_sound:
                        play_error_jingle()
                        self.log_msg(f"🔔 Playing error jingle...")

# --- ⚙️ SETTINGS DIALOG - Enhanced with sound settings! ---
class SettingsDialog:
    """Enhanced settings dialog with sound configuration."""
    
    def __init__(self, parent, settings_manager, callback):
        self.parent = parent
        self.settings = settings_manager
        self.callback = callback
        
        self.root = tk.Toplevel(parent)
        self.root.title("⚙️ Settings")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        
        # Make dialog modal
        self.root.transient(parent)
        self.root.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the enhanced settings UI."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="📁 General")
        self.setup_general_tab(general_frame)
        
        # Features tab
        features_frame = ttk.Frame(notebook)
        notebook.add(features_frame, text="🌟 Features")
        self.setup_features_tab(features_frame)
        
        # Sound tab (NEW!)
        sound_frame = ttk.Frame(notebook)
        notebook.add(sound_frame, text="🔊 Sound")
        self.setup_sound_tab(sound_frame)
        
        # Advanced tab
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="🔧 Advanced")
        self.setup_advanced_tab(advanced_frame)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="💾 Save", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔄 Reset", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="❌ Cancel", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def setup_sound_tab(self, parent):
        """Setup sound settings tab."""
        row = 0
        
        # Enable sound
        self.enable_sound_var = tk.BooleanVar(value=self.settings.get("enable_sound", True))
        tk.Checkbutton(parent, text="🔊 Enable Sound System", 
                      variable=self.enable_sound_var,
                      command=self.toggle_sound_controls).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Startup jingle
        self.startup_jingle_var = tk.BooleanVar(value=self.settings.get("enable_startup_jingle", True))
        tk.Checkbutton(parent, text="🚀 Play Startup Jingle", 
                      variable=self.startup_jingle_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Success jingle
        self.success_jingle_var = tk.BooleanVar(value=self.settings.get("enable_success_jingle", True))
        tk.Checkbutton(parent, text="✅ Play Success Jingle", 
                      variable=self.success_jingle_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Found jingle
        self.found_jingle_var = tk.BooleanVar(value=self.settings.get("enable_found_jingle", True))
        tk.Checkbutton(parent, text="🎯 Play File Found Jingle", 
                      variable=self.found_jingle_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Error jingle
        self.error_jingle_var = tk.BooleanVar(value=self.settings.get("enable_error_jingle", True))
        tk.Checkbutton(parent, text="❌ Play Error Jingle", 
                      variable=self.error_jingle_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Jingle volume
        tk.Label(parent, text="🔊 Jingle Volume:").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        volume_frame = tk.Frame(parent)
        volume_frame.grid(row=row+1, column=0, sticky=tk.EW, padx=10, pady=5)
        
        self.volume_var = tk.DoubleVar(value=self.settings.get("jingle_volume", 1.0))
        volume_scale = tk.Scale(volume_frame, from_=0.0, to=1.0, resolution=0.1, 
                               orient=tk.HORIZONTAL, variable=self.volume_var)
        volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(volume_frame, text="🔊 Test", command=self.test_sound).pack(side=tk.RIGHT, padx=5)
        
        row += 3
        
        # Sound status
        self.sound_status_label = tk.Label(parent, text="🔊 Sound Status: Checking...", fg="blue")
        self.sound_status_label.grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        # Update sound status
        self.update_sound_status()
    
    def toggle_sound_controls(self):
        """Enable/disable sound controls based on main sound setting."""
        state = tk.NORMAL if self.enable_sound_var.get() else tk.DISABLED
        # You can enable/disable individual jingle settings here
    
    def test_sound(self):
        """Test sound with current settings."""
        try:
            # Test different jingles based on settings
            if self.success_jingle_var.get():
                play_success_jingle()
                self.root.after(1000, lambda: messagebox.showinfo("Sound Test", "✅ Success jingle played!"))
            elif self.found_jingle_var.get():
                play_found_jingle()
                self.root.after(1000, lambda: messagebox.showinfo("Sound Test", "🎯 Found jingle played!"))
            else:
                winsound.Beep(1000, 200)  # Simple test beep
                self.root.after(500, lambda: messagebox.showinfo("Sound Test", "🔊 Basic sound played!"))
        except Exception as e:
            messagebox.showerror("Sound Test", f"❌ Sound test failed: {e}")
    
    def update_sound_status(self):
        """Update sound status label."""
        if SOUND_AVAILABLE:
            self.sound_status_label.config(text="✅ Sound System: Working", fg="green")
        else:
            self.sound_status_label.config(text="❌ Sound System: Not Available", fg="red")
    
    def setup_general_tab(self, parent):
        """Setup general settings tab."""
        row = 0
        
        # Monitor folder
        tk.Label(parent, text="📂 Monitor Folder:").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        monitor_frame = tk.Frame(parent)
        monitor_frame.grid(row=row, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        
        self.monitor_var = tk.StringVar(value=self.settings.get("monitor_folder", ""))
        tk.Entry(monitor_frame, textvariable=self.monitor_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(monitor_frame, text="📁 Browse", command=self.browse_monitor).pack(side=tk.RIGHT, padx=5)
        
        row += 1
        
        # Output folder
        tk.Label(parent, text="📦 Output Folder:").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        output_frame = tk.Frame(parent)
        output_frame.grid(row=row, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=5)
        
        self.output_var = tk.StringVar(value=self.settings.get("output_folder", ""))
        tk.Entry(output_frame, textvariable=self.output_var, width=50).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(output_frame, text="📁 Browse", command=self.browse_output).pack(side=tk.RIGHT, padx=5)
        
        row += 1
        
        # File extension
        tk.Label(parent, text="🎥 File Extension:").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.extension_var = tk.StringVar(value=self.settings.get("file_extension", ".mp4"))
        tk.Entry(parent, textvariable=self.extension_var, width=20).grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
    
    def setup_features_tab(self, parent):
        """Setup features settings tab."""
        row = 0
        
        # Preview settings
        self.preview_var = tk.BooleanVar(value=self.settings.get("enable_preview", True))
        tk.Checkbutton(parent, text="🎬 Enable Video Preview", variable=self.preview_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Auto start
        self.autostart_var = tk.BooleanVar(value=self.settings.get("auto_start", False))
        tk.Checkbutton(parent, text="🚀 Auto-start monitoring on launch", variable=self.autostart_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Minimize to tray
        self.tray_var = tk.BooleanVar(value=self.settings.get("minimize_to_tray", False))
        tk.Checkbutton(parent, text="🔽 Minimize to system tray", variable=self.tray_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Show notifications
        self.notifications_var = tk.BooleanVar(value=self.settings.get("show_notifications", True))
        tk.Checkbutton(parent, text="🔔 Show system notifications", variable=self.notifications_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
    
    def setup_advanced_tab(self, parent):
        """Setup advanced settings tab."""
        row = 0
        
        # Retry attempts
        tk.Label(parent, text="🔄 Retry Attempts:").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.retry_attempts_var = tk.IntVar(value=self.settings.get("retry_attempts", 100))
        tk.Spinbox(parent, from_=1, to=1000, textvariable=self.retry_attempts_var, width=10).grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(parent, text="(How many times to try grabbing a file)").grid(row=row, column=2, sticky=tk.W, padx=5)
        
        row += 1
        
        # Retry delay
        tk.Label(parent, text="⏱️ Retry Delay (ms):").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.retry_delay_var = tk.IntVar(value=self.settings.get("retry_delay", 100))
        tk.Spinbox(parent, from_=10, to=5000, increment=10, textvariable=self.retry_delay_var, width=10).grid(row=row, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(parent, text="(Delay between retry attempts)").grid(row=row, column=2, sticky=tk.W, padx=5)
        
        row += 1
        
        # Enable logging
        self.logging_var = tk.BooleanVar(value=self.settings.get("enable_logging", True))
        tk.Checkbutton(parent, text="📝 Enable file logging", variable=self.logging_var).grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        
        row += 1
        
        # Theme
        tk.Label(parent, text="🎨 Theme:").grid(row=row, column=0, sticky=tk.W, padx=10, pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "dark"))
        theme_frame = tk.Frame(parent)
        theme_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, padx=10, pady=5)
        
        tk.Radiobutton(theme_frame, text="🌙 Dark", variable=self.theme_var, value="dark").pack(side=tk.LEFT)
        tk.Radiobutton(theme_frame, text="☀️ Light", variable=self.theme_var, value="light").pack(side=tk.LEFT, padx=10)
    
    def browse_monitor(self):
        """Browse for monitor folder."""
        folder = filedialog.askdirectory(initialdir=self.monitor_var.get())
        if folder:
            self.monitor_var.set(folder)
    
    def browse_output(self):
        """Browse for output folder."""
        folder = filedialog.askdirectory(initialdir=self.output_var.get())
        if folder:
            self.output_var.set(folder)
    
    def save_settings(self):
        """Save settings and close dialog."""
        # Update all settings
        self.settings.set("monitor_folder", self.monitor_var.get())
        self.settings.set("output_folder", self.output_var.get())
        self.settings.set("file_extension", self.extension_var.get())
        self.settings.set("enable_sound", self.enable_sound_var.get())
        self.settings.set("enable_preview", self.preview_var.get())
        self.settings.set("auto_start", self.autostart_var.get())
        self.settings.set("minimize_to_tray", self.tray_var.get())
        self.settings.set("show_notifications", self.notifications_var.get())
        self.settings.set("retry_attempts", self.retry_attempts_var.get())
        self.settings.set("retry_delay", self.retry_delay_var.get())
        self.settings.set("enable_logging", self.logging_var.get())
        self.settings.set("theme", self.theme_var.get())
        
        # Sound settings
        self.settings.set("enable_startup_jingle", self.startup_jingle_var.get())
        self.settings.set("enable_success_jingle", self.success_jingle_var.get())
        self.settings.set("enable_found_jingle", self.found_jingle_var.get())
        self.settings.set("enable_error_jingle", self.error_jingle_var.get())
        self.settings.set("jingle_volume", self.volume_var.get())
        
        # Save to file
        if self.settings.save_settings():
            messagebox.showinfo("Settings", "✅ Settings saved successfully!")
            if self.callback:
                self.callback()
            self.root.destroy()
    
    def reset_settings(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?\nThis cannot be undone!"):
            self.settings.reset_to_defaults()
            messagebox.showinfo("Settings", "✅ Settings reset to defaults!")

# --- 📖 HELP DIALOG - Enhanced with sound help! ---
class HelpDialog:
    """Help dialog with comprehensive documentation."""
    
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent)
        self.root.title("📖 Help & Documentation")
        self.root.geometry("800x600")
        
        # Make dialog modal
        self.root.transient(parent)
        self.root.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the help UI."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Getting Started tab
        getting_started = ScrolledText(notebook, wrap=tk.WORD, width=80, height=30)
        notebook.add(getting_started, text="🚀 Getting Started")
        
        getting_started.insert(tk.END, """
🚀 GETTING STARTED WITH CAPCUT DRAFT GRABBER

WELCOME TO CAPCUT DRAFT GRABBER! 🎬

This tool automatically grabs temporary exported MP4 files from CapCut before they're deleted. Here's how to get started:

📋 STEP-BY-STEP SETUP:
1️⃣ Install Python 3.7+ from python.org
2️⃣ Install VLC Media Player from videolan.org (optional but recommended)
3️⃣ Run the application (python main.py)
4️⃣ Configure your folders:
   • Monitor folder: Where CapCut saves exports
   • Output folder: Where to save grabbed videos
5️⃣ Click "Start Monitoring" and begin grabbing!

💡 PRO TIPS:
• Run as Administrator for best results
• Enable sound for audio feedback
• Use video preview to verify grabs
• Test your setup with the Test button

🎵 SOUND FEATURES:
• Startup jingle plays when application starts
• Found jingle plays when new file is detected
• Success jingle plays when file is successfully grabbed
• Error jingle plays when something goes wrong
• Customize all jingles in Settings > Sound

🎯 HOW IT WORKS:
1. CapCut creates temporary export folders
2. Our app detects new MP4 files immediately
3. Found jingle plays when file is detected
4. Files are moved to your output folder
5. Success jingle plays and you get notified
6. You can rename the file and preview with VLC

🔧 TROUBLESHOOTING:
• No sound? Check audio settings and sound volume
• No files grabbed? Check monitor folder path
• Permission errors? Run as Administrator
• VLC issues? Install VLC from videolan.org

📞 GETTING HELP:
• Use the Test button to diagnose issues
• Check the log for error messages
• Visit GitHub for support and updates
• Check Settings > Sound for audio configuration
        """)
        getting_started.config(state=tk.DISABLED)
        
        # Features tab
        features = ScrolledText(notebook, wrap=tk.WORD, width=80, height=30)
        notebook.add(features, text="🌟 Features")
        
        features.insert(tk.END, """
🌟 FEATURES OVERVIEW

🔍 REAL-TIME MONITORING
• Watchdog-based folder monitoring
• Instant file detection (sub-second)
• Recursive folder searching
• Support for multiple file types

🎬 VIDEO PREVIEW
• VLC Media Player integration
• Quick preview of grabbed videos
• Full-screen viewing option
• Playback controls included

🎵 SOUND NOTIFICATIONS (NEW!)
• Startup jingle with dramatic fanfare
• Found jingle when files are detected
• Success jingle for completed grabs
• Error jingle for troubleshooting
• Customizable volume and settings

🛡️ FILE UNLOCKING
• Background attribute guard
• Handles locked CapCut files
• Administrator privilege support
• Automatic retry mechanism

⚙️ CUSTOMIZATION OPTIONS
• Adjustable retry settings
• Custom file extensions
• Multiple output formats
• Theme selection (dark/light)
• Comprehensive sound controls

📝 LOGGING & DEBUGGING
• Comprehensive activity log
• Timestamped entries
• Error reporting
• Sound event logging
• Exportable log files

🎮 USER INTERFACE
• Modern, intuitive design
• Real-time status indicators
• Responsive controls
• System tray support (optional)
• ASCII splash screen on startup

🔄 AUTOMATION
• Auto-start on launch
• Automatic folder creation
• Silent operation mode
• Background processing
• Sound-enabled automation

📊 STATUS MONITORING
• System status indicators
• Performance metrics
• File grab statistics
• Real-time feedback
• Sound system monitoring

🔧 ADVANCED SETTINGS
• Detailed configuration options
• Backup and restore settings
• Import/export preferences
• Customizable behavior
• Sound customization

💾 DATA MANAGEMENT
• Persistent settings storage
• Configuration backup
• Settings reset option
• JSON-based configuration
• Sound settings persistence

🎨 AUDIO EXPERIENCE
• Professional jingles for all events
• Volume control and testing
• Individual jingle toggles
• Sound system diagnostics
• Audio feedback integration

🌐 INTEGRATION
• Windows shell integration
• External app launching
• URL scheme support
• Sound system integration
- Plugin architecture (future)
        """)
        features.config(state=tk.DISABLED)
        
        # Sound Help tab (NEW!)
        sound_help = ScrolledText(notebook, wrap=tk.WORD, width=80, height=30)
        notebook.add(sound_help, text="🎵 Sound Guide")
        
        sound_help.insert(tk.END, """
🎵 SOUND SYSTEM GUIDE

🔊 SOUND OVERVIEW:
The CapCut Draft Grabber features a comprehensive sound system with jingles for every important event. This enhances the user experience and provides immediate audio feedback for all operations.

🎵 JINGLE TYPES:

1️⃣ STARTUP JINGLE 🚀
• Plays when application starts
• Dramatic ascending arpeggio: C4 -> E4 -> G4 -> C5
• Duration: ~650ms
• Purpose: Welcome and confirm successful startup
• Can be disabled in Settings > Sound

2️⃣ FOUND JINGLE 🎯
• Plays when new MP4 file is detected
• Quick two-note rising pattern: A5 -> D6
• Duration: ~240ms
• Purpose: Alert user that file has been found
• Indicates successful file detection

3️⃣ SUCCESS JINGLE ✅
• Plays when file is successfully grabbed and moved
• Victory fanfare: C6 -> E6 -> G6 -> C7 -> E7
• Duration: ~580ms
• Purpose: Celebrate successful file operation
• Confirms mission accomplished

4️⃣ ERROR JINGLE ❌
• Plays when operations fail
• Descending notes: Low G4 -> E4
• Duration: ~300ms
• Purpose: Alert user to problems
• Helps with troubleshooting

⚙️ SOUND SETTINGS:
Location: Settings > Sound tab

• Enable Sound System: Master toggle for all audio
• Play Startup Jingle: Control startup sound
• Play Success Jingle: Control success sound
• Play File Found Jingle: Control detection sound
• Play Error Jingle: Control error notification
• Jingle Volume: Adjust overall volume (0.0 - 1.0)

🔧 TROUBLESHOOTING SOUND ISSUES:

NO SOUND AT ALL:
• Check Windows volume settings
• Ensure speakers/headphones are connected
• Verify "Enable Sound System" is checked
• Test with the Test button in Sound settings

JINNLE PLAYS BUT WRONG VOLUME:
• Adjust "Jingle Volume" slider in Settings
• Check Windows application volume
• Verify system master volume

SOUND CUTS OFF OR DISTORTED:
• Check speaker connections
• Reduce system volume if too high
• Test with different audio devices

SOME JINGLES WORK, OTHERS DON'T:
• Check individual jingle toggles in Settings
• Verify all desired jingles are enabled
• Use Test button to verify each jingle type

🎵 COMPOSITION NOTES:
All jingles were carefully composed to be:
• Pleasant and not annoying
• Distinct from each other
• Quick and informative
• Professional in tone

🎛️ ADVANCED SOUND CONFIGURATION:
• Master volume control for all jingles
• Individual jingle enable/disable toggles
• Sound system diagnostics
• Real-time sound status monitoring

🔊 TECHNICAL DETAILS:
• Uses Windows winsound API
• Frequency range: 262Hz to 2637Hz
• Duration range: 80ms to 300ms per note
• Supports up to 5-note sequences
• Real-time sound system checking

💡 PRO TIPS:
• Keep volume at moderate level for comfort
• Test different jingle combinations
• Use found jingle to monitor activity remotely
• Success jingle confirms when you can look away
• Error jingle alerts when attention needed

🎨 AUDIO DESIGN PHILOSOPHY:
- Each jingle serves a specific purpose
- Sound patterns are intuitive and memorable
- Audio feedback enhances user experience
- Professional yet approachable sound design
- Non-intrusive but informative notifications

🎵 FUTURE SOUND ENHANCEMENTS:
- Custom jingle upload support (planned)
- Different musical themes (coming soon)
- Voice notification options (in development)
- Integration with system sound schemes
- Audio waveform visualization
        """)
        sound_help.config(state=tk.DISABLED)
        
        # FAQ tab
        faq = ScrolledText(notebook, wrap=tk.WORD, width=80, height=30)
        notebook.add(faq, text="❓ FAQ")
        
        faq.insert(tk.END, """
❓ FREQUENTLY ASKED QUESTIONS

Q: Why isn't my file being grabbed?
A: Check that the monitor folder path is correct, ensure files have the .mp4 extension, and verify folder permissions. Also listen for the found jingle to confirm detection.

Q: VLC preview doesn't work?
A: Install VLC Media Player from videolan.org and restart the application.

Q: Sound notifications not playing?
A: Check Windows audio settings, ensure speakers are connected and not muted. Verify sound is enabled in Settings > Sound and test with the Test button.

Q: Permission denied errors?
A: Run the application as Administrator for better file access.

Q: How do I monitor multiple folders?
A: Run multiple instances of the application, each with different monitor folders.

Q: What are the different jingles for?
A: 
• Startup jingle: Application successfully started
• Found jingle: New MP4 file detected
• Success jingle: File successfully grabbed
• Error jingle: Operation failed

Q: Can I customize the jingles?
A: You can enable/disable individual jingles and adjust volume in Settings > Sound. Custom jingle upload coming in future updates.

Q: Can I change the file extension?
A: Yes, in Settings > General, change the file extension to match your needs.

Q: How many retry attempts are normal?
A: Default is 100 attempts over 10 seconds, usually sufficient for most systems.

Q: Does this work with other video editors?
A: It's designed for CapCut but may work with similar applications that use temporary export folders.

Q: Is my data safe?
A: Yes, the app only moves files, never modifies or deletes them. All processing is local.

Q: Can I disable all sounds?
A: Yes, uncheck "Enable Sound System" in Settings > Sound to disable all jingles.

Q: How do I backup my settings?
A: Copy settings.json file to backup your preferences, including sound settings.

Q: What's the difference between .mp4 and other formats?
A: .mp4 is the standard video format CapCut uses. Other formats may work but aren't officially supported.

Q: Can I use this on macOS/Linux?
A: Currently Windows-only due to Windows-specific file locking features.

Q: How much CPU does this use?
A: Very little - background monitoring uses minimal resources.

Q: Can I help with development?
A: Yes! Visit the GitHub repository to contribute or report issues.

Q: Where are grabbed files stored?
A: In your configured output folder, which you set in Settings or on the main interface.

Q: How do I report bugs?
A: Create an issue on GitHub with detailed information about the problem.

Q: Is this really free?
A: Yes! It's open-source under the MIT license - completely free forever.

Q: Why does the startup jingle play every time?
A: The startup jingle confirms the application started successfully. You can disable it in Settings > Sound if you prefer.
        """)
        faq.config(state=tk.DISABLED)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(nav_frame, text="🌐 GitHub", command=self.open_github).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="📧 Report Issue", command=self.report_issue).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="✅ Check Updates", command=self.check_updates).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="❌ Close", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
    
    def open_github(self):
        """Open GitHub repository in browser."""
        webbrowser.open("https://github.com/yourusername/capcut-grabber")
    
    def report_issue(self):
        """Open GitHub issues page."""
        webbrowser.open("https://github.com/yourusername/capcut-grabber/issues")
    
    def check_updates(self):
        """Check for application updates."""
        messagebox.showinfo("Updates", "🎉 You're running the latest version!\n\nCurrent version: " + VERSION)

# --- 🚀 MAIN APPLICATION - Enhanced with sound system! ---
class CapCutGrabberApp:
    """Main application class for CapCut Grabber."""
    
    def __init__(self, root):
        """Initialize the main application with splash screen."""
        self.root = root
        self.root.title(f"{APP_NAME} v{VERSION}")
        self.root.geometry("800x650")
        
        # Show splash screen first
        self.show_splash_screen()
        
        # Initialize settings manager
        self.settings = SettingsManager()
        
        # Initialize sound system
        self.init_sound_system()
        
        # Initialize variables
        self.observer = None
        self.attribute_stop = threading.Event()
        self.attribute_thread = None
        self.is_monitoring = False
        
        # Setup menu
        self.setup_menu()
        
        # Setup UI (after splash)
        self.setup_ui()
        
        # Show initial status
        self.show_initial_tips()
        
        # Auto-start if enabled
        if self.settings.get("auto_start", False):
            self.root.after(2000, self.start_monitoring)
    
    def show_splash_screen(self):
        """Show ASCII splash screen with animations."""
        splash = SplashScreen(self.root)
        splash_window = splash.show_splash()
        
        # Wait for splash to complete
        self.root.update()
        time.sleep(5.5)  # Wait for splash duration
        
        if splash_window.winfo_exists():
            splash_window.destroy()
    
    def init_sound_system(self):
        """Initialize the enhanced sound system."""
        self.sound_manager = SOUND_MANAGER
        self.enable_sound = self.settings.get("enable_sound", True)
    
    def setup_menu(self):
        """Setup the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="🎬 Test Setup", command=self.test_setup, accelerator="Ctrl+T")
        file_menu.add_separator()
        file_menu.add_command(label="📦 Open Output Folder", command=self.open_output_folder, accelerator="Ctrl+D")
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Exit", command=self.safe_exit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="✏️ Edit", menu=edit_menu)
        edit_menu.add_command(label="⚙️ Settings", command=self.open_settings, accelerator="Ctrl+,")
        edit_menu.add_separator()
        edit_menu.add_command(label="🧹 Clear Log", command=self.clear_log, accelerator="Ctrl+L")
        edit_menu.add_command(label="📋 Copy Log", command=self.copy_log)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="👁️ View", menu=view_menu)
        view_menu.add_checkbutton(label="🔔 Show Notifications", variable=tk.BooleanVar(value=self.settings.get("show_notifications", True)))
        view_menu.add_checkbutton(label="🌙 Dark Theme", variable=tk.BooleanVar(value=self.settings.get("theme", "dark") == "dark"))
        view_menu.add_separator()
        view_menu.add_command(label="📊 Statistics", command=self.show_statistics)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Tools", menu=tools_menu)
        tools_menu.add_command(label="🛡️ Admin Check", command=self.check_admin)
        tools_menu.add_command(label="🎬 VLC Status", command=self.check_vlc)
        tools_menu.add_command(label="🔊 Sound Test", command=self.test_sound_system)
        tools_menu.add_separator()
        tools_menu.add_command(label="📁 Reset Settings", command=self.reset_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📖 Help", menu=help_menu)
        help_menu.add_command(label="📖 Documentation", command=self.open_help, accelerator="Ctrl+H")
        help_menu.add_command(label="⌨️ Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="🎵 Sound Guide", command=self.open_sound_help)
        help_menu.add_separator()
        help_menu.add_command(label="🌐 Visit Website", command=self.open_website)
        help_menu.add_command(label="📧 Report Bug", command=self.report_bug)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-t>', lambda e: self.test_setup())
        self.root.bind('<Control- comma>', lambda e: self.open_settings())
        self.root.bind('<Control-h>', lambda e: self.open_help())
        self.root.bind('<Control-l>', lambda e: self.clear_log())
        self.root.bind('<Control-d>', lambda e: self.open_output_folder())
        self.root.bind('<Control-q>', lambda e: self.safe_exit())
        self.root.bind('<F5>', lambda e: self.refresh_status())
    
    def setup_ui(self):
        """Build the GUI."""
        # Title frame
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=f"🔥 {APP_NAME} v{VERSION} 🔥", 
                font=("Impact", 28), fg="white", bg="#2c3e50").pack(expand=True)
        
        # Status indicators with sound status
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=20, pady=5)
        
        sound_status = "🔊 On" if SOUND_AVAILABLE else "🔇 Off"
        sound_color = "green" if SOUND_AVAILABLE else "red"
        tk.Label(status_frame, text=f"Sound: {sound_status}", fg=sound_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        
        vlc_status = "🎬 Ready" if VLC_AVAILABLE else "🎬 Missing"
        vlc_color = "green" if VLC_AVAILABLE else "red"
        tk.Label(status_frame, text=f"VLC: {vlc_status}", fg=vlc_color, font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        
        admin_status = "🛡️ Admin" if check_admin_privileges() else "👤 User"
        tk.Label(status_frame, text=f"Mode: {admin_status}", font=("Arial", 9)).pack(side=tk.LEFT, padx=10)
        
        # Monitor folder section
        tk.Label(self.root, text="📂 Monitor Folder:", font=("Arial", 10, "bold")).pack()
        monitor_frame = tk.Frame(self.root)
        monitor_frame.pack(pady=5, fill=tk.X, padx=20)
        
        self.monitor_var = tk.StringVar(value=self.settings.get("monitor_folder", ""))
        monitor_entry = tk.Entry(monitor_frame, textvariable=self.monitor_var, width=60)
        monitor_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(monitor_frame, text="📁 Browse", command=self.browse_monitor).pack(side=tk.RIGHT, padx=5)
        
        # Output folder section
        tk.Label(self.root, text="📦 Output Folder:", font=("Arial", 10, "bold")).pack()
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=5, fill=tk.X, padx=20)
        
        self.output_var = tk.StringVar(value=self.settings.get("output_folder", ""))
        output_entry = tk.Entry(output_frame, textvariable=self.output_var, width=60)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(output_frame, text="📁 Browse", command=self.browse_output).pack(side=tk.RIGHT, padx=5)
        
        # Settings frame with sound options
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)
        
        self.sound_var = tk.BooleanVar(value=self.settings.get("enable_sound", True))
        tk.Checkbutton(settings_frame, text="🔊 Enable Sound", variable=self.sound_var).pack(side=tk.LEFT, padx=10)
        
        self.preview_var = tk.BooleanVar(value=self.settings.get("enable_preview", True))
        tk.Checkbutton(settings_frame, text="🎬 Enable Video Preview", variable=self.preview_var).pack(side=tk.LEFT, padx=10)
        
        tk.Button(settings_frame, text="🎵 Sound Settings", command=self.open_sound_settings).pack(side=tk.LEFT, padx=10)
        
        # Log section
        tk.Label(self.root, text="📝 Activity Log:", font=("Arial", 10, "bold")).pack()
        
        self.log = tk.Text(self.root, height=12, width=85, bg="#1a1a1a", fg="#00FF00", font=("Consolas", 9))
        self.log.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.start_btn = tk.Button(button_frame, text="▶️ Start Monitoring", 
                                  bg="green", fg="white", font=("Arial", 12, "bold"),
                                  command=self.start_monitoring)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="⏹️ Stop", 
                                 bg="red", fg="white", font=("Arial", 12, "bold"),
                                 command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🔧 Test", command=self.test_setup).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🔊 Test Sound", command=self.test_sound_system).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="⚙️ Settings", command=self.open_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📖 Help", command=self.open_help).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🚪 Exit", command=self.safe_exit).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to grab some videos! 🎬")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, bg="#34495e", fg="white")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def test_sound_system(self):
        """Test the sound system with user choice."""
        if not SOUND_AVAILABLE:
            messagebox.showwarning("Sound Test", "❌ Sound system not available on this computer")
            return
        
        # Create test dialog
        test_window = tk.Toplevel(self.root)
        test_window.title("🔊 Sound System Test")
        test_window.geometry("400x300")
        test_window.transient(self.root)
        test_window.grab_set()
        
        tk.Label(test_window, text="🎵 Sound System Test", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(test_window, text="Choose which jingle to test:").pack(pady=10)
        
        def test_startup():
            SOUND_MANAGER.play_startup_jingle()
            self.log_msg("🎵 Played startup jingle")
        
        def test_found():
            SOUND_MANAGER.play_found_jingle()
            self.log_msg("🎵 Played found jingle")
        
        def test_success():
            SOUND_MANAGER.play_success_jingle()
            self.log_msg("🎵 Played success jingle")
        
        def test_error():
            SOUND_MANAGER.play_error_jingle()
            self.log_msg("🎵 Played error jingle")
        
        button_frame = tk.Frame(test_window)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🚀 Startup", command=test_startup, width=12).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="🎯 Found", command=test_found, width=12).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="✅ Success", command=test_success, width=12).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="❌ Error", command=test_error, width=12).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(test_window, text="Close", command=test_window.destroy).pack(pady=10)
    
    def browse_monitor(self):
        """Browse for monitor folder."""
        folder = filedialog.askdirectory(initialdir=self.monitor_var.get())
        if folder:
            self.monitor_var.set(folder)
    
    def browse_output(self):
        """Browse for output folder."""
        folder = filedialog.askdirectory(initialdir=self.output_var.get())
        if folder:
            self.output_var.set(folder)
    
    def clear_log(self):
        """Clear the activity log."""
        self.log.delete(1.0, tk.END)
        self.log_msg("📝 Log cleared")
    
    def copy_log(self):
        """Copy log contents to clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.log.get(1.0, tk.END))
            self.log_msg("📋 Log copied to clipboard")
        except Exception as e:
            self.log_msg(f"❌ Failed to copy log: {e}")
    
    def log_msg(self, message):
        """Add timestamped message to log."""
        ts = time.strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{ts}] {message}\n")
        self.log.see(tk.END)
        self.root.update_idletasks()
    
    def show_initial_tips(self):
        """Show initial status and tips."""
        tips = []
        
        if not SOUND_AVAILABLE and self.sound_var.get():
            tips.append("🔊 **Sound Disabled**: No sound system detected")
        else:
            tips.append("🎵 **Sound Enabled**: All jingles ready!")
        
        if not VLC_AVAILABLE and self.preview_var.get():
            tips.append("🎬 **VLC Not Found**: Install VLC for video preview")
        
        if ADMIN_REQUIRED and not check_admin_privileges():
            tips.append("🛡️ **Run as Admin**: Run as Administrator for best results")
        
        self.log_msg("🚀 CapCut Draft Grabber Started!")
        self.log_msg("=" * 50)
        for tip in tips:
            self.log_msg(tip)
        self.log_msg("=" * 50)
        self.log_msg("💡 Pro Tips:")
        self.log_msg("   • Use ⚙️ Settings to customize behavior")
        self.log_msg("   • Press 🔧 Test to verify your setup")
        self.log_msg("   • Check 📖 Help for detailed documentation")
        self.log_msg("   • Listen for jingles to monitor activity")
        self.log_msg("   • 🔊 Test Sound for audio diagnostics")
    
    def test_setup(self):
        """Test the current setup."""
        self.log_msg("🔧 Running Setup Test...")
        self.log_msg("-" * 40)
        
        monitor_path = self.monitor_var.get()
        if os.path.exists(monitor_path):
            self.log_msg(f"✅ Monitor folder: {monitor_path}")
            try:
                test_file = os.path.join(monitor_path, "test.mp4")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.unlink(test_file)
                self.log_msg("✅ Monitor folder: Write test passed")
            except Exception as e:
                self.log_msg(f"❌ Monitor folder: Write test failed - {e}")
        else:
            self.log_msg(f"❌ Monitor folder: Does not exist - {monitor_path}")
        
        output_path = self.output_var.get()
        if os.path.exists(output_path):
            self.log_msg(f"✅ Output folder: {output_path}")
            try:
                test_file = os.path.join(output_path, "test.mp4")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.unlink(test_file)
                self.log_msg("✅ Output folder: Write test passed")
            except Exception as e:
                self.log_msg(f"❌ Output folder: Write test failed - {e}")
        else:
            self.log_msg(f"❌ Output folder: Does not exist - {output_path}")
        
        # Sound test
        if self.sound_var.get():
            self.log_msg("🔊 Testing sound...")
            try:
                winsound.Beep(1000, 200)
                self.log_msg("✅ Sound test: You should have heard a beep")
            except:
                self.log_msg("❌ Sound test: No sound system available")
        else:
            self.log_msg("🔇 Sound: Disabled by user")
        
        if self.preview_var.get():
            if VLC_AVAILABLE:
                self.log_msg("✅ VLC: Available for video preview")
            else:
                self.log_msg("❌ VLC: Not available for preview")
        else:
            self.log_msg("🎬 Preview: Disabled by user")
        
        if check_admin_privileges():
            self.log_msg("✅ Admin: Running with elevated privileges")
        else:
            self.log_msg("⚠️ Admin: Running as normal user")
        
        self.log_msg("-" * 40)
        self.log_msg("🔧 Test complete! Check results above.")
    
    def start_monitoring(self):
        """Start folder monitoring."""
        monitor_path = self.monitor_var.get()
        output_path = self.output_var.get()
        
        if not os.path.exists(monitor_path):
            messagebox.showerror("Error", 
                "Monitor folder does not exist!\n\n"
                f"Please check the path:\n{monitor_path}")
            return
        
        try:
            os.makedirs(output_path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", 
                f"Cannot create output folder:\n{output_path}\n\n"
                f"Error: {e}")
            return
        
        # Start attribute guard
        self.attribute_stop.clear()
        self.attribute_thread = threading.Thread(
            target=attribute_guard_loop,
            args=(monitor_path, self.attribute_stop, self.log_msg),
            daemon=True
        )
        self.attribute_thread.start()
        
        # Start watchdog with enhanced sound
        self.handler = CapCutHandler(
            self.log_msg,
            self.ask_rename,
            output_path,
            self.settings.get("file_extension", ".mp4"),
            self.sound_var.get(),
            self.settings.get("retry_attempts", 100),
            self.settings.get("retry_delay", 100)
        )
        
        self.observer = Observer()
        self.observer.schedule(self.handler, monitor_path, recursive=True)
        self.observer.start()
        
        # Update UI
        self.is_monitoring = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set(f"📡 Monitoring: {monitor_path}")
        
        self.log_msg(f"🎬 Started monitoring: {monitor_path}")
        self.log_msg(f"📦 Output folder: {output_path}")
        self.log_msg("🛡️ Attribute guard activated")
        if self.sound_var.get():
            self.log_msg("🎵 Sound notifications enabled")
        self.log_msg("⚡ Ready to grab CapCut exports!")
    
    def stop_monitoring(self):
        """Stop folder monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2)
        
        self.attribute_stop.set()
        if self.attribute_thread:
            self.attribute_thread.join(timeout=2)
        
        self.is_monitoring = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("⏹️ Stopped")
        
        self.log_msg("⏹️ Monitoring stopped")
        self.log_msg("🛡️ Attribute guard deactivated")
    
    def ask_rename(self, file_path):
        """Ask user to rename grabbed file."""
        def prompt():
            old_name = os.path.basename(file_path)
            new_name = simpledialog.askstring(
                "📝 Rename File",
                f"🎉 Successfully grabbed:\n\n{old_name}\n\n"
                "Enter new name (or keep same):",
                initialvalue=old_name
            )
            
            if new_name and new_name != old_name:
                if not new_name.lower().endswith(self.settings.get("file_extension", ".mp4")):
                    new_name += self.settings.get("file_extension", ".mp4")
                
                try:
                    new_path = os.path.join(self.output_var.get(), new_name)
                    os.rename(file_path, new_path)
                    self.log_msg(f"📝 Renamed to: {new_name}")
                    
                    if VLC_AVAILABLE and self.preview_var.get():
                        if messagebox.askyesno("🎬 Preview", "Would you like to preview this video?"):
                            MediaPlayer(self.root, new_path)
                    
                except Exception as e:
                    self.log_msg(f"❌ Rename failed: {e}")
        
        self.root.after(0, prompt)
    
    def open_settings(self):
        """Open settings dialog."""
        settings_dialog = SettingsDialog(self.root, self.settings, self.refresh_from_settings)
        self.root.wait_window(settings_dialog.root)
    
    def refresh_from_settings(self):
        """Refresh UI after settings change."""
        self.monitor_var.set(self.settings.get("monitor_folder", ""))
        self.output_var.set(self.settings.get("output_folder", ""))
        self.sound_var.set(self.settings.get("enable_sound", True))
        self.preview_var.set(self.settings.get("enable_preview", True))
        self.log_msg("⚙️ Settings updated")
    
    def open_sound_settings(self):
        """Open sound settings directly."""
        settings_dialog = SettingsDialog(self.root, self.settings, self.refresh_from_settings)
        # Show sound tab directly
        settings_dialog.root.select(2)  # Sound tab is index 2
        self.root.wait_window(settings_dialog.root)
    
    def open_help(self):
        """Open help dialog."""
        help_dialog = HelpDialog(self.root)
        self.root.wait_window(help_dialog.root)
    
    def open_sound_help(self):
        """Open sound help directly."""
        help_dialog = HelpDialog(self.root)
        help_dialog.root.select(2)  # Sound tab is index 2
        self.root.wait_window(help_dialog.root)
    
    def open_output_folder(self):
        """Open output folder in file explorer."""
        try:
            folder_path = self.output_var.get()
            if os.path.exists(folder_path):
                os.startfile(folder_path)
            else:
                self.log_msg(f"❌ Folder does not exist: {folder_path}")
        except Exception as e:
            self.log_msg(f"❌ Failed to open folder: {e}")
    
    def refresh_status(self):
        """Refresh status indicators."""
        self.log_msg("🔄 Status refreshed")
        self.show_initial_tips()
    
    def check_admin(self):
        """Check administrator status."""
        if check_admin_privileges():
            messagebox.showinfo("Admin Status", "✅ Running with Administrator privileges")
        else:
            messagebox.showwarning("Admin Status", 
                "⚠️ Running as normal user.\n\n"
                "For best results, run as Administrator to unlock stubborn files.")
    
    def check_vlc(self):
        """Check VLC installation."""
        if VLC_AVAILABLE:
            messagebox.showinfo("VLC Status", "✅ VLC is installed and ready for video preview")
        else:
            messagebox.showwarning("VLC Status", 
                f"❌ VLC not found or not working:\n{VLC_MESSAGE}\n\n"
                "Please install VLC from videolan.org")
    
    def reset_settings(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?\nThis cannot be undone!"):
            self.settings.reset_to_defaults()
            self.refresh_from_settings()
            messagebox.showinfo("Settings", "✅ Settings reset to defaults")
    
    def show_statistics(self):
        """Show application statistics."""
        stats = f"""
📊 APPLICATION STATISTICS

Version: {VERSION}
Running since: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Monitor folder: {self.monitor_var.get()}
Output folder: {self.output_var.get()}
Status: {'Monitoring' if self.is_monitoring else 'Stopped'}

System Status:
• Sound: {'Available' if SOUND_AVAILABLE else 'Unavailable'}
• VLC: {'Available' if VLC_AVAILABLE else 'Unavailable'}
• Admin: {'Yes' if check_admin_privileges() else 'No'}

Settings:
• Sound notifications: {'Enabled' if self.sound_var.get() else 'Disabled'}
• Video preview: {'Enabled' if self.preview_var.get() else 'Disabled'}
• Retry attempts: {self.settings.get('retry_attempts', 100)}
• Retry delay: {self.settings.get('retry_delay', 100)}ms

Sound System:
• Master sound: {'Enabled' if SOUND_AVAILABLE else 'Disabled'}
• Startup jingle: {'Enabled' if self.settings.get('enable_startup_jingle', True) else 'Disabled'}
• Found jingle: {'Enabled' if self.settings.get('enable_found_jingle', True) else 'Disabled'}
• Success jingle: {'Enabled' if self.settings.get('enable_success_jingle', True) else 'Disabled'}
• Error jingle: {'Enabled' if self.settings.get('enable_error_jingle', True) else 'Disabled'}
• Jingle volume: {self.settings.get('jingle_volume', 1.0)}
        """
        messagebox.showinfo("Statistics", stats)
    
    def show_shortcuts(self):
        """Show keyboard shortcuts."""
        shortcuts = """
⌨️ KEYBOARD SHORTCUTS

MAIN WINDOW:
• Ctrl+S: Start/Stop monitoring
• Ctrl+T: Test setup
• Ctrl+H: Open help
• Ctrl+,: Open settings
• Ctrl+Q: Quit application
• F5: Refresh status
• Ctrl+L: Clear log
• Ctrl+D: Open output folder

TIPS:
• Use Tab to navigate without mouse
• Press Escape to close dialogs
• Use Alt+letter keys for quick access
• Ctrl+S works for both Start and Stop
• Listen for jingles to monitor activity
        """
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
    
    def open_website(self):
        """Open project website."""
        webbrowser.open("https://github.com/yourusername/capcut-grabber")
    
    def report_bug(self):
        """Open bug report page."""
        webbrowser.open("https://github.com/yourusername/capcut-grabber/issues")
    
    def show_about(self):
        """Show about dialog with ASCII logo."""
        about_window = tk.Toplevel(self.root)
        about_window.title("ℹ️ About")
        about_window.geometry("600x400")
        about_window.transient(self.root)
        about_window.grab_set()
        
        about_text = tk.Text(about_window, bg='black', fg='lime', font=('Courier', 8), wrap=tk.NONE)
        about_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        about_text.insert('1.0', """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ╔╗ ╔╗    ╔╗      ╔╗      ╔╗      ╔╗      ╔╗               ║
║    ║║ ║║    ║║      ║║      ║║      ║║      ║║               ║
║    ║║ ║║╔══╝║║╔╗╔╗╔╗║╚╗     ║║╔╗   ║║╔╗╔╗╔╗║║╔══╝══╗        ║
║    ║╚═╝║╔╗╔╗║║║║║║║║╔╗     ║║╠╝   ║║║║║║║║║╔╗╔╗║║╔╗╔╗═╝        ║
║    ║╗  ║║║╚╝║║║║║║║║║╚╝     ║║║    ║║║║║║║║║║║╚╝║║║╚╝║          ║
║    ╚╝  ╚╝╚══╝╚╝╚╝╚╝╚╝╚══╝     ╚╝╚═╗ ╚╝╚╝╚╝╚╝╚╝╚══╝╚╝╚══╝          ║
║                                   ╚╝                           ║
║                    Draft Grabber v2.1.0                        ║
║                                                              ║
║                     By Andy Benson 2025                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🎬 Automatic CapCut export grabber with sound notifications!

FEATURES:
• Real-time monitoring with jingles
• VLC video preview support
• Comprehensive sound system
• Customizable settings
• Professional ASCII interface

LICENSE: MIT License
© 2025 Andy Benson

🎵 SOUND FEATURES:
• Startup jingle for welcome
• Found jingle for detection
• Success jingle for completion
• Error jingle for issues

🌟 Thank you for using CapCut Draft Grabber! 🌟
        """)
        about_text.config(state=tk.DISABLED)
        
        tk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=10)
    
    def safe_exit(self):
        """Safely exit the application."""
        # Save current settings
        self.settings.set("monitor_folder", self.monitor_var.get())
        self.settings.set("output_folder", self.output_var.get())
        self.settings.set("enable_sound", self.sound_var.get())
        self.settings.set("enable_preview", self.preview_var.get())
        self.settings.save_settings()
        
        # Stop monitoring if active
        if self.is_monitoring:
            self.stop_monitoring()
        
        # Close application
        self.root.destroy()
        sys.exit(0)

# --- 🚀 BOOTSTRAP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CapCutGrabberApp(root)
    root.mainloop()
