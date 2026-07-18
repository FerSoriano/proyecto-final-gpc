# proyecto-final-gpc

## Initial Layout

```plain text
project/
│
├── main.py                 # Application entry point. Initializes UI and Controller.
│
├── controllers/            # The bridge between UI and Mathematical Logic.
│   ├── __init__.py
│   └── app_controller.py   # Receives UI events, requests calculations, and updates views.
│
├── ui/                     # Views (Tkinter) - Handles layout, buttons, and canvas drawing.
│   ├── __init__.py
│   ├── main_window.py      # Main window structure, side panels, and text areas.
│   └── canvas_manager.py   # Manages the 900x600 canvas and mouse event bindings.
│
├── algorithms/             # Pure math and primitive generation algorithms.
│   ├── __init__.py
│   ├── dda.py              # Digital Differential Analyzer algorithm implementation.
│   ├── bresenham.py        # Bresenham's line algorithm implementation.
│   └── curves.py           # Functions for circles, mid-point parabolas, etc.
│
├── utils/                  # Helper tools.
│   ├── __init__.py
│   └── logger.py           # Formats mathematical steps for the UI output panel.
│
├── .gitignore              # Specifies intentionally untracked files to ignore.
└── README.md               # Project documentation and execution instructions.
```
