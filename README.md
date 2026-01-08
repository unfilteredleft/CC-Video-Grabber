# CapCut Temp Export Grabber

A simple Python tool to automatically grab temporary exported MP4 files from CapCut on Windows before they are deleted.

## 🌟 Features
- 🔍 **Real-time Monitoring**: Watches CapCut export folder for temporary `{...}` folders
- 📦 **Automatic File Detection**: Recursively searches inside for .mp4 files
- 🚀 **Smart Retry Logic**: Tries up to 100 attempts (10 seconds) to grab locked files
- 🎬 **VLC Video Preview**: Built-in video preview with VLC Media Player integration
- 🔊 **Sound Notifications**: Success jingle plays when files are grabbed
- 🛡️ **File Unlocking**: Background thread continuously unlocks CapCut's locked files
- 🖼️ **Modern GUI**: User-friendly interface with log, status indicators, and controls
- ✏️ **Rename Dialog**: Optional rename after successful file grab
- 🎮 **Start/Stop Controls**: Pause/resume/stop monitoring anytime
- 📊 **System Status**: Visual indicators for sound, VLC, and admin privileges
- 🔧 **Setup Testing**: Built-in test function to verify configuration
- ⚙️ **Persistent Settings**: Saves your preferences between sessions
- 💚/💔 **ASCII Notifications**: Success and fail messages in the log

## 🚀 Quick Start
1. **Install Python 3.7+** from [python.org](https://python.org)
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
