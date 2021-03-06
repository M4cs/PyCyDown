# PyCyDown
Python Based Cydia Downloader | **Currently Under Development**

This repository is in active development. The source code may not work completely and not all features have been implemented yet. To keep up with updates Watch this repository above.

# Features:

- Fast and Lightweight Package Manager
- Save and Load Configurations
- Easy to use UI
- Multi-Package Queue
- Basic iOS Support

## Requirements:

- Python 3.6+
- An Internet Connection
- wget

## Installation:

### iOS setup (skip if not on iOS)

- Download TestFlight https://itunes.apple.com/us/app/testflight/id899247664?mt=8
- Download iSH from TestFlight https://testflight.apple.com/join/97i7KM8O

Open iSH and input the following:
```
apk add wget
apk add python
apk add python3
apk add py-pip
apk add git
```

### Clone the repository:
```
git clone https://github.com/M4cs/PyCyDown.git
```

### Install Wget:

**On Windows:**

Using Choco:
```
choco install wget
```

**MacOS and Linux Distros should come with wget by default.**

### Install Python Dependencies:

```
cd PyCyDown/
pip3 install virtualenv
virtualenv venv

// On Windows:
venv\Scripts\activate.bat

// On Unix:
source venv/bin/activate

pip3 install -r requirements.txt
```

# Running

Run:
```
python3 pycydown.py
```

Use `help` to see commands.

