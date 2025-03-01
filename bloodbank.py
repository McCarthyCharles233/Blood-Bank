import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2  # type: ignore
from datetime import datetime

# Database connection
def connect_db():
    return psycopg2.connect(
        dbname="blood_bank",
        user="postgres",
        password="123",  
        host="localhost",
        port="5432"
    )

# Fetch blood bank data
def fetch_blood_bank_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BloodBank")
    data = cursor.fetchall()
    conn.close()
    return data

# Update blood bank data
def update_blood_bank(blood_group, units):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE BloodBank SET units_available = %s WHERE blood_group = %s", (units, blood_group))
    conn.commit()
    conn.close()

# Welcome Screen
def welcome_screen():
    welcome_window = tk.Tk()
    welcome_window.title("Blood Bank Management System")
    welcome_window.geometry("400x300")

    # Add a welcome heading
    heading_label = tk.Label(welcome_window, text="Blood Bank Management System", font=("Arial", 16, "bold"))
    heading_label.pack(pady=20)

    # Add a description
    description_label = tk.Label(welcome_window,
                                 text="Welcome to the Blood Bank Management System.\nPlease log in to continue.",
                                 font=("Arial", 12))
    description_label.pack(pady=20)

    # Admin login button
    def open_admin_login():
        welcome_window.destroy()
        admin_login()

    # Define button and ensure text is black if fg='white' doesn't work
    login_button = tk.Button(welcome_window, text="Admin Login", command=open_admin_login,
                             font=("Arial", 12), width=15, height=2)
    login_button.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
    login_button.pack(pady=30)

    welcome_window.mainloop()

