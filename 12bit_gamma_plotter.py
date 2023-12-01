import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import re
from tkinter import filedialog

# Function to read two 12-bit numbers from a chunk of three bytes
def read_uint12(data_chunk):
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    fst_uint12 = (mid_uint8 << 4) + (fst_uint8 % 16)
    snd_uint12 = (lst_uint8 << 4) + (fst_uint8 >> 4)
    return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])

# Function to update the plots with RGB parameters
def update_plot(parameter_r, parameter_g, parameter_b):

    # Clear the current plot and create new plots for each parameter
    ax.clear()
    ax.plot(parameter_r, 'ro-', label='Red', markersize=0)
    ax.plot(parameter_g, 'go-', label='Green', markersize=0)
    ax.plot(parameter_b, 'bo-', label='Blue', markersize=0)
    ax.set_xlim(0-4, 256+4)
    ax.set_ylim(0-64, 4096+64)
    ax.set_title('Plot of Hex Color Components')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.grid(True)
    ax.legend()
    
    # Redraw the canvas
    canvas.draw()

def parse_hex_colors(input_text):
    # Use a regular expression to find all hex values
    hex_values = re.findall(r'0x[0-9A-Fa-f]+', input_text)

    # Convert hex values to integers and group them into R, G, and B arrays
    values_per_color = len(hex_values) // 3
    parameter_r = [int(hex_values[i], 16) for i in range(0, values_per_color)]
    parameter_g = [int(hex_values[i], 16) for i in range(values_per_color, 2 * values_per_color)]
    parameter_b = [int(hex_values[i], 16) for i in range(2 * values_per_color, 3 * values_per_color)]

    # Make sure all arrays have the same length
    trimmed_length = len(parameter_r) - (len(parameter_r) % 3)
    
    parameter_r = parameter_r[:trimmed_length]
    parameter_g = parameter_g[:trimmed_length]
    parameter_b = parameter_b[:trimmed_length]
    
    # Decode 12bit data format
    def decode_values(data_bytes):
        data_chunk = np.array(data_bytes, dtype=np.uint8).tobytes()
        twelve_bit_numbers = read_uint12(data_chunk)
        return twelve_bit_numbers & 0xFFF # Mask to ensure it's 12-bit
    
    # Return all parameter values (R, G, B)
    return decode_values(parameter_r), decode_values(parameter_g), decode_values(parameter_b)

# Function to handle button click event
def on_button_click():
    # Extract the RGB components from the input text
    parameter_r, parameter_g, parameter_b = parse_hex_colors(text_field.get("1.0", tk.END))

    # Update the plot with the RGB data
    update_plot(parameter_r, parameter_g, parameter_b)

# Function to handle exporting to Adobe AMP format
def export_amp(parameter_r, parameter_g, parameter_b):
    if not len(parameter_r) or not len(parameter_g) or not len(parameter_b):
        print("Error: empty input, nothing to export.")
        return
    if len(parameter_r)+len(parameter_g)+len(parameter_b) < 256*3:
        print("Error: wrong array length in input.")
        return
        # Convert the parameters to 8-bit if they aren't already
    parameter_r_8bit = np.array(parameter_r >> 4, dtype=np.uint8)
    parameter_g_8bit = np.array(parameter_g >> 4, dtype=np.uint8)
    parameter_b_8bit = np.array(parameter_b >> 4, dtype=np.uint8)
    
    # Open a file dialog for the user to choose where to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".amp", filetypes=[("Adobe AMP files", "*.amp")])
    if not file_path:
        print("Export canceled.")
        return  # User canceled the save operation
    
    # Write the data to a binary file in the specified format
    with open(file_path, 'wb') as amp_file:
        amp_file.write(bytes(range(256)))  # Write 256 bytes starting from 00 to FF
        amp_file.write(bytes(parameter_r_8bit))
        amp_file.write(bytes(parameter_g_8bit))
        amp_file.write(bytes(parameter_b_8bit))
        amp_file.write(bytes(range(256)))  # Write 256 bytes starting from 00 to FF again
        
    print("AMP file exported successfully!")

def on_export_button_click():
    # Parse the hex colors from the text field
    parameter_r, parameter_g, parameter_b = parse_hex_colors(text_field.get("1.0", tk.END))
    # Call the function to export to AMP with the parsed RGB values
    export_amp(parameter_r, parameter_g, parameter_b)

# Create the main window
root = tk.Tk()
root.title("12-bit Gamma Curve Plotter")

# Create the text field for input
text_field_label = ttk.Label(root, text="Enter parameter_r, parameter_g, parameter_b values")
text_field_label.pack(fill='x')

# Create a frame to hold text field and scrollbar
text_frame = tk.Frame(root)
text_frame.pack(fill='both', expand=True)

# Create the text field within the frame
text_field = tk.Text(text_frame, height=15)
text_field.pack(side='left', fill='both', expand=True)

# Create a scrollbar within the frame and associate it with the text field
scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_field.yview)
scrollbar.pack(side='right', fill='y')

text_field['yscrollcommand'] = scrollbar.set

# Create a button to update the plots
update_button = ttk.Button(root, text="Update Plot", command=on_button_click)
update_button.pack(fill='x')

export_amp_button = ttk.Button(root, text="Export AMP File", command=on_export_button_click)
export_amp_button.pack(fill='x')

# Create a figure and a single subplot
fig = Figure(figsize=(6, 5), tight_layout=True)
ax = fig.add_subplot(111)

# Create the matplotlib canvas and embed it in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True)


# Start the Tkinter event loop
root.mainloop()