import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"

def view_rooms():
    response = requests.get(f"{BASE_URL}/rooms")
    rooms = response.json()
    text = "\n".join([f"Room ID: {r['id']}, Type: {r['type']}, Price: ₹{r['price']}" for r in rooms])
    messagebox.showinfo("Available Rooms", text if text else "No rooms available.")

def book_room():
    user_id = user_id_entry.get()
    room_id = room_id_entry.get()
    start = start_date.get()
    end = end_date.get()

    if not user_id or not room_id or not start or not end:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        response = requests.post("http://127.0.0.1:5000/book", json={
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

tk.Label(root, text="User ID").grid(row=0, column=0)
entry_user_id = tk.Entry(root)
entry_user_id.grid(row=0, column=1)

tk.Label(root, text="Room ID").grid(row=1, column=0)
entry_room_id = tk.Entry(root)
entry_room_id.grid(row=1, column=1)

tk.Label(root, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0)
entry_start_date = tk.Entry(root)
entry_start_date.grid(row=2, column=1)

tk.Label(root, text="End Date (YYYY-MM-DD)").grid(row=3, column=0)
entry_end_date = tk.Entry(root)
entry_end_date.grid(row=3, column=1)

tk.Button(root, text="View Rooms", command=view_rooms).grid(row=4, column=0, pady=5)
tk.Button(root, text="Book Room", command=book_room).grid(row=4, column=1, pady=5)
tk.Button(root, text="View Bookings", command=view_bookings).grid(row=5, column=0, pady=5)

# 🔴 Cancel Booking Section
tk.Label(root, text="Cancel Booking ID").grid(row=6, column=0)
entry_cancel_id = tk.Entry(root)
entry_cancel_id.grid(row=6, column=1)

tk.Button(root, text="Cancel Booking", command=cancel_booking).grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