# Admin Login Window
def admin_login():
    def validate_login():
        username = entry_username.get()
        password = entry_password.get()

        # Check for empty fields
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        if username == "admin" and password == "admin123":
            login_window.destroy()
            homepage()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Admin Login")
    login_window.geometry("400x300")

    # Create a frame for the login form
    login_frame = tk.Frame(login_window, padx=20, pady=20)
    login_frame.pack(expand=True)

    # Title
    title_label = tk.Label(login_frame, text="Admin Login", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Username
    tk.Label(login_frame, text="Username:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=10)
    entry_username = tk.Entry(login_frame, font=("Arial", 12), width=20)
    entry_username.grid(row=1, column=1, pady=10)

    # Password
    tk.Label(login_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=10)
    entry_password = tk.Entry(login_frame, show="*", font=("Arial", 12), width=20)
    entry_password.grid(row=2, column=1, pady=10)

    # Login button with fixed contrast
    login_btn = tk.Button(login_frame, text="Login", command=validate_login, font=("Arial", 12), width=10)
    login_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
    login_btn.grid(row=3, column=0, columnspan=2, pady=20)

    # Bind Enter key to login function
    login_window.bind('<Return>', lambda event: validate_login())

    # Set focus to username entry
    entry_username.focus()

    # Back button
    def go_back():
        login_window.destroy()
        welcome_screen()

    back_btn = tk.Button(login_window, text="Back", command=go_back, font=("Arial", 10))
    back_btn.configure(bg="#f0f0f0", fg="black", activebackground="#e0e0e0", activeforeground="black")
    back_btn.pack(side=tk.BOTTOM, pady=10)

    login_window.mainloop()

# Homepage
def homepage():
    def donate_blood():
        donate_window = tk.Toplevel()
        donate_window.title("Donate Blood")
        donate_window.geometry("350x300")

        # Create a frame for the form
        form_frame = tk.Frame(donate_window, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)

        # Blood Group Dropdown
        tk.Label(form_frame, text="Blood Group:").grid(row=0, column=0, sticky="w", pady=10)
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        blood_group_var = tk.StringVar()
        blood_group_dropdown = ttk.Combobox(form_frame, textvariable=blood_group_var, values=blood_groups, state="readonly", width=15)
        blood_group_dropdown.grid(row=0, column=1, pady=10, padx=10)
        blood_group_dropdown.current(0)  # Set default value

        # Units Donated
        tk.Label(form_frame, text="Units Donated:").grid(row=1, column=0, sticky="w", pady=10)
        entry_units = tk.Entry(form_frame, width=15)
        entry_units.grid(row=1, column=1, pady=10, padx=10)

        # Date of Donation
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=10)
        entry_date = tk.Entry(form_frame, width=15)
        entry_date.grid(row=2, column=1, pady=10, padx=10)
        entry_date.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default to today's date

        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        def submit_donation():
            blood_group = blood_group_var.get()
            try:
                units = int(entry_units.get())
                if units <= 0:
                    messagebox.showerror("Error", "Units must be a positive number")
                    return
                date = entry_date.get()
                if not date:
                    messagebox.showerror("Error", "Date cannot be empty")
                    return
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE BloodBank SET units_available = units_available + %s WHERE blood_group = %s", (units, blood_group))
                cursor.execute("INSERT INTO Donations (blood_group, units_donated, donation_date) VALUES (%s, %s, %s)",
                               (blood_group, units, date))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Donation recorded successfully!")
                donate_window.destroy()
                refresh_table()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for units")

        def cancel_donation():
            donate_window.destroy()

        # Save button with fixed contrast
        save_btn = tk.Button(button_frame, text="Save", command=submit_donation, width=8, font=("Arial", 11))
        save_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
        save_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button with fixed contrast
        cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_donation, width=8, font=("Arial", 11))
        cancel_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def request_blood():
        request_window = tk.Toplevel()
        request_window.title("Request Blood")
        request_window.geometry("350x300")

        # Create a frame for the form
        form_frame = tk.Frame(request_window, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)

        # Blood Group Dropdown
        tk.Label(form_frame, text="Blood Group:").grid(row=0, column=0, sticky="w", pady=10)
        blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        blood_group_var = tk.StringVar()
        blood_group_dropdown = ttk.Combobox(form_frame, textvariable=blood_group_var, values=blood_groups, state="readonly", width=15)
        blood_group_dropdown.grid(row=0, column=1, pady=10, padx=10)
        blood_group_dropdown.current(0)  # Set default value

        # Units Required
        tk.Label(form_frame, text="Units Required:").grid(row=1, column=0, sticky="w", pady=10)
        entry_units = tk.Entry(form_frame, width=15)
        entry_units.grid(row=1, column=1, pady=10, padx=10)

        # Date of Request
        tk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=10)
        entry_date = tk.Entry(form_frame, width=15)
        entry_date.grid(row=2, column=1, pady=10, padx=10)
        entry_date.insert(0, datetime.today().strftime('%Y-%m-%d'))  # Default to today's date

        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        def submit_request():
            blood_group = blood_group_var.get()
            try:
                units = int(entry_units.get())
                if units <= 0:
                    messagebox.showerror("Error", "Units must be a positive number")
                    return
                date = entry_date.get()
                if not date:
                    messagebox.showerror("Error", "Date cannot be empty")
                    return
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT units_available FROM BloodBank WHERE blood_group = %s", (blood_group,))
                available_units = cursor.fetchone()[0]
                if available_units >= units:
                    cursor.execute("UPDATE BloodBank SET units_available = units_available - %s WHERE blood_group = %s", (units, blood_group))
                    cursor.execute("INSERT INTO Requests (blood_group, units_requested, request_date) VALUES (%s, %s, %s)",
                                   (blood_group, units, date))
                    conn.commit()
                    messagebox.showinfo("Success", "Blood request fulfilled!")
                else:
                    messagebox.showerror("Error", f"Insufficient blood units available! Only {available_units} units of {blood_group} in stock.")
                conn.close()
                request_window.destroy()
                refresh_table()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for units")

        def cancel_request():
            request_window.destroy()

        # Save button with fixed contrast
        save_btn = tk.Button(button_frame, text="Save", command=submit_request, width=8, font=("Arial", 11))
        save_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
        save_btn.pack(side=tk.LEFT, padx=10)

        # Cancel button with fixed contrast
        cancel_btn = tk.Button(button_frame, text="Cancel", command=cancel_request, width=8, font=("Arial", 11))
        cancel_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def view_history():
        history_window = tk.Toplevel()
        history_window.title("Donation and Request History")
        history_window.geometry("800x400")

        # Create a notebook for tabs
        notebook = ttk.Notebook(history_window)
        notebook.pack(fill="both", expand=True)

        # Donation History Tab
        donation_frame = tk.Frame(notebook)
        notebook.add(donation_frame, text="Donation History")

        donation_tree = ttk.Treeview(donation_frame, columns=("Blood Group", "Units Donated", "Date"), show="headings")
        donation_tree.heading("Blood Group", text="Blood Group")
        donation_tree.heading("Units Donated", text="Units Donated")
        donation_tree.heading("Date", text="Date")
        donation_tree.column("Blood Group", width=150, anchor=tk.CENTER)
        donation_tree.column("Units Donated", width=150, anchor=tk.CENTER)
        donation_tree.column("Date", width=150, anchor=tk.CENTER)
        donation_tree.pack(fill="both", expand=True, padx=10, pady=10)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT blood_group, units_donated, donation_date FROM Donations")
        donations = cursor.fetchall()
        for donation in donations:
            donation_tree.insert("", "end", values=donation)
        conn.close()

        # Request History Tab
        request_frame = tk.Frame(notebook)
        notebook.add(request_frame, text="Request History")

        request_tree = ttk.Treeview(request_frame, columns=("Blood Group", "Units Requested", "Date"), show="headings")
        request_tree.heading("Blood Group", text="Blood Group")
        request_tree.heading("Units Requested", text="Units Requested")
        request_tree.heading("Date", text="Date")
        request_tree.column("Blood Group", width=150, anchor=tk.CENTER)
        request_tree.column("Units Requested", width=150, anchor=tk.CENTER)
        request_tree.column("Date", width=150, anchor=tk.CENTER)
        request_tree.pack(fill="both", expand=True, padx=10, pady=10)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT blood_group, units_requested, request_date FROM Requests")
        requests = cursor.fetchall()
        for request in requests:
            request_tree.insert("", "end", values=request)
        conn.close()

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        data = fetch_blood_bank_data()
        for row in data:
            tree.insert("", "end", values=row)

    def logout():
        root.destroy()
        welcome_screen()

    root = tk.Tk()
    root.title("Blood Bank Management System")
    root.geometry("600x400")

    # Create header
    header_label = tk.Label(root, text="Blood Bank Management System", font=("Arial", 16, "bold"))
    header_label.pack(pady=10)

    # Treeview to display blood bank data
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=10, fill="both", expand=True)

    tree_scroll = tk.Scrollbar(tree_frame)
    tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(tree_frame, columns=("Blood Group", "Units Available"), show="headings", yscrollcommand=tree_scroll.set)
    tree.heading("Blood Group", text="Blood Group")
    tree.heading("Units Available", text="Units Available")
    tree.column("Blood Group", width=150, anchor=tk.CENTER)
    tree.column("Units Available", width=150, anchor=tk.CENTER)
    tree.pack(side=tk.LEFT, fill="both", expand=True)

    tree_scroll.config(command=tree.yview)

    refresh_table()

    # Frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=15, padx=10)

    # Buttons with improved visibility and explicit contrast settings
    donate_btn = tk.Button(button_frame, text="Donate Blood", command=donate_blood,
                           font=("Arial", 11), width=12, height=1)
    donate_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
    donate_btn.pack(side=tk.LEFT, padx=10)

    request_btn = tk.Button(button_frame, text="Request Blood", command=request_blood,
                            font=("Arial", 11), width=12, height=1)
    request_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
    request_btn.pack(side=tk.LEFT, padx=10)

    history_btn = tk.Button(button_frame, text="View History", command=view_history,
                            font=("Arial", 11), width=12, height=1)
    history_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
    history_btn.pack(side=tk.LEFT, padx=10)

    logout_btn = tk.Button(button_frame, text="Logout", command=logout, 
                         font=("Arial", 11), width=8, height=1)
    logout_btn.configure(bg="grey", fg="black", activebackground="grey", activeforeground="black")
    logout_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()

# Main Program
if __name__ == "__main__":
    welcome_screen()