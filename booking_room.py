import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        booked_by TEXT NOT NULL,
        supplier_name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)

def book_meeting(conn, booked_by, supplier_name, date, time):
    sql_insert_meeting = """
    INSERT INTO meetings (booked_by, supplier_name, date, time)
    VALUES (?, ?, ?, ?)
    """
    try:
        c = conn.cursor()
        c.execute(sql_insert_meeting, (booked_by, supplier_name, date, time))
        conn.commit()
        messagebox.showinfo("Success", "Booking successful!")
    except sqlite3.Error as e:
        print(e)

def display_meetings_sorted(conn, tree):
    tree.delete(*tree.get_children())
    sql_select_all_sorted = """
    SELECT * FROM meetings ORDER BY date DESC
    """
    try:
        c = conn.cursor()
        c.execute(sql_select_all_sorted)
        rows = c.fetchall()
        
        for row in rows:
            tree.insert("", 0, values=row) 
    except sqlite3.Error as e:
        print(e)

def delete_meeting(conn, meeting_id):
    sql_delete_meeting = """
    DELETE FROM meetings WHERE id=?
    """
    try:
        c = conn.cursor()
        c.execute(sql_delete_meeting, (meeting_id,))
        conn.commit()
        messagebox.showinfo("Success", "Meeting deleted successfully.")
    except sqlite3.Error as e:
        print(e)

def update_meeting(conn, meeting_id, booked_by, supplier_name, date, time):
    sql_update_meeting = """
    UPDATE meetings SET booked_by=?, supplier_name=?, date=?, time=? WHERE id=?
    """
    try:
        c = conn.cursor()
        c.execute(sql_update_meeting, (booked_by, supplier_name, date, time, meeting_id))
        conn.commit()
        messagebox.showinfo("Success", "Meeting updated successfully.")
    except sqlite3.Error as e:
        print(e)

def book_meeting_handler():
    booked_by = entry_booked_by.get()
    supplier_name = entry_supplier_name.get()
    date = cal_date.get_date()  
    hour = combo_hour.get()   
    minute = combo_minute.get()
    
    if booked_by == "" or supplier_name == "" or date == "" or hour == "" or minute == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    time = f"{hour}:{minute}"
    book_meeting(conn, booked_by, supplier_name, date, time)
    display_meetings_sorted(conn, tree) 
    clear_fields()

def delete_meeting_handler():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a meeting to delete.")
        return
    
    meeting_id = tree.item(selected_item)['values'][0]
    delete_meeting(conn, meeting_id)
    display_meetings_sorted(conn, tree) 

def edit_meeting_handler():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a meeting to edit.")
        return
    
    meeting_id = tree.item(selected_item)['values'][0]
    booked_by = entry_booked_by.get()
    supplier_name = entry_supplier_name.get()
    date = cal_date.get_date()  
    hour = combo_hour.get()     
    minute = combo_minute.get()
    
    if booked_by == "" or supplier_name == "" or date == "" or hour == "" or minute == "":
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    
    time = f"{hour}:{minute}"
    update_meeting(conn, meeting_id, booked_by, supplier_name, date, time)
    display_meetings_sorted(conn, tree)  
    clear_fields()

def clear_fields():
    entry_booked_by.delete(0, tk.END)
    entry_supplier_name.delete(0, tk.END)
    cal_date.set_date(datetime.now())  
    combo_hour.set("")     
    combo_minute.set("")

def init_gui():
    global conn, tree, entry_booked_by, entry_supplier_name, cal_date, combo_hour, combo_minute
    
    root = tk.Tk()
    root.title("Meeting Room Booking")
    root.geometry("1020x520") 
    root.resizable(False, False)
    
    # Warna untuk elemen GUI
    background_color = "#ffe6f2" 
    accent_color = "#ff69b4"    
    text_color = "#ffffff"     
    
    conn = create_connection("meeting.db")
    create_table(conn)
    
    root.config(bg=background_color)
    
    label_booked_by = tk.Label(root, text="Booked by:", bg=background_color, fg=accent_color)
    label_booked_by.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    entry_booked_by = tk.Entry(root)
    entry_booked_by.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
    
    label_supplier_name = tk.Label(root, text="Supplier Name:", bg=background_color, fg=accent_color)
    label_supplier_name.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    entry_supplier_name = tk.Entry(root)
    entry_supplier_name.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
    
    label_date = tk.Label(root, text="Date:", bg=background_color, fg=accent_color)
    label_date.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    cal_date = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2)
    cal_date.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
    
    label_hour = tk.Label(root, text="Hour:", bg=background_color, fg=accent_color)
    label_hour.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    combo_hour = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(24)], state="readonly", width=5)
    combo_hour.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
    
    label_minute = tk.Label(root, text="Minute:", bg=background_color, fg=accent_color)
    label_minute.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    combo_minute = ttk.Combobox(root, values=[str(i).zfill(2) for i in range(60)], state="readonly", width=5)
    combo_minute.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
    
    btn_book_meeting = tk.Button(root, text="Book Meeting Room", bg=accent_color, fg=text_color, command=book_meeting_handler)
    btn_book_meeting.grid(row=5, column=0, padx=10, pady=10)
    
    tree_frame = tk.Frame(root, bg=background_color)
    tree_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
    
    tree = ttk.Treeview(tree_frame, columns=("ID", "Booked By", "Supplier Name", "Date", "Time"), show="headings", height=10)
    tree.heading("ID", text="ID")
    tree.heading("Booked By", text="Booked By")
    tree.heading("Supplier Name", text="Supplier Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.column("ID", anchor=tk.CENTER)       
    tree.column("Booked By", anchor=tk.CENTER) 
    tree.column("Supplier Name", anchor=tk.CENTER) 
    tree.column("Date", anchor=tk.CENTER)    
    tree.column("Time", anchor=tk.CENTER)   
    tree.pack(fill=tk.BOTH, expand=True)
    
    btn_delete_meeting = tk.Button(root, text="Delete Meeting", bg=accent_color, fg=text_color, command=delete_meeting_handler)
    btn_delete_meeting.grid(row=7, column=0, padx=10, pady=10)
    
    btn_edit_meeting = tk.Button(root, text="Edit Meeting", bg=accent_color, fg=text_color, command=edit_meeting_handler)
    btn_edit_meeting.grid(row=7, column=1, padx=10, pady=10)
    
    credit_label = tk.Label(root, text="IT Division @2024", bg=background_color, fg=accent_color, font=("Arial", 10, "italic"))
    credit_label.grid(row=8, column=0, columnspan=2, pady=10)
    
    display_meetings_sorted(conn, tree) 
    root.mainloop()

if __name__ == "__main__":
    init_gui()
