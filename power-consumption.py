import psutil
import time
import csv
import tkinter as tk
root = tk.Tk()
monitoring=False
root.title("Power Consumption and Activity Monitor")
interval_label = tk.Label(root, text="Monitoring Interval (in seconds):")
interval_label.grid(row=0, column=0, padx=5, pady=5)
interval_input = tk.Entry(root, width=10)
interval_input.grid(row=0, column=1, padx=5, pady=5)
count_label = tk.Label(root, text="Number of Intervals to Monitor:")
count_label.grid(row=1, column=0, padx=5, pady=5)
count_input = tk.Entry(root, width=10)
count_input.grid(row=1, column=1, padx=5, pady=5)
battery_label = tk.Label(root, text="Battery Percentage:")
battery_label.grid(row=2, column=0, padx=5, pady=5)
cpu_label = tk.Label(root, text="CPU Usage:")
cpu_label.grid(row=3, column=0, padx=5, pady=5)
memory_label = tk.Label(root, text="Memory Usage:")
memory_label.grid(row=4, column=0, padx=5, pady=5)
battery_text = tk.Text(root, height=1, width=10)
battery_text.grid(row=2, column=1, padx=5, pady=5)
cpu_text = tk.Text(root, height=1, width=10)
cpu_text.grid(row=3, column=1, padx=5, pady=5)
memory_text = tk.Text(root, height=2, width=20)
memory_text.grid(row=4, column=1, padx=5, pady=5)
def start_monitoring():
    monitor_interval = int(interval_input.get())
    monitor_count = int(count_input.get())
    with open('monitoring_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Battery Percentage', 'CPU Usage', 'Used Memory', 'Free Memory'])
        for i in range(monitor_count):
            power_usage = psutil.sensors_battery()
            if power_usage:
                battery_percentage = power_usage.percent
                battery_text.delete("1.0", tk.END)
                battery_text.insert(tk.END, f"{battery_percentage}%")
            cpu_usage = psutil.cpu_percent()
            cpu_text.delete("1.0", tk.END)
            cpu_text.insert(tk.END, f"{cpu_usage}%")
            memory_usage = psutil.virtual_memory()
            used_memory = memory_usage.used
            free_memory = memory_usage.available
            memory_text.delete("1.0", tk.END)
            memory_text.insert(tk.END, f"{used_memory/1024/1024:.2f} MB / {free_memory/1024/1024:.2f} MB")
            writer.writerow([battery_percentage, cpu_usage, used_memory, free_memory])
            time.sleep(monitor_interval)
            if not monitoring:
                break
    interval_input.config(state="normal")
    count_input.config(state="normal")
    start_button.config(state="normal")
    stop_button.config(state="disabled")
def stop_monitoring():
    global monitoring
    monitoring = False
start_button = tk.Button(root, text="Start", command=start_monitoring)
start_button.grid(row=5, column=0, padx=5, pady=5)
stop_button = tk.Button(root, text="Stop", command=stop_monitoring, state="disabled")
stop_button.grid(row=5, column=1, padx=5, pady=5)
root.mainloop()
