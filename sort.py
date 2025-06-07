import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
import csv
import pyperclip

# Global variables
root = tk.Tk()
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)
canvas = None
algo_choice = None
entry_array = None
complexity_var = None
result_var = None
sorted_var = None
last_sorted = []
speed_scale = None
speed_scale = None

# Algorithm complexity information
ALGO_COMPLEXITY = {
    "Bubble Sort": {"time": "O(n²)", "space": "O(1)"},
    "Selection Sort": {"time": "O(n²)", "space": "O(1)"},
    "Insertion Sort": {"time": "O(n²)", "space": "O(1)"},
    "Merge Sort": {"time": "O(n log n)", "space": "O(n)"},
    "Quick Sort": {"time": "O(n log n)", "space": "O(log n)"},
    "Heap Sort": {"time": "O(n log n)", "space": "O(1)"}
}

PROFESSIONAL_FONTS = {
    'header': ('Segoe UI', 16, 'bold'),
    'subheader': ('Segoe UI', 14),
    'body': ('Segoe UI', 11),
    'button': ('Segoe UI', 10),
    'code': ('Cascadia Code', 11)  # Modern monospace font
}

COLORS = {
    'primary': '#1976D2',      # More muted blue for main actions
    'success': '#2E7D32',      # Darker green for better contrast
    'danger': '#C62828',       # Deeper red
    'accent': '#512DA8',       # Rich purple
    'border': '#E0E0E0'        # Light gray for borders
}

