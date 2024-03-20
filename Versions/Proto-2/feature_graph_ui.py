import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import spotify_analysis as sa
import config as c

class FeatureGraphUI:
    def __init__(self):
        self.graph_window = tk.Toplevel()
        self.graph_window.title("Feature analysis")
        self.graph_window.protocol("WM_DELETE_WINDOW", self.destroy)

    def create_graph(self, features, similarity):
        similarity = round(similarity, 2)
        fig = sa.feature_plot2(c.CURRENT_TRACK_FEATURES, features, 8)

        self.text_frame = tk.Frame(self.graph_window)
        self.canvas_frame = tk.Frame(self.graph_window)
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.sim_label = tk.Label(self.text_frame, text=f"Similarity: {similarity}")
        self.close_button = tk.Button(self.text_frame, text='Close', command= self.destroy)
        self.sim_label.pack(side="left", padx=5, pady=5)
        self.close_button.pack(side=tk.RIGHT)

        self.text_frame.pack(side='top', fill = 'x')
        self.canvas_frame.pack(side='bottom', fill='both', expand=True)

        # Calculate window size based on widget sizes
        widget_width = self.canvas.get_width_height()[0]
        widget_height = self.close_button.winfo_reqheight() + self.canvas.get_width_height()[1]

        # Set window geometry to fit widgets
        window_width = 770 if widget_width > 770 else widget_width
        window_height = 800 if widget_height > 800 else widget_height
        self.graph_window.geometry(f"{window_width}x{window_height}")
        self.graph_window.update()

        return None

    def destroy(self):
        if self.graph_window: 
            self.graph_window.destroy()
            print('Graph destroyed')
        else: pass
