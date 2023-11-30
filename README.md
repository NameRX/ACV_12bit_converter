# Adobe ACV to Android TV Panel 12-bit Gamma Curves Converter

This project is a Python application designed for graphical visualization and conversion of Adobe ACV files commonly used to store tone curves for image processing. It includes a main script that reads an ACV file, plots the curve data, and converts it into a format suitable for Android TV panel calibration.

<img src="https://github.com/NameRX/ACV_12bit_converter/blob/main/Adobe_AE_curves_screenshot.png" height="520" alt="Screenshot of Adobe_curves"> <img src="https://github.com/NameRX/ACV_12bit_converter/blob/main/ACV_12bit_converter_screenshot.png" height="520" alt="Screenshot of ACV conversion">


## Features

- **ACV Curve Plotting**: The main script (`ACV_12bit_converter.py`) plots the curves from the ACV file, showing Luma and the RGB channels.
- **Conversion to Panel Format**: The curves are converted into a 12-bit hexadecimal format compliant with the requirements of Android TV's panel calibration configuration.
- **Gamma Curve Review**: An additional script (`12bit_gamma_plotter.py`) provides functionality to review the converted gamma curves or visualize original gamma curves from an Android TV panel ini file.

## Usage

1. **ACV to 12-bit Converter (`ACV_12bit_converter.py`):**
    - Run the script in a Python environment with the required dependencies installed.
    - Use the graphical interface to open an `.acv` file.
    - Observe the plotted gamma curves for the Luma and RGB channels.
    - The output 12-bit gamma tables for Red, Green, and Blue channels are displayed in the text field and can be copied for use in panel calibration configurations.

2. **12-bit Gamma Plotter (`12bit_gamma_plotter.py`):**
    - Run the script to initiate the graphical tool for plotting gamma curves.
    - Paste the 12-bit gamma parameters for the Red, Green, and Blue channels into the text area.
    - Press the "Update Plot" button to visualize the curves.

## Installation

To set up the project, ensure you have [Python](https://www.python.org/downloads/) installed ([3.12.0](https://www.python.org/downloads/release/python-3120/) works well on Windows 10) along with the following dependencies:

- `matplotlib`
- `numpy`
- `opencv-python`
- `scipy`
- `tkinter`

You can use `pip` to install any missing dependencies:

```bash
pip install matplotlib numpy opencv-python scipy
```

Note: `tkinter` is usually included in standard Python distributions. If it's missing, refer to Python's documentation for installation instructions suitable for your operating system.

## Output Format

The output gamma curves are formatted as follows:

```python
parameter_r = \
{ \
    # Red Gamma table here...
}  \
;
parameter_g = \
{ \
    # Green Gamma table here...
}  \
;
parameter_b = \
{ \
    # Blue Gamma table here...
}  \
;
```

This format is also used as input by the `12bit_gamma_plotter.py` script.

<img src="https://github.com/NameRX/ACV_12bit_converter/blob/main/12bit_gamma_plotter_screenshot.png" height="600" alt="Screenshot of gamma curve plotting">

## Contributing

Contributions to the project are welcome!