THEME = {
    'bg': '#F5F5F5',           # Light gray background
    'canvas': '#FFFFFF',       # White canvas
    'text': '#212121',         # Dark text
    'bar': '#2196F3',         # Bright blue bars
    'secondary_bg': '#EEEEEE', # Slightly darker gray
    'border': '#E0E0E0',
    'hover': '#E3F2FD'        # Light blue hover effect
}

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=THEME['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # Create the scrollable frame
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Add the frame to the canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas to expand horizontally
        self.canvas.bind('<Configure>', self.adjust_frame_width)
        
        # Configure scrolling
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the widgets
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        self.bind_mouse_wheel()
        
    def adjust_frame_width(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
        
    def bind_mouse_wheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def unbind_mouse_wheel(self):
        self.canvas.unbind_all("<MouseWheel>")

def create_main_layout():
    global canvas, algo_choice, entry_array, complexity_var, result_var, sorted_var, speed_scale

    # Create scrollable main container
    scroll_container = ScrollableFrame(frame)
    scroll_container.pack(fill='both', expand=True)
    
    # Create main container with padding
    main_container = ttk.Frame(scroll_container.scrollable_frame)
    main_container.pack(fill='both', expand=True, padx=30, pady=20)

    # Header section with gradient effect
    header_frame = tk.Frame(main_container, bg=THEME['bg'], pady=20)
    header_frame.pack(fill='x')

    title = tk.Label(
        header_frame,
        text="Algorithm Visualizer Pro",
        font=('Segoe UI', 28, 'bold'),
        bg=THEME['bg'],
        fg=THEME['text']
    )
    title.pack()

    subtitle = tk.Label(
        header_frame,
        text="Visualize and analyze sorting algorithms in real-time",
        font=PROFESSIONAL_FONTS['subheader'],
        bg=THEME['bg'],
        fg=THEME['text']
    )
    subtitle.pack(pady=(5, 0))

    # Create control panel frame
    control_panel = ttk.LabelFrame(main_container, text="Controls", padding=10)
    control_panel.pack(fill='x', pady=(0, 20))

    # Create three columns in control panel
    input_frame = ttk.Frame(control_panel)
    input_frame.pack(fill='x', pady=5)
    
    # First row: Array input and Algorithm selection
    ttk.Label(input_frame, text="Input Array:", font=PROFESSIONAL_FONTS['body']).grid(row=0, column=0, padx=5, sticky='w')
    entry_array = ttk.Entry(input_frame, font=PROFESSIONAL_FONTS['body'], width=40)
    entry_array.grid(row=0, column=1, padx=5, sticky='ew')
    
    ttk.Label(input_frame, text="Algorithm:", font=PROFESSIONAL_FONTS['body']).grid(row=0, column=2, padx=5, sticky='w')
    algo_choice = ttk.Combobox(input_frame, values=list(ALGO_COMPLEXITY.keys()), font=PROFESSIONAL_FONTS['body'], state="readonly", width=20)
    algo_choice.grid(row=0, column=3, padx=5, sticky='ew')
    
    # Second row: Speed control and buttons
    speed_frame = ttk.Frame(control_panel)
    speed_frame.pack(fill='x', pady=10)
    
    ttk.Label(speed_frame, text="Animation Speed:", font=PROFESSIONAL_FONTS['body']).pack(side='left', padx=5)
    speed_scale = ttk.Scale(speed_frame, from_=0.1, to=2.0, orient='horizontal', length=200)
    speed_scale.set(1.0)  # Default speed
    speed_scale.pack(side='left', padx=5)
    
    # Buttons frame
    button_frame = ttk.Frame(control_panel)
    button_frame.pack(fill='x', pady=5)
    
    buttons = [
        ("Visualize", "▶", perform_sort, COLORS['primary']),
        ("Reset", "⟲", reset_input, COLORS['danger']),
        ("Export CSV", "⤓", export_to_csv, COLORS['success']),
        ("Copy", "⎘", copy_to_clipboard, COLORS['accent']),
        ("Generate Random", "⚄", generate_random_array, COLORS['primary'])
    ]

    for i, (text, icon, command, color) in enumerate(buttons):
        btn = create_modern_button(button_frame, f"{icon} {text}", command, color)
        btn.pack(side='left', padx=5)

    # Canvas frame with better styling
    canvas_frame = ttk.LabelFrame(main_container, text="Visualization", padding=10)
    canvas_frame.pack(fill='both', expand=True, pady=10)
    
    canvas = tk.Canvas(
        canvas_frame,
        width=900,
        height=300,
        bg=THEME['canvas'],
        bd=0,
        highlightthickness=0
    )
    canvas.pack(pady=10, padx=10, fill='both', expand=True)

    # Information panel
    info_frame = ttk.LabelFrame(main_container, text="Statistics", padding=10)
    info_frame.pack(fill='x', pady=10)
    
    # Add complexity and result variables
    complexity_var = tk.StringVar()
    result_var = tk.StringVar()
    sorted_var = tk.StringVar()
    
    ttk.Label(info_frame, textvariable=complexity_var, font=PROFESSIONAL_FONTS['code']).pack(side='left', padx=10)
    ttk.Label(info_frame, textvariable=result_var, font=PROFESSIONAL_FONTS['code']).pack(side='right', padx=10)

    # Sorted array display
    sorted_frame = ttk.LabelFrame(main_container, text="Sorted Array", padding=10)
    sorted_frame.pack(fill='x', pady=10)
    
    sorted_display = ttk.Label(
        sorted_frame,
        textvariable=sorted_var,
        font=PROFESSIONAL_FONTS['code'],
        wraplength=800
    )
    sorted_display.pack(fill='x', padx=10, pady=5)

def apply_theme():
    root.configure(bg=THEME['bg'])
    frame.configure(bg=THEME['bg'])

    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.configure(
                bg=THEME['bg'],
                highlightbackground=THEME['border'],
                highlightthickness=1
            )

    style = ttk.Style()

    # Check if theme already exists
    try:
        style.theme_create('professional', parent='alt', settings={
            "TCombobox": {
                "configure": {
                    "selectbackground": THEME['secondary_bg'],
                    "fieldbackground": THEME['canvas'],
                    "background": THEME['bg'],
                    "foreground": THEME['text'],
                    "arrowcolor": THEME['text'],
                    "padding": 5
                }
            }
        })
    except tk.TclError:
        # Theme already exists, just configure it
        style.configure('TCombobox',
                       selectbackground=THEME['secondary_bg'],
                       fieldbackground=THEME['canvas'],
                       background=THEME['bg'],
                       foreground=THEME['text'],
                       arrowcolor=THEME['text'])

    style.theme_use('professional')

def setup_main_window():
    root.title("Algorithm Visualizer Pro")
    root.geometry("1024x768")
    root.configure(bg=THEME['bg'])
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Center window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1024) // 2
    y = (screen_height - 768) // 2
    root.geometry(f"1024x768+{x}+{y}")
    
    # Add window icon
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
        
    # Configure grid weight
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

# Sorting algorithms implementation
def bubble_sort(arr):
    n = len(arr)
    steps = []
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append(arr.copy())
    return steps

def selection_sort(arr):
    n = len(arr)
    steps = []
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr.copy())
    return steps

