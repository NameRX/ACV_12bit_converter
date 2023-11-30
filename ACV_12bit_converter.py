import struct
import cv2
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d
import numpy as np

# Define colors for the curves, removed the entry for the alpha curve
curve_colors = {
    1: ('Luma', 'black'),
    2: ('Red', 'red'),
    3: ('Green', 'green'),
    4: ('Blue', 'blue')
}

# Initialize arrays to store the 256-element interpolated values for each curve
curve_values = {
    'Luma': [],
    'Red': [],
    'Green': [],
    'Blue': []
}

orig_points = []

# Create the main window
window = tk.Tk()
window.title("ACV to 12bit HEX Converter")

def LUT(src, lut):
    # Check if the LUT has the correct size for 16-bit images
    if lut.size != 65536:
        raise ValueError("LUT must have 65536 elements for a 16-bit image.")
    
    # Initialize the output image with the same shape as the source
    result = np.empty_like(src)
    
    # Apply the LUT to each pixel in the source image
    for i in range(len(src)):
            result[i] = lut[src[i]]
            
    return result

def uint16toHex12(uint16_array):
    # Resize the array to 256 elements
    array256 = []
    for i in range (0, 256):
        array256.append(round(uint16_array[i*256]/16))

    # Map the resized array to 12-bit range
    mapped_array = np.interp(array256, (0, 4095), (0, 4095)).astype(np.uint16)

    # Format each element as a 12-bit hex string in uppercase
    hex_array = ['{:03X}'.format(x) for x in mapped_array]
    
    return hex_array

