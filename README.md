# Adobe *.acv to Android TV Panel *.ini Gamma Table Converter

This project is designed for graphical visualization and conversion of Adobe ACV files into Android gamma panel format. It includes a main script that reads an `*.acv` file, draws curves plot, and converts curves data into a format suitable for Android TV panel calibration. And an additional script, that decodes 12bit HEX `gamma_table_x` values, draws a plot with RGB curves and exports them in AMP format.

<img src="https://github.com/NameRX/ACV_12bit_converter/blob/main/Adobe_AE_curves_screenshot.png" height="520" alt="Screenshot of Adobe_curves"> <img src="https://github.com/NameRX/ACV_12bit_converter/blob/main/ACV_12bit_converter_screenshot.png" height="520" alt="Screenshot of ACV conversion">


## Features

- **ACV Curve Plotting**: The main script (`ACV_12bit_converter.py`) plots the curves from the ACV file, which shows input Luma and RGB curves, and also calculates combined Luma + RGB curves.
- **Conversion to Panel Format**: The curves are converted into a 12-bit hexadecimal format compliant with the requirements of Android TV's panel calibration configuration. This data is stored in an `ini` file, for example: `/vendor/tvconfig/config/panel/FullHD_CMO216_H1L01.ini`.
- **Gamma Curve Review**: An additional script (`12bit_gamma_plotter.py`) provides functionality to review the converted gamma curves or to visualize the original gamma curves from an Android TV panel `ini` file.
- **Gamma Curve Export**: A script (`12bit_gamma_plotter.py`) can also export gamma table to Adobe *.amp format.

## Usage

1. **ACV to 12-bit Converter (`ACV_12bit_converter.py`):**
    - Run the script or the corresponding executable.
    - Use the graphical interface to open an `.acv` file.
    - Observe the plotted gamma curves for the Luma and RGB channels.
    - The output 12-bit gamma tables for the Red, Green, and Blue channels are displayed in the text field. They can be copied for use in panel calibration configurations.

2. **12-bit Gamma Plotter (`12bit_gamma_plotter.py`):**
    - Run the script or the corresponding executable to initiate the graphical tool for plotting gamma curves.
    - Paste the 12-bit gamma parameters for the Red, Green, and Blue channels into the text area provided.
    - Press the "Update Plot" button to visualize the curves.
    - Press the "Export AMP File" button to export curves to *.amp format.


## Downloads

You can download windows executable builds in [Releases](https://github.com/NameRX/ACV_12bit_converter/releases) section.

## Manual Installation and Running

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

This format is also used as input by the `12bit_gamma_plotter.py` script, that could be usefull to look through original curve from `*.ini` file.

<img src="https://github.com/NameRX/ACV_12bit_converter/blob/main/12bit_gamma_plotter_screenshot.png" height="600" alt="Screenshot of gamma curve plotting">

## Modifying Android Panel .ini File

To upload and download system files to an Android device, you may need proper file system permissions (root access), and you should also enable Developer Mode. I used [ADB AppControl](https://adbappcontrol.com/) to perform all the manipulations.

- Locate your device's panel *.ini file. The path to it can be found in the `Customer_1.ini` file, which is located here, for example:

  `/tvconfig/config/model/Customer_1.ini`
  
- Open it in a text editor (I recommend using [Sublime Text](https://www.sublimetext.com/)) and find the `m_pPanelName` entry. For example:
  
  `m_pPanelName = "/vendor/tvconfig/config/panel/FullHD_CMO216_H1L01.ini"`
  
- Download the panel *.ini file and make a backup. Open it in a text editor, look through it, and find the text segment:
```ini
[gamma_table_0]
parameter_r = \
{ \
0x40,0x00,0x01,0xD8,0x02,0x03,0x61,0x05,0x06, \
.....
```
- Carefully replace the original values for `parameter_r`, `parameter_g`, and `parameter_b` with the desired gamma tables under each `[gamma_table_x]`. For my device, I replaced `[gamma_table_x]` values 4 times.
- Save the file, upload it to the device by replacing the existing one, and reboot the device.

## FAQ - Frequently Asked Questions

### Q1: Curves shown in the script don't exactly match the curves in the Adobe application.
**A:** Try adding more points before saving the *.acv file. Adobe uses its own interpolation method for curve points.

### Q2: I replaced the file on my Android device, and there are no changes in image quality.
**A:** Try to change the Picture mode and Gamma settings back and forth if they are present. If that doesn't work, double-check the panel file location.

## Contributing

Contributions to the project are welcome!

## Author

- **Andrey Voskresensky** - RailwayFX (aka NameRX)

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