def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
        steps.append(arr.copy())
    return steps

def merge_sort(arr):
    steps = []

    def merge(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            steps.append(arr.copy())

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            steps.append(arr.copy())

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            steps.append(arr.copy())

    def merge_sort_helper(arr, l, r):
        if l < r:
            m = (l + r) // 2
            merge_sort_helper(arr, l, m)
            merge_sort_helper(arr, m+1, r)
            merge(arr, l, m, r)

    merge_sort_helper(arr, 0, len(arr)-1)
    return steps

def quick_sort(arr):
    steps = []

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(arr.copy())
        arr[i+1], arr[high] = arr[high], arr[i+1]
        steps.append(arr.copy())
        return i+1

    def quick_sort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort_helper(arr, low, pi-1)
            quick_sort_helper(arr, pi+1, high)

    quick_sort_helper(arr, 0, len(arr)-1)
    return steps

def heap_sort(arr):
    steps = []

    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[largest] < arr[l]:
            largest = l

        if r < n and arr[largest] < arr[r]:
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            steps.append(arr.copy())
            heapify(arr, n, largest)

    n = len(arr)

    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        steps.append(arr.copy())
        heapify(arr, i, 0)

    return steps

# Function to update complexity information
def update_complexity(event=None):
    selected_algo = algo_choice.get()
    if selected_algo in ALGO_COMPLEXITY:
        complexity_info = ALGO_COMPLEXITY[selected_algo]
        complexity_var.set(f"Time: {complexity_info['time']} | Space: {complexity_info['space']}")

# Function to perform sorting and visualization
def perform_sort():
    global last_sorted
    try:
        # Get input array
        input_text = entry_array.get().strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter an array of numbers")
            return

        # Parse input
        try:
            # Try to evaluate as a Python expression (for lists like [1, 2, 3])
            arr = eval(input_text)
            if not isinstance(arr, list):
                arr = [int(x) for x in input_text.split(',')]
        except:
            # Fall back to comma-separated values
            arr = [int(x.strip()) for x in input_text.split(',')]

        # Validate array
        if not arr or not all(isinstance(x, (int, float)) for x in arr):
            messagebox.showerror("Error", "Invalid input. Please enter numbers separated by commas.")
            return

        # Get selected algorithm
        selected_algo = algo_choice.get()
        if not selected_algo:
            messagebox.showerror("Error", "Please select an algorithm")
            return

        # Perform sorting
        sorting_functions = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort
        }

        # Make a copy of the array to avoid modifying the original
        arr_copy = arr.copy()

        # Measure time
        start_time = time.time()
        steps = sorting_functions[selected_algo](arr_copy)
        end_time = time.time()

        # Store the sorted array
        last_sorted = arr_copy

        # Update result
        elapsed = end_time - start_time
        result_var.set(f"Time: {elapsed:.6f} seconds | Steps: {len(steps)}")

        # Visualize
        visualize_sorting(steps)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to visualize sorting steps
