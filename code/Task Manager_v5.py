import tkinter as tk
from tkinter import messagebox, Toplevel, Label, ttk
from tkcalendar import Calendar
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

# 主應用程式類別
class TaskManagerApp:
    def __init__(self, root):
        """
        初始化應用程式，設置主視窗屬性及介面元件。
        - root: 主視窗物件
        """
        self.root = root
        self.root.title("Task and Time Management System")  # 設定視窗標題
        self.root.geometry("600x400")  # 設定主視窗大小
        self.root.resizable(False, False)  # 禁止視窗縮放
        self.tasks = []  # 儲存任務的列表

        # 鍵盤視窗與目標輸入框
        self.keyboard_window = None
        self.target_entry = None
        self.is_keyboard_open = False  # 鍵盤是否打開
        self.ignore_focus_event = False  # 是否忽略焦點事件

        # 設定按鈕與標籤的樣式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TLabel", font=("Arial", 10))

        # 建立 UI 元件
        self.create_widgets()

    def create_widgets(self):
        """
        建立主視窗中的 UI 元件，包括標題、任務清單及功能按鈕。
        """
        # 標題
        title_label = tk.Label(self.root, text="Task List", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # 任務清單框
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

        self.refresh_task_list()  # 初始化任務清單

    def refresh_task_list(self):
        """
        更新任務清單的顯示內容。
        """
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task['name']} - Due: {task['deadline']} (Category: {task['category']}, Status: {task['status']})")

    def add_task(self):
        """
        開啟新增任務的窗口。
        """
        self.open_task_window("Add Task")

    def edit_task(self):
        """
        編輯已選定的任務。
        若未選定任務，顯示警告訊息。
        """
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to edit.")
            return
        selected_task = self.tasks[selected_index[0]]
        self.open_task_window("Edit Task", selected_task)

    def delete_task(self):
        """
        刪除已選定的任務。
        若未選定任務，顯示警告訊息。
        """
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return
        del self.tasks[selected_index[0]]
        self.refresh_task_list()
        messagebox.showinfo("Task Deleted", "Task has been deleted successfully.")

    def display_gantt_chart(self):
        """
        顯示所有任務的甘特圖。
        若無任務，顯示提示訊息。
        """
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
                start_date = datetime.strptime(task['deadline'], "%Y-%m-%d")
                task_names.append(task['name'])
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
        """
        顯示任務的日曆視圖。
        若無任務，顯示提示訊息。
        """
        if not self.tasks:
            messagebox.showinfo("No Tasks", "No tasks available to display in Calendar View.")
            return

        # 創建日曆窗口
        calendar_window = Toplevel(self.root)
        calendar_window.title("Calendar View")
        calendar_window.geometry("380x300")

        # 創建日曆小部件
        cal = Calendar(calendar_window, selectmode="day", year=2024, month=1, day=1)
        cal.pack(pady=20)

        # 標記任務日期
        for task in self.tasks:
            try:
                deadline = datetime.strptime(task['deadline'], "%Y-%m-%d").date()
                cal.calevent_create(deadline, task['name'], "task")
            except ValueError:
                continue

        Label(calendar_window, text="Tasks are marked on the calendar").pack(pady=10)
        cal.tag_config("task", background="lightblue", foreground="black")

    def open_task_window(self, title, task=None):
        """
        開啟新增或編輯任務的窗口。
        - title: 窗口標題 (字串)
        - task: 若為編輯模式，傳入要編輯的任務字典；新增模式則為 None。
        """
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
                task['name'] = name
                task['deadline'] = deadline
                task['category'] = category
            else:
                self.tasks.append({'name': name, 'deadline': deadline, 'category': category, 'status': 'Pending'})

            task_window.destroy()
            self.refresh_task_list()

        task_window = Toplevel(self.root)
        task_window.title(title)
        task_window.geometry("400x200")
        task_window.resizable(False, False)

        frame = tk.Frame(task_window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        labels = ["Task Name:", "Deadline (YYYY-MM-DD):", "Category:"]
        entries = []
        for i, label_text in enumerate(labels):
            tk.Label(frame, text=label_text).grid(row=i, column=0, padx=5, pady=10, sticky="w")
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=10)
            self.attach_to_entry(entry)
            entries.append(entry)

        name_entry, deadline_entry, category_entry = entries
        if task:
            name_entry.insert(0, task['name'])
            deadline_entry.insert(0, task['deadline'])
            category_entry.insert(0, task['category'])

        ttk.Button(frame, text="Save", command=save_task).grid(row=3, column=0, columnspan=2, pady=10)

    def open_login_system(self):
        """
        開啟登入系統。
        """
        login_window = tk.Toplevel(self.root)
        login_window.title("Login System")
        login_window.geometry("350x120")

        self.correct_username = "user"  # 正確的使用者名稱
        self.correct_password = "1234"  # 正確的密碼

        tk.Label(login_window, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = tk.Entry(login_window, width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.attach_to_entry(self.username_entry)

        tk.Label(login_window, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(login_window, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        self.attach_to_entry(self.password_entry)

        tk.Button(login_window, text="Login", command=self.verify_login).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(login_window, text="Cancel", command=login_window.destroy).grid(row=3, column=1, padx=10, pady=10)
    
    def verify_login(self):
        messagebox.showinfo("Login", "Login feature not implemented.")

    def attach_to_entry(self, entry):
        """
        將虛擬鍵盤附加到指定輸入框。
        """
        entry.bind("<FocusIn>", lambda e: self.set_cursor_active(entry))

    def set_cursor_active(self, entry):
        if self.ignore_focus_event:  # 若處於忽略狀態，直接跳過
            return
        if not self.is_keyboard_open:  # 只有鍵盤未打開時執行
            self.target_entry = entry
            self.open_virtual_keyboard(entry)

    def open_virtual_keyboard(self, entry):
        if self.is_keyboard_open:
            return

        self.is_keyboard_open = True
        self.target_entry = entry
        self.keyboard_window = Toplevel(self.root)
        self.keyboard_window.title("Virtual Keyboard")
        self.keyboard_window.geometry("830x270")

        # 綁定關閉事件
        self.keyboard_window.protocol("WM_DELETE_WINDOW", self.close_virtual_keyboard)

        # 定義鍵盤按鍵列表（移除 Backspace、Enter 和 Shift）
        keys = [
            ['Esc', '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\', 'Del'],
            ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''],
            ['Shift','z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '↑'],
            ['Fn', 'Ctrl', 'Win', 'Alt', 'Space', 'Alt2', 'Fn2', 'Ctrl2', '←', '↓', '→','-']
        ]

        # 用 grid 排列其餘按鍵
        for row_idx, row_keys in enumerate(keys):
            for col_idx, key in enumerate(row_keys):
                # 跳過需要用 place 單獨處理的按鍵
                if key in ['Space']:
                    continue

                # 確保 Space 後的按鍵適當偏移
                if key in ['Alt2', 'Fn2', 'Ctrl2', '←', '↓', '→','-']:
                    col_idx += 2  # 偏移 2 格

                # 判斷是否需要移除後綴 '2'
                if len(key) > 1 and key.endswith("2"):
                    display_key = key[:-1]
                else:
                    display_key = key

                tk.Button(
                    self.keyboard_window, text=display_key,
                    width=5, height=2,
                    command=lambda k=display_key: self.insert_text(k)
                ).grid(row=row_idx, column=col_idx, padx=5, pady=5)

        # 使用 place 單獨處理特定按鍵
        special_keys = {
            'Space': {'x': 225, 'y': 210, 'width': 20, 'height': 2, 'text': 'Space'},
            'Backspace': {'x': 670, 'y': 5, 'width': 20, 'height': 2, 'text': 'Backspace'},
            'Enter': {'x': 670, 'y': 105, 'width': 20, 'height': 2, 'text': 'Enter'},
            'Shift2': {'x': 670, 'y': 158, 'width': 20, 'height': 2, 'text': 'Shift'}
        }

        for key, params in special_keys.items():
            tk.Button(
                self.keyboard_window, text=params['text'],
                width=params['width'], height=params['height'],
                command=lambda k=params['text']: self.insert_text(k)
            ).place(x=params['x'], y=params['y'])

    def insert_text(self, key):
        """
        根據按鍵執行對目標輸入框的操作。
        """
        if not self.target_entry:  # 如果沒有目標輸入框，直接返回
            return

        current_text = self.target_entry.get()  # 獲取當前輸入框內容
        cursor_index = self.target_entry.index(tk.INSERT)  # 獲取游標位置

        # 特殊按鍵處理
        if key == 'Backspace':
            # 刪除游標左邊一格
            if cursor_index > 0:
                self.target_entry.delete(cursor_index - 1, cursor_index)

        elif key == 'Del':
            # 刪除游標右邊一格
            if cursor_index < len(current_text):
                self.target_entry.delete(cursor_index, cursor_index + 1)

        elif key == 'Space':
            # 插入一個空格
            self.target_entry.insert(cursor_index, ' ')

        elif key in ['Enter', 'Esc']:
            # 關閉虛擬鍵盤
            self.close_virtual_keyboard()

        elif key == 'Caps':
            # 切換英文大小寫
            if hasattr(self, 'is_caps_lock') and self.is_caps_lock:
                self.is_caps_lock = False
            else:
                self.is_caps_lock = True

        elif key == 'Tab':
            # 切換到下一個輸入框
            next_widget = self.target_entry.tk_focusNext()
            if next_widget and next_widget.widgetName == 'entry':  # 確保下一個是輸入框
                next_widget.focus_set()
                self.target_entry = next_widget  # 更新目標輸入框

        elif key == '←':
            # 游標往左移動一格
            if cursor_index > 0:
                self.target_entry.icursor(cursor_index - 1)

        elif key == '→':
            # 游標往右移動一格
            if cursor_index < len(current_text):
                self.target_entry.icursor(cursor_index + 1)

        else:
            # 普通按鍵輸入（處理大小寫）
            if hasattr(self, 'is_caps_lock') and self.is_caps_lock and key.isalpha():
                key = key.upper() if key.islower() else key.lower()
            self.target_entry.insert(cursor_index, key)


    def close_virtual_keyboard(self):
        if self.keyboard_window:
            self.keyboard_window.destroy()
            self.keyboard_window = None

        self.is_keyboard_open = False
        self.target_entry = None
        self.ignore_focus_event = True  # 啟用忽略狀態

        # 在短時間後重置忽略狀態
        self.root.after(200, self.reset_focus_event)
    def reset_focus_event(self):
        """
        重置忽略 FocusIn 事件的狀態。
        """
        self.ignore_focus_event = False

# 主程式入口
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
