import socket
import threading
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from matplotlib.figure import Figure
# Client.py
# This script connects to a server, receives ADC data, and plots it in real-time using Tkinter and Matplotlib.
import matplotlib.pyplot as plt

HOST = '127.0.0.1'
PORT = 12345
data_points = []

def receive_data():
    global data_points
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    buffer = ""
    while True:
        try:
            buffer += s.recv(1024).decode()
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if line.strip().isdigit() or '.' in line:
                    data_points.append(float(line.strip()))
                    update_plot()
        except:
            break

def update_plot():
    ax.clear()
    ax.plot(data_points[-100:], color='blue')
    ax.set_title("Real-time ADC Signal")
    ax.set_ylabel("Amplitude")
    ax.set_xlabel("Sample")
    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("Client ADC Plot")
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
threading.Thread(target=receive_data, daemon=True).start()
root.mainloop()