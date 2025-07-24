import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import requests

BASE_URL = "http://127.0.0.1:5000"

def view_rooms():
    response = requests.get(f"{BASE_URL}/rooms")
    rooms = response.json()
    text = "\n".join([f"Room ID: {r['id']}, Type: {r['type']}, Price: ₹{r['price']}" for r in rooms])
    messagebox.showinfo("Available Rooms", text if text else "No rooms available.")

def book_room():
    user_id = entry_user_id.get()
    room_id = entry_room_id.get()
    start = entry_start_date.get()
    end = entry_end_date.get()

    if not user_id or not room_id or not start or not end:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        response = requests.post(f"{BASE_URL}/book", json={
            "user_id": int(user_id),
            "room_id": int(room_id),
            "start_date": start,
            "end_date": end
        })

        if response.status_code == 200:
            data = response.json()
            messagebox.showinfo("Success", data.get("message", "Room booked successfully!"))
        else:
            try:
                error = response.json().get("message", "Booking failed.")
            except:
                error = f"Booking failed. Status: {response.status_code}"
            messagebox.showerror("Failed", error)

    except Exception as e:
        messagebox.showerror("Error", f"Request failed: {str(e)}")

def cancel_booking():
    booking_id = entry_cancel_id.get()
    if not booking_id:
        messagebox.showwarning("Input Error", "Please enter Booking ID to cancel")
        return
    response = requests.delete(f"{BASE_URL}/cancel/{booking_id}")
    messagebox.showinfo("Cancel Booking", response.json().get("message", "Unknown response"))

def view_bookings():
    response = requests.get(f"{BASE_URL}/bookings")
    bookings = response.json()
    text = "\n".join([f"Booking ID: {b['id']}, User ID: {b['user_id']}, Room ID: {b['room_id']}" for b in bookings])
    messagebox.showinfo("All Bookings", text if text else "No bookings yet.")

# GUI setup
root = tk.Tk()
root.title("🏨 Hotel Booking System")

# Window size and center
window_width = 900
window_height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 🔹 Background image
bg_image = Image.open("photo/pexels-pixabay-271639.jpg") 
bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# 🔹 Center Frame
main_frame = tk.Frame(root, bg="#ffffff", bd=2)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

font_style = ("Arial", 14)  # 🔸 Common font for all

# 🔹 Labels & Entries with spacing
tk.Label(main_frame, text="User ID", font=font_style).grid(row=0, column=0, sticky="w", padx=12, pady=12)
entry_user_id = tk.Entry(main_frame, width=30, font=font_style)
entry_user_id.grid(row=0, column=1, pady=12)

tk.Label(main_frame, text="Room ID", font=font_style).grid(row=1, column=0, sticky="w", padx=12, pady=12)
entry_room_id = tk.Entry(main_frame, width=30, font=font_style)
entry_room_id.grid(row=1, column=1, pady=12)

tk.Label(main_frame, text="Start Date (YYYY-MM-DD)", font=font_style).grid(row=2, column=0, sticky="w", padx=12, pady=12)
entry_start_date = tk.Entry(main_frame, width=30, font=font_style)
entry_start_date.grid(row=2, column=1, pady=12)

tk.Label(main_frame, text="End Date (YYYY-MM-DD)", font=font_style).grid(row=3, column=0, sticky="w", padx=12, pady=12)
entry_end_date = tk.Entry(main_frame, width=30, font=font_style)
entry_end_date.grid(row=3, column=1, pady=12)

# 🔹 Action Buttons
tk.Button(main_frame, text="View Rooms", command=view_rooms, font=font_style, width=20).grid(row=4, column=0, pady=12)
tk.Button(main_frame, text="Book Room", command=book_room, font=font_style, width=20).grid(row=4, column=1, pady=12)

tk.Button(main_frame, text="View Bookings", command=view_bookings, font=font_style, width=43).grid(row=5, column=0, columnspan=2, pady=12)

# 🔹 Cancel Booking
tk.Label(main_frame, text="Cancel Booking ID", font=font_style).grid(row=6, column=0, sticky="w", padx=12, pady=12)
entry_cancel_id = tk.Entry(main_frame, width=30, font=font_style)
entry_cancel_id.grid(row=6, column=1, pady=12)

tk.Button(main_frame, text="Cancel Booking", command=cancel_booking, font=font_style, width=43).grid(row=7, column=0, columnspan=2, pady=16)

root.mainloop()
