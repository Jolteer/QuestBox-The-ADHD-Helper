import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, date

class CalendarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Application")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Get current date
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.today_date = today.day
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        self.update_calendar()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header frame for navigation
        header_frame = tk.Frame(main_frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Navigation buttons and dropdowns
        self.prev_button = tk.Button(header_frame, text="◀", font=('Arial', 14, 'bold'),
                                   command=self.prev_month, bg='#4CAF50', fg='white',
                                   padx=15, pady=5)
        self.prev_button.pack(side='left')
        
        # Month and year selection
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        month_combo = ttk.Combobox(header_frame, textvariable=self.month_var,
                                 values=[calendar.month_name[i] for i in range(1, 13)],
                                 state="readonly", width=12, font=('Arial', 12))
        month_combo.pack(side='left', padx=10)
        month_combo.bind('<<ComboboxSelected>>', self.on_date_change)
        
        year_combo = ttk.Combobox(header_frame, textvariable=self.year_var,
                                values=[str(year) for year in range(1900, 2101)],
                                state="readonly", width=8, font=('Arial', 12))
        year_combo.pack(side='left', padx=10)
        year_combo.bind('<<ComboboxSelected>>', self.on_date_change)
        
        self.next_button = tk.Button(header_frame, text="▶", font=('Arial', 14, 'bold'),
                                   command=self.next_month, bg='#4CAF50', fg='white',
                                   padx=15, pady=5)
        self.next_button.pack(side='left', padx=10)
        
        # Today button
        today_button = tk.Button(header_frame, text="Today", font=('Arial', 10),
                               command=self.go_to_today, bg='#2196F3', fg='white',
                               padx=10, pady=5)
        today_button.pack(side='right')
        
        # Calendar frame
        self.calendar_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=2)
        self.calendar_frame.pack(fill='both', expand=True)
        
        # Day headers
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for i, day in enumerate(days):
            day_label = tk.Label(self.calendar_frame, text=day, font=('Arial', 12, 'bold'),
                               bg='#E3F2FD', fg='#1976D2', relief='ridge', bd=1)
            day_label.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        
        # Configure grid weights
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(7):  # 6 weeks + header
            self.calendar_frame.rowconfigure(i, weight=1)
        
        # Initialize day buttons list
        self.day_buttons = []
        for week in range(6):
            week_buttons = []
            for day in range(7):
                btn = tk.Button(self.calendar_frame, text="", font=('Arial', 12),
                              relief='flat', bg='white', fg='black',
                              command=lambda w=week, d=day: self.on_day_click(w, d))
                btn.grid(row=week+1, column=day, sticky='nsew', padx=1, pady=1)
                week_buttons.append(btn)
            self.day_buttons.append(week_buttons)
    
    def update_calendar(self):
        # Update month and year comboboxes
        self.month_var.set(calendar.month_name[self.current_month])
        self.year_var.set(str(self.current_year))
        
        # Get calendar data
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Clear all buttons first
        for week_buttons in self.day_buttons:
            for btn in week_buttons:
                btn.config(text="", bg='white', fg='black', state='disabled')
        
        # Fill in the calendar
        today = date.today()
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                btn = self.day_buttons[week_num][day_num]
                if day == 0:
                    btn.config(text="", state='disabled', bg='#f5f5f5')
                else:
                    btn.config(text=str(day), state='normal')
                    
                    # Highlight today
                    if (self.current_year == today.year and 
                        self.current_month == today.month and 
                        day == today.day):
                        btn.config(bg='#FF5722', fg='white', font=('Arial', 12, 'bold'))
                    else:
                        btn.config(bg='white', fg='black', font=('Arial', 12))
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()
    
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()
    
    def on_date_change(self, event=None):
        try:
            month_name = self.month_var.get()
            self.current_month = list(calendar.month_name).index(month_name)
            self.current_year = int(self.year_var.get())
            self.update_calendar()
        except (ValueError, IndexError):
            pass
    
    def go_to_today(self):
        today = datetime.now()
        self.current_year = today.year
        self.current_month = today.month
        self.update_calendar()
    
    def on_day_click(self, week, day):
        btn = self.day_buttons[week][day]
        if btn.cget('text'):
            selected_day = btn.cget('text')
            date_str = f"{calendar.month_name[self.current_month]} {selected_day}, {self.current_year}"
            
            # Create a popup window to show selected date
            popup = tk.Toplevel(self.root)
            popup.title("Selected Date")
            popup.geometry("300x150")
            popup.configure(bg='#f0f0f0')
            popup.resizable(False, False)
            
            # Center the popup
            popup.transient(self.root)
            popup.grab_set()
            
            tk.Label(popup, text="Selected Date:", font=('Arial', 12, 'bold'), 
                    bg='#f0f0f0').pack(pady=20)
            tk.Label(popup, text=date_str, font=('Arial', 14), 
                    bg='#f0f0f0', fg='#1976D2').pack(pady=10)
            tk.Button(popup, text="OK", command=popup.destroy,
                     bg='#4CAF50', fg='white', padx=20, pady=5).pack(pady=20)

def main():
    root = tk.Tk()
    app = CalendarGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()