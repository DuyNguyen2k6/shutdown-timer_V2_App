# Shutdown Timer V2 App

A desktop application for Windows that lets you schedule system shutdown, restart, or sleep at a specified time, with customizable warnings and easy cancellation. Built with Python and PyQt6.

---

## Features

* **Schedule Actions**: Pick a specific date and time to shutdown, restart, or put your PC to sleep.
* **Countdown Timer**: Set a countdown in minutes or hours before triggering the action.
* **Custom Warnings**: Show one or more warning messages with configurable intervals before execution.
* **Cancel/Abort**: Easily cancel the scheduled action at any time.
* **System Tray Integration**: Minimize to tray with status icon and context menu.
* **Lightweight & Portable**: Single-file executable using PyInstaller.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DuyNguyen2k6/shutdown-timer_V2_App.git
   ```
2. Navigate to the project directory:

   ```bash
   cd shutdown-timer_V2_App
   ```
3. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:

   ```bash
   python shutdown_timer.py
   ```
6. To build an executable:

   ```bash
   pyinstaller --onefile --windowed --icon=app_icon.ico shutdown_timer.py
   ```

---

## Usage

1. **Select Action**: Choose `Shutdown`, `Restart`, or `Sleep` from the dropdown.
2. **Set Schedule**:

   * **Specific Time**: Pick a date and clock time.
   * **Countdown**: Enter minutes or hours for a countdown.
3. **Configure Warnings**:

   * Enable warnings and set intervals (e.g., 10, 5, and 1 minute before).
   * Customize warning messages.
4. **Start Timer**: Click **Start** to activate.
5. **Monitor**: The tray icon changes color to indicate active timer.
6. **Cancel**: Click **Cancel** in the UI or tray context menu to abort.

---

## File Structure

* `shutdown_timer.py` — Main application logic and UI.
* `ui_main.py`      — Auto-generated PyQt6 UI file.
* `resources/`      — Icons and resource files.
* `requirements.txt` — Python dependencies.
* `app_icon.ico`     — Icon for the executable.
* `README.md`        — This documentation.

---

## Contributing

Contributions welcome! Steps:

1. Fork the repo.
2. Create a feature branch:

   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add my feature"
   ```
4. Push and open a pull request:

   ```bash
   git push origin feature/my-feature
   ```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
