import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import datetime

# ============================================================
# BUDGET MANAGEMENT SYSTEM
# One program containing all pages + SQLite database
# ============================================================

DB_NAME = "budget_management.db"

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# ---------------- DATABASE ----------------

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT DEFAULT '',
            email TEXT DEFAULT ''
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            entry_date TEXT NOT NULL,
            income REAL DEFAULT 0,
            food REAL DEFAULT 0,
            transport REAL DEFAULT 0,
            shopping REAL DEFAULT 0,
            bills REAL DEFAULT 0,
            education REAL DEFAULT 0,
            health REAL DEFAULT 0,
            entertainment REAL DEFAULT 0,
            other REAL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ---------------- MAIN APPLICATION ----------------

class BudgetApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Budget Planner")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        # Full screen
        self.after(100, self.make_fullscreen)

        self.green_dark = "#315C45"
        self.green = "#4F8A68"
        self.green_light = "#DDEFE4"
        self.green_pale = "#F2F8F4"
        self.text_dark = "#20352A"
        self.white = "#FFFFFF"

        self.current_user_id = None
        self.current_username = None
        self.current_page = None

        self.pages = {}

        self.create_login_page()
        self.create_signup_page()
        self.create_welcome_page()
        self.create_front_page()
        self.create_dashboard_page()
        self.create_admin_dashboard_page()
        self.create_spending_page()
        self.create_budget_page()
        self.create_balance_page()
        self.create_graph_page()
        self.create_admin_login_page()
        self.create_admin_panel()

        self.show_page("welcome")

    def make_fullscreen(self):
        try:
            self.state("zoomed")
        except Exception:
            pass

    # ---------------- COMMON UI ----------------

    def clear_page(self, page):
        for widget in page.winfo_children():
            widget.destroy()

    def make_header(self, page, title, subtitle=""):
        header = ctk.CTkFrame(
            page,
            fg_color=self.green_dark,
            corner_radius=0,
            height=85
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.white
        ).pack(side="left", padx=35, pady=(15, 0))

        if subtitle:
            ctk.CTkLabel(
                header,
                text=subtitle,
                font=ctk.CTkFont(size=14),
                text_color="#DDEFE4"
            ).pack(side="left", padx=5, pady=(18, 0))

        return header

    def make_nav(self, page, buttons):
        nav = ctk.CTkFrame(page, fg_color=self.green_pale, corner_radius=0)
        nav.pack(fill="x", padx=0, pady=0)

        for text, command in buttons:
            ctk.CTkButton(
                nav,
                text=text,
                command=command,
                fg_color=self.green,
                hover_color=self.green_dark,
                text_color=self.white,
                height=35,
                corner_radius=8
            ).pack(side="left", padx=5, pady=8)

        ctk.CTkButton(
            nav,
            text="Logout",
            command=self.logout,
            fg_color="#6B806F",
            hover_color=self.green_dark,
            height=35,
            corner_radius=8
        ).pack(side="right", padx=10, pady=8)

        return nav

    def show_page(self, name):
        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[name]
        page.pack(fill="both", expand=True)
        self.current_page = name

        if name == "dashboard":
            self.refresh_dashboard()
        elif name == "spending":
            self.refresh_spending()
        elif name == "budget":
            self.refresh_budget()
        elif name == "balance":
            self.refresh_balance()
        elif name == "graph":
            self.refresh_graph()
        elif name == "admin_dashboard":
            self.refresh_admin_dashboard()
        elif name == "admin_panel":
            self.refresh_admin_panel()

    # =========================================================
    # WELCOME PAGE
    # =========================================================

    def create_welcome_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["welcome"] = page

        card = ctk.CTkFrame(
            page,
            fg_color=self.white,
            corner_radius=25,
            border_width=2,
            border_color=self.green
        )
        card.place(
            relx=0.5, rely=0.5, anchor="center",
            relwidth=0.68, relheight=0.72
        )

        ctk.CTkLabel(
            card,
            text="WELCOME",
            font=ctk.CTkFont(size=46, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(65, 5))

        ctk.CTkLabel(
            card,
            text="to Budget Planner",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=self.text_dark
        ).pack(pady=5)

        ctk.CTkLabel(
            card,
            text="Budget Management System",
            font=ctk.CTkFont(size=19),
            text_color="#607568"
        ).pack(pady=10)

        ctk.CTkLabel(
            card,
            text="Please choose how you want to continue.",
            font=ctk.CTkFont(size=15),
            text_color="#718277"
        ).pack(pady=(15, 25))

        buttons = ctk.CTkFrame(card, fg_color="transparent")
        buttons.pack()

        ctk.CTkButton(
            buttons,
            text="User",
            command=lambda: self.show_page("front"),
            width=210,
            height=50,
            fg_color=self.green,
            hover_color=self.green_dark,
            font=ctk.CTkFont(size=17, weight="bold")
        ).grid(row=0, column=0, padx=12, pady=10)

        ctk.CTkButton(
            buttons,
            text="Admin",
            command=lambda: self.show_page("admin_login"),
            width=210,
            height=50,
            fg_color=self.green_dark,
            hover_color=self.green,
            font=ctk.CTkFont(size=17, weight="bold")
        ).grid(row=0, column=1, padx=12, pady=10)

        ctk.CTkButton(
            card,
            text="Continue as User",
            command=lambda: self.show_page("login"),
            fg_color="#E8F2EC",
            hover_color=self.green_light,
            text_color=self.green_dark,
            width=180
        ).pack(pady=(25, 5))

    # =========================================================
    # FRONT PAGE
    # =========================================================

    def create_front_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["front"] = page

        center = ctk.CTkFrame(
            page,
            fg_color=self.white,
            corner_radius=25,
            border_width=2,
            border_color=self.green
        )
        center.place(relx=0.5, rely=0.5, anchor="center",
                     relwidth=0.65, relheight=0.65)

        ctk.CTkLabel(
            center,
            text="budget Planner",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(80, 10))

        ctk.CTkLabel(
            center,
            text="Budget Management System",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=self.text_dark
        ).pack(pady=5)

        ctk.CTkLabel(
            center,
            text="Manage income, expenses, savings and spending in one place.",
            font=ctk.CTkFont(size=16),
            text_color="#607568"
        ).pack(pady=10)

        ctk.CTkButton(
            center,
            text="Login",
            command=lambda: self.show_page("login"),
            width=220,
            height=48,
            fg_color=self.green,
            hover_color=self.green_dark,
            font=ctk.CTkFont(size=17, weight="bold")
        ).pack(pady=(35, 10))

        ctk.CTkButton(
            center,
            text="Create Account",
            command=lambda: self.show_page("signup"),
            width=220,
            height=48,
            fg_color=self.green_light,
            hover_color="#C8E1D1",
            text_color=self.green_dark,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)

        ctk.CTkButton(
            page,
            text="Admin",
            command=lambda: self.show_page("admin_login"),
            width=90,
            height=35,
            fg_color=self.green_dark,
            hover_color=self.green,
        ).place(relx=0.02, rely=0.95, anchor="sw")

        ctk.CTkButton(
            page,
            text="Skip",
            command=lambda: self.show_page("welcome"),
            width=90,
            height=35,
            fg_color=self.green_dark,
            hover_color=self.green,
        ).place(relx=0.98, rely=0.95, anchor="se")

    # =========================================================
    # LOGIN PAGE
    # =========================================================

    def create_login_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["login"] = page

        box = ctk.CTkFrame(
            page,
            fg_color=self.white,
            corner_radius=20,
            border_width=2,
            border_color=self.green
        )
        box.place(relx=0.5, rely=0.5, anchor="center",
                  relwidth=0.42, relheight=0.70)

        ctk.CTkLabel(
            box,
            text="Welcome Back",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(55, 8))

        ctk.CTkLabel(
            box,
            text="Login to your Budget Planner",
            text_color="#607568",
            font=ctk.CTkFont(size=15)
        ).pack(pady=(0, 30))

        self.login_username = ctk.CTkEntry(
            box, placeholder_text="Username", width=300, height=45
        )
        self.login_username.pack(pady=10)

        self.login_password = ctk.CTkEntry(
            box, placeholder_text="Password", show="*", width=300, height=45
        )
        self.login_password.pack(pady=10)

        ctk.CTkButton(
            box,
            text="Login",
            command=self.login_user,
            width=300,
            height=45,
            fg_color=self.green,
            hover_color=self.green_dark
        ).pack(pady=25)

        ctk.CTkButton(
            box,
            text="Create New Account",
            command=lambda: self.show_page("signup"),
            fg_color="transparent",
            text_color=self.green_dark,
            hover_color=self.green_light
        ).pack()

        ctk.CTkButton(
            box,
            text="Back",
            command=lambda: self.show_page("front"),
            fg_color="#E8F2EC",
            text_color=self.green_dark,
            hover_color=self.green_light,
            width=120
        ).pack(pady=15)

    def login_user(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showwarning("Missing information",
                                   "Please enter username and password.")
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username FROM users WHERE username=? AND password=?",
            (username, password)
        )
        row = cur.fetchone()
        conn.close()

        if row:
            self.current_user_id = row[0]
            self.current_username = row[1]
            self.show_page("dashboard")
        else:
            messagebox.showerror("Login failed",
                                 "Incorrect username or password.")

    # =========================================================
    # CREATE ACCOUNT
    # =========================================================

    def create_signup_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["signup"] = page

        box = ctk.CTkFrame(
            page,
            fg_color=self.white,
            corner_radius=20,
            border_width=2,
            border_color=self.green
        )
        box.place(relx=0.5, rely=0.5, anchor="center",
                  relwidth=0.45, relheight=0.82)

        ctk.CTkLabel(
            box,
            text="Create Account",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(35, 15))

        self.signup_name = ctk.CTkEntry(
            box, placeholder_text="Full Name", width=320, height=42
        )
        self.signup_name.pack(pady=7)

        self.signup_email = ctk.CTkEntry(
            box, placeholder_text="Email", width=320, height=42
        )
        self.signup_email.pack(pady=7)

        self.signup_username = ctk.CTkEntry(
            box, placeholder_text="Username", width=320, height=42
        )
        self.signup_username.pack(pady=7)

        self.signup_password = ctk.CTkEntry(
            box, placeholder_text="Password", show="*", width=320, height=42
        )
        self.signup_password.pack(pady=7)

        self.signup_confirm = ctk.CTkEntry(
            box, placeholder_text="Confirm Password",
            show="*", width=320, height=42
        )
        self.signup_confirm.pack(pady=7)

        ctk.CTkButton(
            box,
            text="Create Account",
            command=self.create_account,
            width=320,
            height=45,
            fg_color=self.green,
            hover_color=self.green_dark
        ).pack(pady=22)

        ctk.CTkButton(
            box,
            text="Back to Login",
            command=lambda: self.show_page("login"),
            fg_color="#E8F2EC",
            text_color=self.green_dark,
            hover_color=self.green_light,
            width=150
        ).pack()

    def create_account(self):
        name = self.signup_name.get().strip()
        email = self.signup_email.get().strip()
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()

        if not name or not email or not username or not password:
            messagebox.showwarning(
                "Missing information",
                "Please fill all fields."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password error",
                "Passwords do not match."
            )
            return

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO users(username, password, full_name, email)
                VALUES (?, ?, ?, ?)
            """, (username, password, name, email))
            conn.commit()
            messagebox.showinfo(
                "Account created",
                "Your account has been created successfully."
            )

            self.signup_name.delete(0, "end")
            self.signup_email.delete(0, "end")
            self.signup_username.delete(0, "end")
            self.signup_password.delete(0, "end")
            self.signup_confirm.delete(0, "end")

            self.show_page("login")

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Username exists",
                "That username is already registered."
            )

        finally:
            conn.close()

    # =========================================================
    # DASHBOARD
    # =========================================================

    def create_dashboard_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["dashboard"] = page

        self.dashboard_header = self.make_header(
            page,
            "Budget Planner",
            "Dashboard"
        )

        self.make_nav(page, [
            ("Dashboard", lambda: self.show_page("dashboard")),
            ("Spending", lambda: self.show_page("spending")),
            ("Budget", lambda: self.show_page("budget")),
            ("Balance", lambda: self.show_page("balance")),
            ("Expense Graph", lambda: self.show_page("graph")),
        ])

        body = ctk.CTkScrollableFrame(
            page,
            fg_color=self.green_pale
        )
        body.pack(fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(
            body,
            text="Enter Your Budget Information",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=self.green_dark
        ).pack(anchor="w", padx=15, pady=(5, 20))

        form = ctk.CTkFrame(
            body,
            fg_color=self.white,
            corner_radius=15
        )
        form.pack(fill="x", padx=10, pady=5)

        self.date_entry = ctk.CTkEntry(
            form, placeholder_text="Date (YYYY-MM-DD)", width=230, height=40
        )
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=0, padx=12, pady=15)

        self.income_entry = ctk.CTkEntry(
            form, placeholder_text="Total Income", width=230, height=40
        )
        self.income_entry.grid(row=0, column=1, padx=12, pady=15)

        categories = [
            ("Food", "food"),
            ("Transport", "transport"),
            ("Shopping", "shopping"),
            ("Bills", "bills"),
            ("Education", "education"),
            ("Health", "health"),
            ("Entertainment", "entertainment"),
            ("Other", "other")
        ]

        self.expense_entries = {}

        for i, (label, key) in enumerate(categories):
            row = 1 + i // 2
            col = (i % 2) * 2

            ctk.CTkLabel(
                form,
                text=label,
                text_color=self.text_dark,
                font=ctk.CTkFont(size=15, weight="bold")
            ).grid(row=row, column=col, padx=(20, 5), pady=10, sticky="e")

            entry = ctk.CTkEntry(
                form,
                placeholder_text="Enter amount",
                width=230,
                height=40
            )
            entry.grid(row=row, column=col + 1, padx=(5, 20), pady=10)
            self.expense_entries[key] = entry

        button_frame = ctk.CTkFrame(
            body, fg_color="transparent"
        )
        button_frame.pack(fill="x", padx=10, pady=20)

        ctk.CTkButton(
            button_frame,
            text="Add",
            command=self.add_budget,
            fg_color=self.green,
            hover_color=self.green_dark,
            width=130
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Update",
            command=self.update_budget,
            fg_color=self.green,
            hover_color=self.green_dark,
            width=130
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self.delete_budget,
            fg_color="#6B806F",
            hover_color=self.green_dark,
            width=130
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_budget_form,
            fg_color="#E8F2EC",
            text_color=self.green_dark,
            hover_color=self.green_light,
            width=130
        ).pack(side="left", padx=5)

        # Saved entries
        ctk.CTkLabel(
            body,
            text="Your Saved Budget Entries",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=self.green_dark
        ).pack(anchor="w", padx=15, pady=(10, 10))

        self.entries_frame = ctk.CTkFrame(
            body, fg_color=self.white, corner_radius=15
        )
        self.entries_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.selected_budget_id = None

    def safe_float(self, value):
        value = value.strip()
        if value == "":
            return 0.0
        try:
            number = float(value)
            if number < 0:
                raise ValueError
            return number
        except ValueError:
            raise ValueError("Amounts must be positive numbers.")

    def get_form_values(self):
        date = self.date_entry.get().strip()
        income = self.safe_float(self.income_entry.get())

        values = {
            "date": date,
            "income": income
        }

        for key, entry in self.expense_entries.items():
            values[key] = self.safe_float(entry.get())

        return values

    def add_budget(self):
        if not self.current_user_id:
            return

        try:
            data = self.get_form_values()
        except ValueError as e:
            messagebox.showerror("Invalid amount", str(e))
            return

        if not data["date"]:
            messagebox.showwarning("Missing date", "Please enter a date.")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO budgets(
                user_id, entry_date, income, food, transport, shopping,
                bills, education, health, entertainment, other
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.current_user_id,
            data["date"],
            data["income"],
            data["food"],
            data["transport"],
            data["shopping"],
            data["bills"],
            data["education"],
            data["health"],
            data["entertainment"],
            data["other"]
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Saved", "Budget information saved.")
        self.clear_budget_form()
        self.refresh_dashboard()

    def get_user_budgets(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, entry_date, income, food, transport, shopping,
                   bills, education, health, entertainment, other
            FROM budgets
            WHERE user_id=?
            ORDER BY id DESC
        """, (self.current_user_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def refresh_dashboard(self):
        if not self.current_user_id:
            return

        for widget in self.entries_frame.winfo_children():
            widget.destroy()

        rows = self.get_user_budgets()

        if not rows:
            ctk.CTkLabel(
                self.entries_frame,
                text="No budget entries yet. Enter your information above.",
                text_color="#607568",
                font=ctk.CTkFont(size=16)
            ).pack(pady=30)
            return

        for row in rows:
            (
                budget_id, date, income, food, transport, shopping,
                bills, education, health, entertainment, other
            ) = row

            total_expense = (
                food + transport + shopping + bills +
                education + health + entertainment + other
            )

            card = ctk.CTkFrame(
                self.entries_frame,
                fg_color=self.green_pale,
                corner_radius=12
            )
            card.pack(fill="x", padx=12, pady=8)

            ctk.CTkLabel(
                card,
                text=f"Date: {date}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.green_dark
            ).pack(side="left", padx=15, pady=12)

            ctk.CTkLabel(
                card,
                text=f"Income: ₹{income:,.2f}",
                text_color=self.text_dark
            ).pack(side="left", padx=15)

            ctk.CTkLabel(
                card,
                text=f"Expenses: ₹{total_expense:,.2f}",
                text_color=self.text_dark
            ).pack(side="left", padx=15)

            ctk.CTkButton(
                card,
                text="Select",
                width=80,
                height=30,
                command=lambda r=row: self.select_budget(r),
                fg_color=self.green,
                hover_color=self.green_dark
            ).pack(side="right", padx=12)

    def select_budget(self, row):
        (
            budget_id, date, income, food, transport, shopping,
            bills, education, health, entertainment, other
        ) = row

        self.selected_budget_id = budget_id

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, date)

        self.income_entry.delete(0, "end")
        self.income_entry.insert(0, str(income))

        values = {
            "food": food,
            "transport": transport,
            "shopping": shopping,
            "bills": bills,
            "education": education,
            "health": health,
            "entertainment": entertainment,
            "other": other
        }

        for key, value in values.items():
            self.expense_entries[key].delete(0, "end")
            self.expense_entries[key].insert(0, str(value))

        messagebox.showinfo(
            "Selected",
            "This budget entry is selected. You can now update or delete it."
        )

    def update_budget(self):
        if not self.selected_budget_id:
            messagebox.showwarning(
                "No selection",
                "Select a budget entry first."
            )
            return

        try:
            data = self.get_form_values()
        except ValueError as e:
            messagebox.showerror("Invalid amount", str(e))
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE budgets
            SET entry_date=?, income=?, food=?, transport=?, shopping=?,
                bills=?, education=?, health=?, entertainment=?, other=?
            WHERE id=? AND user_id=?
        """, (
            data["date"],
            data["income"],
            data["food"],
            data["transport"],
            data["shopping"],
            data["bills"],
            data["education"],
            data["health"],
            data["entertainment"],
            data["other"],
            self.selected_budget_id,
            self.current_user_id
        ))

        conn.commit()
        conn.close()

        self.selected_budget_id = None
        self.clear_budget_form()
        self.refresh_dashboard()
        messagebox.showinfo("Updated", "Budget entry updated.")

    def delete_budget(self):
        if not self.selected_budget_id:
            messagebox.showwarning(
                "No selection",
                "Select a budget entry first."
            )
            return

        if not messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this entry?"
        ):
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM budgets WHERE id=? AND user_id=?",
            (self.selected_budget_id, self.current_user_id)
        )
        conn.commit()
        conn.close()

        self.selected_budget_id = None
        self.clear_budget_form()
        self.refresh_dashboard()

    def clear_budget_form(self):
        self.selected_budget_id = None

        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.income_entry.delete(0, "end")

        for entry in self.expense_entries.values():
            entry.delete(0, "end")

    # =========================================================
    # SPENDING OVERVIEW
    # =========================================================

    def create_spending_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["spending"] = page

        self.make_header(
            page,
            "Spending Overview",
            "Your spending information"
        )

        self.make_nav(page, [
            ("Dashboard", lambda: self.show_page("dashboard")),
            ("Spending", lambda: self.show_page("spending")),
            ("Budget", lambda: self.show_page("budget")),
            ("Balance", lambda: self.show_page("balance")),
            ("Expense Graph", lambda: self.show_page("graph")),
        ])

        self.spending_body = ctk.CTkScrollableFrame(
            page, fg_color=self.green_pale
        )
        self.spending_body.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh_spending(self):
        for widget in self.spending_body.winfo_children():
            widget.destroy()

        rows = self.get_user_budgets()

        ctk.CTkLabel(
            self.spending_body,
            text=f"User: {self.current_username}",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=self.green_dark
        ).pack(anchor="w", padx=15, pady=10)

        if not rows:
            ctk.CTkLabel(
                self.spending_body,
                text="No spending data has been entered yet.",
                font=ctk.CTkFont(size=17),
                text_color="#607568"
            ).pack(pady=30)
            return

        total_income = sum(row[2] for row in rows)
        categories = self.category_totals(rows)
        total_expense = sum(categories.values())

        summary = ctk.CTkFrame(
            self.spending_body,
            fg_color=self.white,
            corner_radius=15
        )
        summary.pack(fill="x", padx=10, pady=10)

        self.summary_card(summary, "Total Income",
                          f"₹{total_income:,.2f}", 0)
        self.summary_card(summary, "Total Spending",
                          f"₹{total_expense:,.2f}", 1)
        self.summary_card(summary, "Remaining",
                          f"₹{total_income - total_expense:,.2f}", 2)

        ctk.CTkLabel(
            self.spending_body,
            text="Spending by Category",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=self.green_dark
        ).pack(anchor="w", padx=15, pady=(25, 10))

        for category, amount in categories.items():
            if amount <= 0:
                continue

            row_frame = ctk.CTkFrame(
                self.spending_body,
                fg_color=self.white,
                corner_radius=12
            )
            row_frame.pack(fill="x", padx=10, pady=6)

            ctk.CTkLabel(
                row_frame,
                text=category,
                width=160,
                anchor="w",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.text_dark
            ).pack(side="left", padx=15, pady=12)

            ctk.CTkProgressBar(
                row_frame,
                width=450,
                progress_color=self.green,
                fg_color=self.green_light
            ).pack(side="left", padx=15, pady=12)

            percent = (amount / total_expense * 100) if total_expense else 0

            ctk.CTkLabel(
                row_frame,
                text=f"₹{amount:,.2f}  ({percent:.1f}%)",
                text_color=self.green_dark
            ).pack(side="right", padx=15)

        ctk.CTkButton(
            self.spending_body,
            text="View User Details",
            command=self.show_user_details,
            fg_color=self.green,
            hover_color=self.green_dark
        ).pack(pady=25)

    def summary_card(self, parent, title, value, column):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.green_pale,
            corner_radius=12
        )
        card.grid(row=0, column=column, padx=15, pady=15,
                  sticky="nsew")
        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="#607568"
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(0, 15))

    def show_user_details(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT full_name, email, username FROM users WHERE id=?",
            (self.current_user_id,)
        )
        user = cur.fetchone()
        conn.close()

        if not user:
            return

        messagebox.showinfo(
            "User Details",
            f"Full Name: {user[0]}\n"
            f"Email: {user[1]}\n"
            f"Username: {user[2]}"
        )

    # =========================================================
    # BUDGET WEEKLY / MONTHLY
    # =========================================================

    def create_budget_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["budget"] = page

        self.make_header(
            page,
            "Budget View",
            "Weekly and monthly spending"
        )

        self.make_nav(page, [
            ("Dashboard", lambda: self.show_page("dashboard")),
            ("Spending", lambda: self.show_page("spending")),
            ("Budget", lambda: self.show_page("budget")),
            ("Balance", lambda: self.show_page("balance")),
            ("Expense Graph", lambda: self.show_page("graph")),
        ])

        self.budget_body = ctk.CTkScrollableFrame(
            page, fg_color=self.green_pale
        )
        self.budget_body.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh_budget(self):
        for widget in self.budget_body.winfo_children():
            widget.destroy()

        rows = self.get_user_budgets()

        ctk.CTkLabel(
            self.budget_body,
            text="Choose a Spending View",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=20)

        buttons = ctk.CTkFrame(
            self.budget_body,
            fg_color="transparent"
        )
        buttons.pack(pady=10)

        ctk.CTkButton(
            buttons,
            text="Weekly",
            width=180,
            height=45,
            fg_color=self.green,
            hover_color=self.green_dark,
            command=lambda: self.show_period_budget("weekly")
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons,
            text="Monthly",
            width=180,
            height=45,
            fg_color=self.green,
            hover_color=self.green_dark,
            command=lambda: self.show_period_budget("monthly")
        ).pack(side="left", padx=10)

        self.budget_result = ctk.CTkFrame(
            self.budget_body,
            fg_color=self.white,
            corner_radius=15
        )
        self.budget_result.pack(fill="x", padx=15, pady=30)

        if not rows:
            ctk.CTkLabel(
                self.budget_result,
                text="Enter budget information from the Dashboard first.",
                text_color="#607568",
                font=ctk.CTkFont(size=16)
            ).pack(pady=30)

    def show_period_budget(self, period):
        for widget in self.budget_result.winfo_children():
            widget.destroy()

        rows = self.get_user_budgets()

        if not rows:
            return

        # This is based on all entered data. The dates entered by the
        # user are used to determine the period.
        today = datetime.now().date()

        selected = []

        for row in rows:
            try:
                d = datetime.strptime(row[1], "%Y-%m-%d").date()
            except ValueError:
                continue

            if period == "weekly":
                days = (today - d).days
                if 0 <= days < 7:
                    selected.append(row)

            else:
                if d.year == today.year and d.month == today.month:
                    selected.append(row)

        income = sum(row[2] for row in selected)
        categories = self.category_totals(selected)
        expenses = sum(categories.values())
        remaining = income - expenses

        title = "This Week" if period == "weekly" else "This Month"

        ctk.CTkLabel(
            self.budget_result,
            text=title,
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            self.budget_result,
            text=f"Income: ₹{income:,.2f}",
            font=ctk.CTkFont(size=18),
            text_color=self.text_dark
        ).pack(pady=5)

        ctk.CTkLabel(
            self.budget_result,
            text=f"Expenses: ₹{expenses:,.2f}",
            font=ctk.CTkFont(size=18),
            text_color=self.text_dark
        ).pack(pady=5)

        ctk.CTkLabel(
            self.budget_result,
            text=f"Remaining: ₹{remaining:,.2f}",
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(5, 25))

    # =========================================================
    # BALANCE / SAVINGS
    # =========================================================

    def create_balance_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["balance"] = page

        self.make_header(
            page,
            "Remaining Balance",
            "Automatic savings calculation"
        )

        self.make_nav(page, [
            ("Dashboard", lambda: self.show_page("dashboard")),
            ("Spending", lambda: self.show_page("spending")),
            ("Budget", lambda: self.show_page("budget")),
            ("Balance", lambda: self.show_page("balance")),
            ("Expense Graph", lambda: self.show_page("graph")),
        ])

        self.balance_body = ctk.CTkFrame(
            page,
            fg_color=self.green_pale
        )
        self.balance_body.pack(fill="both", expand=True, padx=30, pady=30)

    def refresh_balance(self):
        for widget in self.balance_body.winfo_children():
            widget.destroy()

        rows = self.get_user_budgets()

        income = sum(row[2] for row in rows)
        categories = self.category_totals(rows)
        expenses = sum(categories.values())
        remaining = income - expenses

        box = ctk.CTkFrame(
            self.balance_body,
            fg_color=self.white,
            corner_radius=25,
            border_width=2,
            border_color=self.green
        )
        box.place(relx=0.5, rely=0.45, anchor="center",
                  relwidth=0.62, relheight=0.62)

        ctk.CTkLabel(
            box,
            text="Your Automatic Savings Result",
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(55, 25))

        ctk.CTkLabel(
            box,
            text=f"Total Income\n₹{income:,.2f}",
            font=ctk.CTkFont(size=20),
            text_color=self.text_dark
        ).pack(pady=10)

        ctk.CTkLabel(
            box,
            text=f"Total Expenses\n₹{expenses:,.2f}",
            font=ctk.CTkFont(size=20),
            text_color=self.text_dark
        ).pack(pady=10)

        result_text = (
            f"Remaining Balance / Savings\n₹{remaining:,.2f}"
        )

        ctk.CTkLabel(
            box,
            text=result_text,
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=20)

    # =========================================================
    # EXPENSE GRAPH
    # =========================================================

    def create_graph_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["graph"] = page

        self.make_header(
            page,
            "Expense Graph",
            "Automatically calculated from your budget entries"
        )

        self.make_nav(page, [
            ("Dashboard", lambda: self.show_page("dashboard")),
            ("Spending", lambda: self.show_page("spending")),
            ("Budget", lambda: self.show_page("budget")),
            ("Balance", lambda: self.show_page("balance")),
            ("Expense Graph", lambda: self.show_page("graph")),
        ])

        self.graph_body = ctk.CTkScrollableFrame(
            page, fg_color=self.green_pale
        )
        self.graph_body.pack(fill="both", expand=True, padx=20, pady=15)

    def refresh_graph(self):
        for widget in self.graph_body.winfo_children():
            widget.destroy()

        rows = self.get_user_budgets()
        categories = self.category_totals(rows)
        total_income = sum(row[2] for row in rows)
        total_expenses = sum(categories.values())

        ctk.CTkLabel(
            self.graph_body,
            text="Expense Distribution",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.graph_body,
            text="All values are taken automatically from the Dashboard.",
            font=ctk.CTkFont(size=15),
            text_color="#607568"
        ).pack(pady=(0, 20))

        summary = ctk.CTkFrame(
            self.graph_body,
            fg_color=self.white,
            corner_radius=15
        )
        summary.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            summary,
            text=f"Total Income: ₹{total_income:,.2f}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.green_dark
        ).pack(side="left", padx=25, pady=20)

        ctk.CTkLabel(
            summary,
            text=f"Total Expenses: ₹{total_expenses:,.2f}",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.green_dark
        ).pack(side="left", padx=25, pady=20)

        if total_expenses == 0:
            ctk.CTkLabel(
                self.graph_body,
                text="No expenses entered yet.",
                font=ctk.CTkFont(size=18),
                text_color="#607568"
            ).pack(pady=40)
            return

        # Green-shade graphical representation.
        # No extra input is required here.
        shades = [
            "#315C45", "#3E7355", "#4F8A68", "#619D79",
            "#74AF8A", "#87BF99", "#9ACCAA", "#B0D8BC"
        ]

        for index, (category, amount) in enumerate(categories.items()):
            if amount <= 0:
                continue

            percent = (amount / total_expenses) * 100

            row = ctk.CTkFrame(
                self.graph_body,
                fg_color=self.white,
                corner_radius=12
            )
            row.pack(fill="x", padx=10, pady=7)

            ctk.CTkLabel(
                row,
                text=category,
                width=145,
                anchor="w",
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=self.text_dark
            ).pack(side="left", padx=15, pady=12)

            bar_background = ctk.CTkFrame(
                row,
                fg_color=self.green_light,
                height=28,
                corner_radius=14
            )
            bar_background.pack(
                side="left", fill="x", expand=True, padx=10, pady=12
            )

            # Approximate visual width using a percentage label and
            # a progress bar so the graph stays entirely in CustomTkinter.
            progress = ctk.CTkProgressBar(
                bar_background,
                progress_color=shades[index % len(shades)],
                fg_color=self.green_light,
                height=20
            )
            progress.pack(fill="x", expand=True, padx=3, pady=3)
            progress.set(percent / 100)

            ctk.CTkLabel(
                row,
                text=f"₹{amount:,.2f}\n{percent:.1f}%",
                width=125,
                text_color=self.green_dark,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="right", padx=12)

        ctk.CTkLabel(
            self.graph_body,
            text="Expense values are shown as a percentage of total expenses.",
            font=ctk.CTkFont(size=14),
            text_color="#607568"
        ).pack(pady=20)

    # =========================================================
    # HELPERS
    # =========================================================

    def category_totals(self, rows):
        totals = {
            "Food": 0,
            "Transport": 0,
            "Shopping": 0,
            "Bills": 0,
            "Education": 0,
            "Health": 0,
            "Entertainment": 0,
            "Other": 0
        }

        indexes = {
            "Food": 3,
            "Transport": 4,
            "Shopping": 5,
            "Bills": 6,
            "Education": 7,
            "Health": 8,
            "Entertainment": 9,
            "Other": 10
        }

        for row in rows:
            for category, index in indexes.items():
                totals[category] += float(row[index] or 0)

        return totals

    # =========================================================
    # ADMIN LOGIN
    # =========================================================

    def create_admin_login_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["admin_login"] = page

        box = ctk.CTkFrame(
            page,
            fg_color=self.white,
            corner_radius=20,
            border_width=2,
            border_color=self.green
        )
        box.place(relx=0.5, rely=0.5, anchor="center",
                  relwidth=0.42, relheight=0.65)

        ctk.CTkLabel(
            box,
            text="Admin Login",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(60, 10))

        ctk.CTkLabel(
            box,
            text="Restricted administrator area",
            text_color="#607568"
        ).pack(pady=(0, 25))

        self.admin_username = ctk.CTkEntry(
            box, placeholder_text="Admin Username",
            width=300, height=45
        )
        self.admin_username.pack(pady=10)

        self.admin_password = ctk.CTkEntry(
            box, placeholder_text="Admin Password",
            show="*", width=300, height=45
        )
        self.admin_password.pack(pady=10)

        ctk.CTkButton(
            box,
            text="Admin Login",
            command=self.admin_login,
            width=300,
            height=45,
            fg_color=self.green,
            hover_color=self.green_dark
        ).pack(pady=25)

        ctk.CTkButton(
            box,
            text="Back",
            command=lambda: self.show_page("front"),
            fg_color="#E8F2EC",
            text_color=self.green_dark,
            hover_color=self.green_light
        ).pack()

        ctk.CTkLabel(
            box,
            text="Default: admin / admin123",
            text_color="#718277",
            font=ctk.CTkFont(size=12)
        ).pack(pady=15)

    def admin_login(self):
        username = self.admin_username.get().strip()
        password = self.admin_password.get()

        # Change these two values if you want your own admin credentials.
        if username == "admin" and password == "admin123":
            self.show_page("admin_dashboard")
        else:
            messagebox.showerror(
                "Access denied",
                "Only the administrator can access this page."
            )

    # =========================================================
    # ADMIN DASHBOARD
    # Same dashboard style as the user's dashboard
    # =========================================================

    def create_admin_dashboard_page(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["admin_dashboard"] = page

        self.make_header(
            page,
            "Budget Planner",
            "Admin Dashboard"
        )

        nav = ctk.CTkFrame(
            page, fg_color=self.green_pale, corner_radius=0
        )
        nav.pack(fill="x")

        ctk.CTkButton(
            nav,
            text="Dashboard",
            command=lambda: self.show_page("admin_dashboard"),
            fg_color=self.green,
            hover_color=self.green_dark,
            height=35
        ).pack(side="left", padx=5, pady=8)

        ctk.CTkButton(
            nav,
            text="User Information",
            command=lambda: self.show_page("admin_panel"),
            fg_color=self.green,
            hover_color=self.green_dark,
            height=35
        ).pack(side="left", padx=5, pady=8)

        ctk.CTkButton(
            nav,
            text="Logout",
            command=lambda: self.show_page("welcome"),
            fg_color=self.green_dark,
            hover_color=self.green,
            height=35
        ).pack(side="right", padx=10, pady=8)

        self.admin_dashboard_body = ctk.CTkScrollableFrame(
            page, fg_color=self.green_pale
        )
        self.admin_dashboard_body.pack(
            fill="both", expand=True, padx=20, pady=15
        )

    def refresh_admin_dashboard(self):
        for widget in self.admin_dashboard_body.winfo_children():
            widget.destroy()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM budgets")
        budget_count = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(income), 0) FROM budgets")
        total_income = cur.fetchone()[0]

        cur.execute("""
            SELECT COALESCE(
                SUM(food + transport + shopping + bills +
                    education + health + entertainment + other), 0
            )
            FROM budgets
        """)
        total_expenses = cur.fetchone()[0]
        conn.close()

        ctk.CTkLabel(
            self.admin_dashboard_body,
            text="Admin Overview",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.green_dark
        ).pack(anchor="w", padx=15, pady=10)

        # Same card style as the user's dashboard.
        cards = ctk.CTkFrame(
            self.admin_dashboard_body,
            fg_color="transparent"
        )
        cards.pack(fill="x", padx=10, pady=10)

        self.admin_summary_card(
            cards, "Registered Users", str(user_count), 0
        )
        self.admin_summary_card(
            cards, "Budget Entries", str(budget_count), 1
        )
        self.admin_summary_card(
            cards, "Total Income", f"₹{total_income:,.2f}", 2
        )
        self.admin_summary_card(
            cards, "Total Expenses", f"₹{total_expenses:,.2f}", 3
        )

        remaining = total_income - total_expenses

        result = ctk.CTkFrame(
            self.admin_dashboard_body,
            fg_color=self.white,
            corner_radius=15
        )
        result.pack(fill="x", padx=10, pady=20)

        ctk.CTkLabel(
            result,
            text="Total Remaining Balance / Savings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            result,
            text=f"₹{remaining:,.2f}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            self.admin_dashboard_body,
            text="View All User Information",
            command=lambda: self.show_page("admin_panel"),
            width=250,
            height=45,
            fg_color=self.green,
            hover_color=self.green_dark
        ).pack(pady=20)

    def admin_summary_card(self, parent, title, value, column):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.white,
            corner_radius=15
        )
        card.grid(
            row=0, column=column,
            padx=7, pady=7, sticky="nsew"
        )
        parent.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=13),
            text_color="#607568"
        ).pack(pady=(18, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.green_dark
        ).pack(pady=(0, 18))

    # =========================================================
    # ADMIN PANEL
    # =========================================================

    def create_admin_panel(self):
        page = ctk.CTkFrame(self, fg_color=self.green_pale)
        self.pages["admin_panel"] = page

        self.make_header(
            page,
            "Admin Panel",
            "User information and budget records"
        )

        admin_nav = ctk.CTkFrame(
            page, fg_color=self.green_pale, corner_radius=0
        )
        admin_nav.pack(fill="x")

        ctk.CTkButton(
            admin_nav,
            text="Admin Dashboard",
            command=lambda: self.show_page("admin_dashboard"),
            fg_color=self.green,
            hover_color=self.green_dark,
            height=35
        ).pack(side="left", padx=8, pady=8)

        ctk.CTkButton(
            admin_nav,
            text="User Information",
            command=lambda: self.show_page("admin_panel"),
            fg_color=self.green,
            hover_color=self.green_dark,
            height=35
        ).pack(side="left", padx=8, pady=8)

        ctk.CTkButton(
            admin_nav,
            text="Admin Logout",
            command=lambda: self.show_page("welcome"),
            width=130,
            fg_color=self.green_dark,
            hover_color=self.green,
            height=35
        ).pack(side="right", padx=10, pady=8)

        self.admin_body = ctk.CTkScrollableFrame(
            page, fg_color=self.green_pale
        )
        self.admin_body.pack(fill="both", expand=True, padx=20, pady=10)

    def refresh_admin_panel(self):
        for widget in self.admin_body.winfo_children():
            widget.destroy()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, username, full_name, email
            FROM users
            ORDER BY id
        """)
        users = cur.fetchall()

        ctk.CTkLabel(
            self.admin_body,
            text=f"Registered Users: {len(users)}",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=self.green_dark
        ).pack(anchor="w", padx=10, pady=10)

        if not users:
            ctk.CTkLabel(
                self.admin_body,
                text="No users have registered yet.",
                text_color="#607568"
            ).pack(pady=30)
            conn.close()
            return

        for user in users:
            user_id, username, full_name, email = user

            cur.execute("""
                SELECT entry_date, income, food, transport, shopping,
                       bills, education, health, entertainment, other
                FROM budgets
                WHERE user_id=?
                ORDER BY id DESC
            """, (user_id,))
            budgets = cur.fetchall()

            user_card = ctk.CTkFrame(
                self.admin_body,
                fg_color=self.white,
                corner_radius=15,
                border_width=1,
                border_color=self.green
            )
            user_card.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(
                user_card,
                text=f"Username: {username}",
                font=ctk.CTkFont(size=20, weight="bold"),
                text_color=self.green_dark
            ).pack(anchor="w", padx=20, pady=(15, 3))

            ctk.CTkLabel(
                user_card,
                text=f"Full Name: {full_name}\nEmail: {email}",
                justify="left",
                text_color=self.text_dark
            ).pack(anchor="w", padx=20, pady=5)

            if budgets:
                for budget in budgets:
                    (
                        date, income, food, transport, shopping,
                        bills, education, health, entertainment, other
                    ) = budget

                    expense = (
                        food + transport + shopping + bills +
                        education + health + entertainment + other
                    )

                    ctk.CTkLabel(
                        user_card,
                        text=(
                            f"Date: {date}   |   "
                            f"Income: ₹{income:,.2f}   |   "
                            f"Expenses: ₹{expense:,.2f}   |   "
                            f"Balance: ₹{income - expense:,.2f}"
                        ),
                        text_color=self.green_dark
                    ).pack(anchor="w", padx=20, pady=5)
            else:
                ctk.CTkLabel(
                    user_card,
                    text="No budget information entered yet.",
                    text_color="#607568"
                ).pack(anchor="w", padx=20, pady=5)

        conn.close()

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self):
        self.current_user_id = None
        self.current_username = None
        self.selected_budget_id = None

        try:
            self.login_username.delete(0, "end")
            self.login_password.delete(0, "end")
        except Exception:
            pass

        self.show_page("front")


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
    create_database()
    app = BudgetApp()
    app.mainloop()
