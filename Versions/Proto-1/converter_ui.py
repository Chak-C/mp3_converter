import tkinter as tk
from tkinter import ttk

import recommend_ui as ru
import ui_functions as uf

root = tk.Tk()
root.title("YouTube Converter")
root.protocol("WM_DELETE_WINDOW", quit)

# URL Entry
url_label = tk.Label(root, text="Enter URL:")
url_label.pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Default folder option
default_folder_var = tk.IntVar(value=0)
default_folder_checkbox = tk.Checkbutton(root, text="Use default download folder", 
                                         variable=default_folder_var, 
                                         command=lambda: uf.toggle_default_folder(default_folder_var))
default_folder_checkbox.pack()

# Information Labels
title_label = tk.Text(root, wrap='none', height=1, width = 0, borderwidth=0, highlightthickness=0, state=tk.DISABLED)
duration_label = tk.Label(root, text="")
image_label = tk.Label(root)

# Download Button
download_button = tk.Button(root, text="Download", command=lambda: '')

# Dropdown menu for additional properties
additional_properties_frame = tk.Frame(root)

properties = {
    "Title": tk.StringVar(),
    "Subtitle": tk.StringVar(),
    "Contributing Artists": tk.StringVar(),
    "Album Artist": tk.StringVar(),
    "Album": tk.StringVar(),
    "Year": tk.StringVar(),
    "Genre": tk.StringVar(),
    "Bit Rate": tk.StringVar()
}

for prop_name, prop_var in properties.items():
    property_frame = tk.Frame(additional_properties_frame)
    property_frame.pack(side="top", fill="x", padx=5, pady=5)
    
    label = tk.Label(property_frame, text=prop_name)
    label.pack(side="left", padx=5, pady=5)
    
    dropdown = ttk.Entry(property_frame, textvariable=prop_var, width = 40)
    dropdown.pack(side="right", padx=5, pady=5, anchor="center")

# Frame for the Recommendations button
recommend_frame = tk.Frame(root)

# Recommend Button
recommend_button = tk.Button(recommend_frame, 
                             text="Recommendations", 
                             command=lambda: ru.start_recommendation_ui(properties['Title'].get(),properties['Album Artist'].get()))
recommend_button.pack(padx=5, pady=8, anchor="center")

# Advanced Properties Check Boolean
advanced_properties_var = tk.BooleanVar(value=False)

toggle_properties_widget = {
    'title_label': title_label,
    'advanced_properties_var': advanced_properties_var,
    'additional_properties_frame': additional_properties_frame,
    'recommend_frame': recommend_frame
}

# Advanced Properties Check Button
advanced_properties_checkbox = tk.Checkbutton(root, text="Show Advanced Properties", 
                                              variable=advanced_properties_var, 
                                              command=lambda: uf.toggle_advanced_properties(toggle_properties_widget, properties))


handle_scan_widget = {
    'title_label': title_label,
    'duration_label': duration_label,
    'image_label': image_label,
    'download_button': download_button,
    'advanced_properties_var': advanced_properties_var
}

# Scan Button
scan_button = tk.Button(root, text="URL Search", command=lambda: uf.handle_scan(url_entry, handle_scan_widget, properties))

# Packing in order
scan_button.pack()
title_label.pack()
duration_label.pack()
image_label.pack()
advanced_properties_checkbox.pack()
download_button.pack()

def quit():
    global root
    print('Leaving converter')
    root.quit()
    pass

def load_recommended_url(url):
    global url_entry
    url_entry.delete(0, tk.END)
    url_entry.insert(0, url)
    uf.handle_scan(url_entry, handle_scan_widget, properties)
    pass

root.mainloop()