import tkinter as tk
from tkinter import ttk

import ui_functions as uf
from ui_mediator import Mediator
from recommend_ui import RecommendUI
from typing import Type

class ConverterUI:
    def __init__(self, mediator: Type[Mediator]):
        self.url_mediator = mediator
        self.url_mediator.subscribe(self)

        self.root = tk.Tk()
        self.root.title("Youtube Converter")
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        # URL Entry
        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack() 

        # Default folder option
        self.default_folder_var = tk.IntVar(value=0)
        self.default_folder_checkbox = tk.Checkbutton(self.root, text="Use default download folder", 
                                         variable=self.default_folder_var, 
                                         command=lambda: uf.toggle_default_folder(self.default_folder_var))
        self.default_folder_checkbox.pack()

        # Information Labels
        self.title_label = tk.Text(self.root, wrap='none', height=1, width = 0, borderwidth=0, highlightthickness=0, state=tk.DISABLED)
        self.duration_label = tk.Label(self.root, text="")
        self.image_label = tk.Label(self.root)
        
        # Download Button
        self.download_button = tk.Button(self.root, text="Download", command=lambda: '')

        # Dropdown menu for additional properties
        self.additional_properties_frame = tk.Frame(self.root)

        self.properties = {
            "Title": tk.StringVar(),
            "Subtitle": tk.StringVar(),
            "Contributing Artists": tk.StringVar(),
            "Album Artist": tk.StringVar(),
            "Album": tk.StringVar(),
            "Year": tk.StringVar(),
            "Genre": tk.StringVar(),
            "Bit Rate": tk.StringVar()
        }

        for prop_name, prop_var in self.properties.items():
            property_frame = tk.Frame(self.additional_properties_frame)
            property_frame.pack(side="top", fill="x", padx=5, pady=5)
            
            label = tk.Label(property_frame, text=prop_name)
            label.pack(side="left", padx=5, pady=5)
            
            dropdown = ttk.Entry(property_frame, textvariable=prop_var, width = 40)
            dropdown.pack(side="right", padx=5, pady=5, anchor="center")
            
        # Frame for the Search and Recommendations buttons
        self.bottom_frame = tk.Frame(self.root)
        self.recommend_frame = tk.Frame(self.bottom_frame)
        self.search_frame = tk.Frame(self.bottom_frame)

        self.recommend_frame.pack(side=tk.RIGHT)
        self.search_frame.pack(side=tk.LEFT)
        
        # Search Button
        self.search_button = tk.Button(self.search_frame,
                                       text="Search",
                                       command=lambda: uf.search(self.url_mediator, self.properties))
        self.search_button.pack(padx=5, pady=8, anchor="center")

        # Recommend Button
        self.recommend_button = tk.Button(self.recommend_frame, 
                                    text="Recommendations", 
                                    command=lambda: self.start_recommender(self.properties))
        self.recommend_button.pack(padx=5, pady=8, anchor="center")

        # Advanced Properties Check Boolean
        self.advanced_properties_var = tk.BooleanVar(value=False)

        self.toggle_properties_widget = {
            'title_label': self.title_label,
            'advanced_properties_var': self.advanced_properties_var,
            'additional_properties_frame': self.additional_properties_frame,
            'bottom_frame': self.bottom_frame
        }

        # Advanced Properties Check Button
        self.advanced_properties_checkbox = tk.Checkbutton(self.root, text="Show Advanced Properties", 
                                                    variable=self.advanced_properties_var, 
                                                    command=lambda: uf.toggle_advanced_properties(self.toggle_properties_widget, self.properties))


        self.handle_scan_widget = {
            'title_label': self.title_label,
            'duration_label': self.duration_label,
            'image_label': self.image_label,
            'download_button': self.download_button,
            'advanced_properties_var': self.advanced_properties_var
        }

        # Scan Button
        scan_button = tk.Button(self.root, text="URL Search", command=lambda: uf.handle_scan(self.url_entry, self.handle_scan_widget, self.properties))

        # Packing in order
        scan_button.pack()
        self.title_label.pack()
        self.duration_label.pack()
        self.image_label.pack()
        self.advanced_properties_checkbox.pack()
        self.download_button.pack()

        pass
    
    def start_recommender(self, properties):
        self.recommender = RecommendUI(self.url_mediator)
        self.recommender.start_recommendation_ui(properties['Title'].get(),properties['Album Artist'].get())
        pass

    def update(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        uf.handle_scan(self.url_entry, self.handle_scan_widget, self.properties)
        pass

    def quit(self):
        print('Leaving converter')
        self.root.quit()
        pass
    
    def run(self):
        self.root.mainloop()