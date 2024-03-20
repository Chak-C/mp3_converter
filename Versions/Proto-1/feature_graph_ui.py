import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import spotify_analysis as sa
import config as c

_graph_window = ''

def create_graph(features, similarity):
    global _graph_window

    similarity = round(similarity, 2)
    fig = sa.feature_plot2(c.CURRENT_TRACK_FEATURES, features, 8)

    _graph_window = tk.Toplevel()
    _graph_window.title("Feature analysis")
    _graph_window.protocol("WM_DELETE_WINDOW", _graph_window.destroy)

    text_frame = tk.Frame(_graph_window)
    canvas_frame = tk.Frame(_graph_window)
    
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    sim_label = tk.Label(text_frame, text=f"Similarity: {similarity}")
    close_button = tk.Button(text_frame, text='Close', command=_graph_window.destroy)
    sim_label.pack(side="left", padx=5, pady=5)
    close_button.pack(side=tk.RIGHT)

    text_frame.pack(side='top', fill = 'x')
    canvas_frame.pack(side='bottom', fill='both', expand=True)

    # Calculate window size based on widget sizes
    widget_width = canvas.get_width_height()[0]
    widget_height = close_button.winfo_reqheight() + canvas.get_width_height()[1]

    # Set window geometry to fit widgets
    window_width = 770 if widget_width > 770 else widget_width
    window_height = 800 if widget_height > 800 else widget_height
    _graph_window.geometry(f"{window_width}x{window_height}")
    _graph_window.update()

    return None

def destroy():
    global _graph_window
    if _graph_window: 
        _graph_window.destroy()
        print('Graph destroyed')
    else: pass
