# 🎯 Habit Tracker

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.5%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A simple, elegant, and powerful desktop application for tracking daily habits and building consistency.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Roadmap](#-roadmap)

</div>

---

## ✨ Features

- ✅ **Track Daily Habits** - Add and manage your daily routines
- 🔥 **Streak Tracking** - Visual streak counters to keep you motivated
- 📊 **Statistics** - Monitor your completion rates and progress
- 💾 **Local Storage** - Your data stays on your computer (SQLite database)
- 🎨 **Clean Interface** - Modern, intuitive, and distraction-free design
- ⚡ **Fast & Lightweight** - No bloat, just what you need

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/manish-kumar-das/habit-tracker.git
cd habit-tracker
```

2. **Create a virtual environment**
```bash
# Windows (Git Bash)
python -m venv venv
source venv/Scripts/activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main.py
```

---

## 📖 Usage

### Adding a Habit
1. Click the **"➕ Add New Habit"** button
2. Enter the habit name (e.g., "Morning Exercise")
3. Add an optional description
4. Select frequency (Daily/Weekly)
5. Click **"Create Habit"**

### Tracking Habits
- ✅ Check the box next to a habit to mark it complete for today
- ⬜ Uncheck to mark as incomplete
- 🔥 Watch your streak counter grow!

### Managing Habits
- 🗑️ Click the trash icon to delete a habit
- 📋 Use **File → Refresh** to reload the habit list
- 🔄 Data saves automatically

### Viewing Progress
- See your current streak next to each habit
- Completed habits show a green checkmark
- Streaks display with a 🔥 icon

---

## 📸 Screenshots

*Coming soon! Run the app to see it in action.*

---

## 🗂️ Project Structure
```
habit-tracker/
├── app/
│   ├── views/           # User interface components (Windows, Dialogs, Content)
│   │   ├── main_window.py
│   │   ├── dashboard_content_view.py
│   │   └── sidebar.py
│   ├── themes/          # Theme system (Dark/Light mode)
│   │   ├── light_theme.py
│   │   └── dark_theme.py
│   ├── widgets/         # Reusable UI components
│   │   └── theme_toggle.py
│   ├── models/          # Data models
│   ├── services/        # Business logic & services
│   ├── db/              # Database layer
│   ├── utils/           # Utility functions
│   └── assets/          # Icons and styles
├── data/                # SQLite database storage
├── docs/                # Documentation
├── main.py              # Application entry point (Shim)
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🛠️ Technology Stack

- **Language:** Python 3.8+
- **GUI Framework:** PySide6 (Qt for Python)
- **Database:** SQLite3
- **Architecture:** MVC (Model-View-Controller)

---

## 🗺️ Roadmap

See [docs/roadmap.md](docs/roadmap.md) for detailed future plans.

**Coming Soon:**
- 📊 Advanced statistics dashboard
- 🎨 Dark mode
- 📁 Data export/import
- 🔔 Reminders and notifications
- 📱 Mobile companion app

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Bug Reports

Found a bug? Please open an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Your environment (OS, Python version)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Manish Kumar Das**
- GitHub: [@manish-kumar-das](https://github.com/manish-kumar-das)
- Email: manishkumardas7890@gmail.com

---

## 🙏 Acknowledgments

- Built with [PySide6](https://doc.qt.io/qtforpython/)
- Inspired by the power of consistent daily habits
- Thanks to the Python and Qt communities

---

## ⭐ Show Your Support

If you found this project helpful, please consider giving it a star on GitHub!

---

<div align="center">

**Made with ❤️ and Python**

*Track your habits. Build consistency. Achieve your goals.*

</div>
