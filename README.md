# TrackTime — Personal Activity & Time Tracker
TrackTime is a Python desktop application that helps users record activities, measure time spent on tasks, and manage session history through a simple, 
colourful interface.

## Features
- **Session Timer:** Start an activity timer and save the elapsed time when finished.
- **Add Sessions:** Create activity records manually.
- **Edit Sessions:** Update activity names without recreating records.
- **Delete Sessions:** Remove unwanted records.
- **Session History:** View saved activities, dates, and recorded durations.
- **Tracked-Time Summary:** See the total number of sessions and recorded time.
- **Local Data Storage:** Save session history in a local JSON file.

## Technologies Used
- Python
- CustomTkinter
- JSON
- Python standard libraries: `time`, `datetime`, `json`, `os`, and `tkinter`

## Getting Started

### Prerequisites
- Python 3.10 or a compatible Python version
- pip

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shatarupa4321-cloud/TrackTime.git
   ```

2. Navigate to the project folder:
   ```bash
   cd TrackTime
   ```

3. Install the required package:
   ```bash
   python -m pip install customtkinter
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The application creates or uses `sessions.json` in its working directory to store session history.

## How to Use
1. Enter the name of an activity.
2. Select **Start** to begin tracking time.
3. Select **Stop & Save** to save a completed timed session.
4. Use **Add Session** to create a manual activity record.
5. Use **Edit** to rename a session or **Delete** to remove it.
6. Review your session history and tracked-time summary.

## Data and Privacy
Session history is stored locally in `sessions.json`. This file is excluded from version control through `.gitignore` so personal session records are not uploaded to the repository.

## Future Improvements
- Daily and weekly activity reports
- Search and filtering for session history
- Optional data export