def output_final(input, color):
    if len(input) < 2:
        raise ValueError("Input array must contain at least two elements.")
    
    to12bit = []
    for i in range(0, len(input) - 1, 2):
        # Construct the strings and append them all at once
        combined = f'0x{input[i+1][2]}{input[i][2]} 0x{input[i][:2]} 0x{input[i+1][:2]}'
        to12bit.extend(combined.split())

    out = f'parameter_{color} = \\\n{{ \\\n'
    lenght = len(to12bit)
    for i in range(0, lenght // 9):
        for y in range(0,9):
            out += f'{to12bit[i*9+y]},'
        out += ' \\\n'
    for y in range(lenght - lenght % 9 ,lenght):
        out += f'{to12bit[y]},'
    out += '0x00,0xFF \\\n} \\\n;\n'
        
    return out

def open_acv_file():
    filepath = filedialog.askopenfilename(filetypes=[("ACV files", "*.acv"), ("All files", "*.*")])
    if not filepath:
        return

    print(filepath)
    window.title("ACV to 12bit HEX Converter " + filepath)
    filename = filepath.split('/')[-1]

    with open(filepath, 'rb') as f:
        _, num_curves = struct.unpack("!hh", f.read(4))

        curves = []
        for _ in range(num_curves):
            num_points, = struct.unpack("!h", f.read(2))
            points = [struct.unpack("!hh", f.read(4)) for _ in range(num_points)]
            curves.append(points)

    plot_curves(curves,filename)

def plot_curves(curves,filename):
    # Clear previous figure
    plt.clf()

    # Clear the output text field before plotting new curves
    text_output.delete("1.0", tk.END)

    interpolated_curves = {}

    global orig_points, orig_curveL, orig_curveR, orig_curveG, orig_curveB, mod_curveR, mod_curveG, mod_curveB
    
    for i, curve in enumerate(curves):
        if i == 4:  # This is the index for the alpha curve, so we skip it
            continue
        y, x = zip(*curve)  # Swapping input and output

        
        label, color = curve_colors.get(i+1, (f'Curve {i+1}', 'gray'))  # Fallback label and color if not defined

        print (label)
        print (curve)

        x_new = np.arange(0, 256*256)*255/65535

        # Decide on the type of interpolation based on the number of points
        if len(x) < 3:
            kind = 'linear'
        else:
            kind = 'quadratic'
        
        # Create an interpolation function based on the kind of interpolation
        interpolating_function = interp1d(x, y, kind=kind, fill_value="extrapolate")
        y_new = interpolating_function(x_new)  # Apply the interpolation function to the new x points

        y_new_clipped = np.clip(y_new, 0, 255)*65535/255

        # Store the interpolated and clipped values
        curve_name = curve_colors.get(i+1, (None,))[0]
        if curve_name:  # Only proceed if curve name is valid
            interpolated_curves[curve_name] = y_new_clipped.astype(np.uint16)

        # Plot the interpolated curve
        orig_points.append(plt.scatter(np.array(x)*65535/255, np.array(y)*65535/255, color=color, marker='o', s=16, visible=show_original.get()))


    # Create arrays
    Luma = interpolated_curves['Luma']
    Red = interpolated_curves['Red']
    Green = interpolated_curves['Green']
    Blue = interpolated_curves['Blue']

    # Calculate modified curves with Luma
    Red_wLuma = LUT(Red, Luma)
    Green_wLuma = LUT(Green, Luma)
    Blue_wLuma = LUT(Blue, Luma)

    # Format curve arrays to 12bit
    Red_12bit = uint16toHex12(Red_wLuma)
    Green_12bit = uint16toHex12(Green_wLuma)
    Blue_12bit = uint16toHex12(Blue_wLuma)

    # Plot original curve
    orig_curveL, = plt.plot(Luma, label='Luma', color='black', linewidth=1, visible=show_original.get())
    orig_curveR, = plt.plot(Red, label='Red', color='red', linewidth=1, visible=show_original.get())
    orig_curveG, = plt.plot(Green, label='Green', color='green', linewidth=1, visible=show_original.get())
    orig_curveB, = plt.plot(Blue, label='Blue', color='blue', linewidth=1, visible=show_original.get())

    # Plot the modified curves
    mod_curveR, = plt.plot(Red_wLuma, label='Red_wLuma', color='red', linewidth=1, alpha=0.4, linestyle='--', visible=show_modified.get())
    mod_curveG, = plt.plot(Green_wLuma, label='Green_wLuma', color='green', linewidth=1, alpha=0.4, linestyle='--', visible=show_modified.get())
    mod_curveB, = plt.plot(Blue_wLuma, label='Blue_wLuma', color='blue', linewidth=1, alpha=0.4, linestyle='--', visible=show_modified.get())


    # Output the modified curve arrays into the text field in 12bit
    text_output.insert(tk.END, output_final(Red_12bit, 'r'))
    text_output.insert(tk.END, output_final(Green_12bit, 'g'))
    text_output.insert(tk.END, output_final(Blue_12bit, 'b'))



    plt.title(filename + ' curves')
    plt.legend()
    plt.grid(True)
    plt.xlim(0-256*3, 65535+256*3)
    plt.ylim(0-256*3, 65535+256*3)
    plt.xlabel('Input')
    plt.ylabel('Output')

    # Embedding the plot into the Tkinter window
    canvas.draw()

# Define a function to update plot based on checkboxes
def update_plot():
    
    # Change the Original Curves visibility based on checkbox
    for i in orig_points:
        i.set_visible(show_original.get())
    orig_curveL.set_visible(show_original.get())
    orig_curveR.set_visible(show_original.get())
    orig_curveG.set_visible(show_original.get())
    orig_curveB.set_visible(show_original.get())

    # Change the Moddified Curves visibility based on checkbox
    mod_curveR.set_visible(show_modified.get())
    mod_curveG.set_visible(show_modified.get())
    mod_curveB.set_visible(show_modified.get())

    canvas.draw()  # Redraw the canvas after changing the visibility
    
# Create a frame to hold the buttons and checkboxes in a single line
controls_frame = tk.Frame(window)
controls_frame.pack(side=tk.TOP)

# Add the open ACV file button to the controls frame
open_button = tk.Button(controls_frame, text="Open ACV File", command=open_acv_file)
open_button.pack(side=tk.LEFT, padx=5)  # Add a little padding for spacing
#open_button.pack(side=tk.TOP, fill=tk.X)

# Checkbox toggle states
show_original = tk.BooleanVar(value=True)
show_modified = tk.BooleanVar(value=True)

# Add the show original curves checkbox to the controls frame
original_checkbox = tk.Checkbutton(controls_frame, text="Show Original Curves", variable=show_original, command=update_plot)
original_checkbox.pack(side=tk.LEFT, padx=5)  # Add a little padding for spacing

# Add the show modified curves checkbox to the controls frame
modified_checkbox = tk.Checkbutton(controls_frame, text="Show Output Curves", variable=show_modified, command=update_plot)
modified_checkbox.pack(side=tk.LEFT, padx=5)  # Add a little padding for spacing

# Create a figure for plotting
fig, ax = plt.subplots(figsize=(8, 7))
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
plt.title('No curves loaded')

# Create the text field for input
text_field_label = tk.Label(window, text="Output parameter_r, parameter_g, parameter_b values")
text_field_label.pack(fill='x')

# Create a frame to hold the text field and the scrollbar
text_frame = tk.Frame(window)
text_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

# Create a text field to output the curve arrays
text_output = tk.Text(text_frame, height=15, width=30)
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar widget
scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')

# Configure the text field to work with the scrollbar
text_output.config(yscrollcommand=scrollbar.set)

# Start the Tkinter loop
window.mainloop()