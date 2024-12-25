import tkinter as tk
from tkinter import messagebox, Toplevel, Label, ttk
from tkcalendar import Calendar
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

# 定義任務類別
class Task:
    def __init__(self, name, deadline, category="General", status="Pending"):
        self.name = name
        self.deadline = deadline
        self.category = category
        self.status = status

    def __str__(self):
        return f"{self.name} - Due: {self.deadline} (Category: {self.category}, Status: {self.status})"

# 主應用程式類別
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task and Time Management System")
        self.root.geometry("600x400")  # 設定主視窗大小
        self.root.resizable(False, False)  # 禁止縮放
        self.tasks = []

        # 樣式美化
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TLabel", font=("Arial", 10))

        # 建立 UI 元件
        self.create_widgets()

    def create_widgets(self):
        # 標題
        title_label = tk.Label(self.root, text="Task List", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 任務清單
        self.task_listbox = tk.Listbox(self.root, height=15, width=50, font=("Arial", 10))
        self.task_listbox.grid(row=1, column=0, rowspan=6, padx=10, pady=10)

        # 功能按鈕
        button_texts = [
            ("Add Task", self.add_task),
            ("Edit Task", self.edit_task),
            ("Delete Task", self.delete_task),
            ("Display Gantt Chart", self.display_gantt_chart),
            ("Display Calendar View", self.display_calendar_view),
            ("Open Login System", self.open_login_system),
            ("Exit", self.root.quit),
        ]
        for i, (text, command) in enumerate(button_texts):
            ttk.Button(self.root, text=text, command=command).grid(row=i + 1, column=1, padx=10, pady=5)

        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, str(task))

    def add_task(self):
        self.open_task_window("Add Task")

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to edit.")
            return
        selected_task = self.tasks[selected_index[0]]
        self.open_task_window("Edit Task", selected_task)

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return
        del self.tasks[selected_index[0]]
        self.refresh_task_list()
        messagebox.showinfo("Task Deleted", "Task has been deleted successfully.")

    def display_gantt_chart(self):
        if not self.tasks:
            messagebox.showinfo("No Tasks", "No tasks available to display in Gantt Chart.")
            return

        # 創建甘特圖窗口
        gantt_window = Toplevel(self.root)
        gantt_window.title("Gantt Chart")
        gantt_window.geometry("800x600")

        # 準備甘特圖數據
        task_names = []
        start_dates = []
        durations = []

        for task in self.tasks:
            try:
                start_date = datetime.strptime(task.deadline, "%Y-%m-%d")
                task_names.append(task.name)
                start_dates.append(date2num(start_date))
                durations.append(1)  # 預設每個任務持續一天
            except ValueError:
                continue

        # 設定字體
        font_path = 'C:/Windows/Fonts/msyh.ttc'  # 微軟雅黑字體
        prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = prop.get_name()

        # 繪製甘特圖
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.barh(task_names, durations, left=start_dates, color="skyblue", edgecolor="black")
        ax.set_xlabel("Dates", fontproperties=prop)
        ax.set_ylabel("Tasks", fontproperties=prop)
        ax.set_title("Gantt Chart", fontproperties=prop)
        ax.xaxis_date()  # 設置 x 軸為日期格式
        plt.tight_layout()

        # 將圖嵌入到 Tkinter 視窗中
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_calendar_view(self):
        if not self.tasks:
            messagebox.showinfo("No Tasks", "No tasks available to display in Calendar View.")
            return

        # 創建日曆窗口
        calendar_window = Toplevel(self.root)
        calendar_window.title("Calendar View")
        calendar_window.geometry("400x400")

        # 創建日曆小部件
        cal = Calendar(calendar_window, selectmode="day", year=2024, month=1, day=1)
        cal.pack(pady=20)

        # 標記任務日期
        for task in self.tasks:
            try:
                deadline = datetime.strptime(task.deadline, "%Y-%m-%d").date()
                cal.calevent_create(deadline, task.name, "task")
            except ValueError:
                continue

        Label(calendar_window, text="Tasks are marked on the calendar").pack(pady=10)
        cal.tag_config("task", background="lightblue", foreground="black")

    def open_task_window(self, title, task=None):
        def save_task():
            name = name_entry.get().strip()
            deadline = deadline_entry.get().strip()
            category = category_entry.get().strip() or "General"

            if not name or not deadline:
                messagebox.showerror("Input Error", "Name and Deadline are required.")
                return

            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Date Error", "Deadline must be in YYYY-MM-DD format.")
                return

            if task:
                task.name = name
                task.deadline = deadline
                task.category = category
            else:
                self.tasks.append(Task(name, deadline, category))

            task_window.destroy()
            self.refresh_task_list()

        task_window = Toplevel(self.root)
        task_window.title(title)
        task_window.geometry("350x200")
        task_window.resizable(False, False)

        frame = tk.Frame(task_window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        labels = ["Task Name:", "Deadline (YYYY-MM-DD):", "Category:"]
        entries = []
        for i, label_text in enumerate(labels):
            tk.Label(frame, text=label_text).grid(row=i, column=0, padx=5, pady=10, sticky="w")
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=10)
            entries.append(entry)

        name_entry, deadline_entry, category_entry = entries
        if task:
            name_entry.insert(0, task.name)
            deadline_entry.insert(0, task.deadline)
            category_entry.insert(0, task.category)

        ttk.Button(frame, text="Save", command=save_task).grid(row=3, column=0, columnspan=2, pady=10)

    def open_login_system(self):
        LoginSystem(self.root)

class LoginSystem:
    def __init__(self, root):
        self.root = root
        login_window = tk.Toplevel(self.root)
        login_window.title("Login System with Virtual Keyboard")
        login_window.geometry("400x300")

        self.correct_username = "user"
        self.correct_password = "1234"

        tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(login_window, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(login_window, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(login_window, text="Login", command=self.login).grid(row=2, column=1, pady=10)
        tk.Button(login_window, text="Open Virtual Keyboard", command=self.open_virtual_keyboard).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == self.correct_username and password == self.correct_password:
            messagebox.showinfo("Login Successful", "Welcome!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_virtual_keyboard(self):
        keyboard_window = Toplevel(self.root)
        keyboard_window.title("Virtual Keyboard")
        keyboard_window.geometry("600x200")

        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', 'Back'
        ]

        for i, key in enumerate(keys):
            action = lambda x=key: self.insert_text(x)
            tk.Button(keyboard_window, text=key, width=5, command=action).grid(row=i//10, column=i%10)

    def insert_text(self, key):
        if key == "Space":
            self.password_entry.insert(tk.END, " ")
        elif key == "Back":
            current_text = self.password_entry.get()
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, current_text[:-1])
        else:
            self.password_entry.insert(tk.END, key)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()