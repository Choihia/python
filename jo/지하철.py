import tkinter as tk
from tkinter import ttk, messagebox
import requests
from xml.etree import ElementTree

# 발급받은 API 키를 입력하세요
API_KEY = '4d796a4d5774726538344558747578'

def get_station_data():
    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/xml/StationDstncReqreTimeHm/1/278/"
    response = requests.get(url)
    if response.status_code == 200:
        return ElementTree.fromstring(response.content)
    return None

def parse_time_to_minutes(time_str):
    """Convert time string (MM:SS) to total minutes."""
    minutes, seconds = map(int, time_str.split(':'))
    return minutes + (seconds / 60)

def get_travel_time(start_station, end_station):
    tree = get_station_data()
    if not tree:
        return "Failed to retrieve data from the API."
    
    rows = tree.findall('.//row')
    
    start_found = False
    total_minutes = 0
    
    for row in rows:
        line = row.find('LINE').text
        if line != "1":
            continue  # Skip stations not on Line 1
        
        station_name = row.find('STATN_NM').text
        if station_name == start_station:
            start_found = True
            total_minutes = 0  # Reset the total time calculation
        
        if start_found:
            minutes_str = row.find('MNT').text
            total_minutes += parse_time_to_minutes(minutes_str)
            
            if station_name == end_station:
                hours = int(total_minutes) // 60
                minutes = int(total_minutes) % 60
                return f"The travel time from {start_station} to {end_station} is approximately {hours} hours and {minutes} minutes."
    
    return "No route information available or invalid station names."

def on_submit():
    start_station = start_entry.get()
    end_station = end_entry.get()
    travel_time = get_travel_time(start_station, end_station)
    messagebox.showinfo("Travel Time", travel_time)

# GUI 설정
root = tk.Tk()
root.title("1호선 지하철 이동시간 계산기")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

start_label = ttk.Label(frame, text="출발역:")
start_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

start_entry = ttk.Entry(frame, width=20)
start_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

end_label = ttk.Label(frame, text="도착역:")
end_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

end_entry = ttk.Entry(frame, width=20)
end_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

submit_button = ttk.Button(frame, text="이동 시간 확인", command=on_submit)
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()