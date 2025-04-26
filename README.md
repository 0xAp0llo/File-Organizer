# 📁 File Organizer

A simple yet powerful Python tool to automatically organize files into categories based on their file types.

## ✨ Features

- 🗂️ Automatically categorizes files based on their extensions
- 📊 Provides statistics on organized files
- 🔄 Handles file name conflicts
- 🔍 Supports recursive directory scanning
- 🧪 Dry-run mode to preview changes without moving files

## 📋 Categories

The tool organizes files into the following categories:

- 🖼️ **Images**: jpg, jpeg, png, gif, bmp, tiff, webp, svg
- 📄 **Documents**: pdf, doc, docx, txt, rtf, odt, xls, xlsx, ppt, pptx
- 🎵 **Audio**: mp3, wav, flac, aac, ogg, m4a
- 🎬 **Video**: mp4, avi, mkv, mov, wmv, flv, webm
- 🗜️ **Archives**: zip, rar, tar, gz, 7z
- 💻 **Code**: py, js, html, css, java, cpp, c, php, rb, go, rs, json
- 📦 **Others**: Any file type not in the above categories

## 🔧 Requirements

- Python 3.6 or higher

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/0xAp0llo/file-organizer.git
cd file-organizer
```

2. Make the script executable (Unix/Linux/macOS):
```bash
chmod +x main.py
```

## 🔍 Usage
```bash
python main.py [source_directory] [options]
```

## ⚙️ Options

- `-t, --target`: Target directory (default: same as source)
- `-r, --recursive`: Process directories recursively
- `-d, --dry-run`: Show what would be done without actually moving files
- `-n, --no-stats`: Don't show statistics

📝 Examples

### Organize the current directory
```bash
python main.py
```

### Organize Downloads folder and move files to a different location
```bash
python main.py ~/Downloads -t ~/Organized
```

### Preview organization without moving files
```bash
python main.py ~/Documents -d
```

### Recursively organize a directory
```bash
python main.py ~/Projects -r
```
## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