def visualize_sorting(steps):
    if not steps:
        return

    # Get canvas dimensions
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # Find maximum value for scaling
    max_val = max(max(step) for step in steps)

    # Calculate bar width
    bar_width = width / len(steps[-1])
    
    # Get animation speed from scale (inverse relationship)
    speed_factor = 1 / speed_scale.get()
    base_delay = 0.1  # Base delay in seconds
    delay = base_delay * speed_factor
    
    # Colors for visualization
    ACTIVE_COLOR = "#FF5722"  # Orange for active elements
    SORTED_COLOR = "#4CAF50"  # Green for sorted elements
    
    for i, step in enumerate(steps):
        canvas.delete("all")  # Clear previous frame
        
        # Draw background grid
        for x in range(0, width, 50):
            canvas.create_line(x, 0, x, height, fill="#E0E0E0", dash=(1, 5))
        for y in range(0, height, 50):
            canvas.create_line(0, y, width, y, fill="#E0E0E0", dash=(1, 5))

        # Draw bars
        for j, val in enumerate(step):
            # Calculate bar height
            bar_height = (val / max_val) * (height - 40)  # Leave space for value labels
            
            # Calculate position
            x0 = j * bar_width + 2  # Add small gap between bars
            y0 = height - bar_height - 20  # Leave space at bottom
            x1 = (j + 1) * bar_width - 2
            y1 = height - 20

            # Determine bar color
            if i == len(steps) - 1:  # Last step - all sorted
                color = SORTED_COLOR
            elif j == i:  # Active element
                color = ACTIVE_COLOR
            else:
                color = THEME['bar']

            # Draw bar with 3D effect
            canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=color,
                outline="",
                tags="bars"
            )
            
            # Add value label
            canvas.create_text(
                (x0 + x1) / 2,
                y1 + 10,
                text=str(val),
                font=('Segoe UI', 8),
                fill=THEME['text']
            )

        # Update progress
        progress = (i + 1) / len(steps) * 100
        canvas.create_text(
            width - 10,
            10,
            text=f"Progress: {progress:.1f}%",
            anchor='e',
            font=PROFESSIONAL_FONTS['body'],
            fill=THEME['text']
        )

        # Update canvas and sorted array display
        canvas.update()
        sorted_var.set(", ".join(map(str, step)))
        
        # Delay for animation
        if i < len(steps) - 1:  # No delay for the last step
            time.sleep(delay)

    # Final update of sorted array
    sorted_var.set(", ".join(map(str, steps[-1])))

# Function to reset input
def reset_input():
    entry_array.delete(0, tk.END)
    complexity_var.set("")
    result_var.set("")
    canvas.delete("all")

# Function to export results to CSV
def export_to_csv():
    global last_sorted
    if not last_sorted:
        messagebox.showerror("Error", "No sorting results to export")
        return

    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not file_path:
            return

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Index", "Value"])
            for i, val in enumerate(last_sorted):
                writer.writerow([i, val])

        messagebox.showinfo("Success", f"Results exported to {file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export: {str(e)}")

# Function to copy results to clipboard
def copy_to_clipboard():
    global last_sorted
    if not last_sorted:
        messagebox.showerror("Error", "No sorting results to copy")
        return

    try:
        text = ", ".join(str(x) for x in last_sorted)
        pyperclip.copy(text)
        messagebox.showinfo("Success", "Results copied to clipboard")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy: {str(e)}")

# Helper functions for modern UI elements
def create_modern_button(parent, text, command, color):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=PROFESSIONAL_FONTS['button'],
        bg=color,
        fg='white',
        padx=20,
        pady=10,
        relief='flat',
        cursor='hand2'
    )
    
    def on_enter(e):
        btn['bg'] = blend_color(color, '#FFFFFF', 0.1)
    
    def on_leave(e):
        btn['bg'] = color
    
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    return btn

def blend_color(color1, color2, factor):
    """Blend two colors together"""
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return f'#{r:02x}{g:02x}{b:02x}'

def clear_placeholder(event, entry):
    if entry.get() == "Enter numbers separated by commas":
        entry.delete(0, tk.END)
        entry.config(fg=THEME['text'])

def restore_placeholder(event, entry):
    if entry.get() == "":
        entry.insert(0, "Enter numbers separated by commas")
        entry.config(fg='gray')

def generate_random_array():
    import random
    size = random.randint(5, 20)  # Random size between 5 and 20
    arr = [random.randint(1, 100) for _ in range(size)]
    entry_array.delete(0, tk.END)
    entry_array.insert(0, ", ".join(map(str, arr)))

if __name__ == "__main__":
    setup_main_window()
    create_main_layout()
    apply_theme()
    root.mainloop()
