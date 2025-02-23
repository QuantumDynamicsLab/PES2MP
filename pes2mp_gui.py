import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import sys
import shutil
from tkinter import ttk

# Define color scheme
# Define color scheme
BG_COLOR = "whitesmoke"  
TEXT_COLOR = "black"  
ACCENT_COLOR = "lightblue"  
HEADER_COLOR = "gainsboro"  
OPTIONAL_SCRIPT_COLOR = "crimson"  
SCRIPT_BOX_COLOR = "silver"  
HOVER_COLOR = "forestgreen" 

class PES2MPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PES2MP GUI")
        self.root.config(bg=BG_COLOR)
        
        # Default folder setup
        default_folder = os.path.join(os.getcwd(), "PES2MP_GUI")
        os.makedirs(default_folder, exist_ok=True)

        self.scripts = {
            "1D": ["1_pesgen1D", "opt_plot1D", "2_FnFit1D"],
            "2D": ["1_pesgen2D", "opt_NNfit2D", "opt_plot2D", "2_FnFit2D", "3_MPExp2D", "4_FnFit_Vlam2D", "opt_residual2D"],
            "4D": ["1_pesgen4D", "opt_NNfit4D", "opt_plot4D", "2_FnFit4D", "3_MPExp4D", "4_FnFit_Vlam4D"]
        }

        self.selected_scripts = []
        self.selected_category = None
        self.check_vars = {}
        self.script_folders = {
            "1_pesgen1D": "psi4_PES_data",
            "opt_plot1D": "plots",
            "2_FnFit1D": "PESFnFit",
            
            "1_pesgen2D": "psi4_PES_data",
            "opt_plot2D": "plots",
            "opt_NNfit2D": "NN_files",
            "2_FnFit2D": "PESFnFit",
            "3_MPExp2D": "MP_files",
            "4_FnFit_Vlam2D": "MP_files/VlamFnFit",
            "opt_residual2D": "MP_files/Residuals_Inv_Fit",
            
            "1_pesgen4D": "psi4_PES_data",
            "opt_plot4D": "plots",
            "opt_NNfit4D": "NN_files",
            "2_FnFit4D": "PESFnFit",
            "3_MPExp4D": "MP_files",
            "4_FnFit_Vlam4D": "MP_files/VlamFnFit"
        }
        
        # Configure ttk styles for Mac compatibility
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TNotebook', background=BG_COLOR)
        style.configure('TNotebook.Tab', background=HEADER_COLOR, foreground=TEXT_COLOR)
        style.configure('TCombobox', fieldbackground=BG_COLOR)
        style.configure('TButton', background=ACCENT_COLOR)
        
        self.create_widgets(default_folder)

        # Adjust window size dynamically based on content size
        self.adjust_window_size()


    def adjust_window_size(self):
        # Get the required size for the window based on the content
        # First, update the layout to get the proper requested size of the window
        self.root.update_idletasks()

        required_width = self.root.winfo_reqwidth()
        required_height = self.root.winfo_reqheight()

        # Define maximum and minimum threshold
        max_width = 1000
        max_height = 700
        min_width = 400  # Minimum width
        min_height = 300  # Minimum height

        # Set the window size, but don't exceed the max dimensions
        final_width = min(required_width, max_width)
        final_height = min(required_height, max_height)

        # Ensure the window isn't smaller than the minimum size
        final_width = max(final_width, min_width)
        final_height = max(final_height, min_height)

        self.root.geometry(f"{final_width}x{final_height}")

        # Set a minimum window size (to prevent shrinking too small)
        self.root.minsize(min_width, min_height)

    def create_widgets(self, default_folder):
        # Header
        title_label = tk.Label(self.root, text="PES2MP Setup", fg=TEXT_COLOR, bg=HEADER_COLOR, 
                             font=("Helvetica", 18, "bold"), pady=10)
        title_label.pack(fill=tk.X)

        # Settings Panel (always visible)
        settings_frame = ttk.Frame(self.root)
        settings_frame.pack(padx=20, pady=10, fill=tk.X)

        # Environment Selection
        tk.Label(settings_frame, text="Anaconda Environment:", fg=TEXT_COLOR, bg=BG_COLOR, \
                 font=(None, 11)).grid(row=0, column=0, sticky="w")
        self.env_var = tk.StringVar(value="pes2mp")
        ttk.Combobox(settings_frame, textvariable=self.env_var, 
                    values=["pes2mp", "pes2mp_q"], state="readonly", font=(None, 11)).grid(row=0, column=1)

        # Folder Selection
        tk.Label(settings_frame, text="Working Folder:" , fg=TEXT_COLOR, bg=BG_COLOR, \
                font=(None, 11)).grid(row=1, column=0, sticky="w")
                

        self.folder_var = tk.StringVar(value=default_folder)
        #ttk.Entry(settings_frame, textvariable=self.folder_var, state="readonly", font=(None, 11),width=25).grid(row=1, column=1)
        self.folder_entry = ttk.Entry(settings_frame, textvariable=self.folder_var, 
                                     state="readonly", font=(None, 11), width=25)

        self.folder_entry.grid(row=1, column=1, sticky="ew")
        self.folder_entry.xview_moveto(1)  # Auto-scroll to rightmost position
        
        ttk.Button(settings_frame, text="Browse", command=self.select_folder).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(settings_frame, text="Copy PES2MP Files", command=self.copy_pes2mp_files).grid(row=1, column=3, padx=5, pady=5)


        # Project Name
        tk.Label(settings_frame, text="Project Name:", fg=TEXT_COLOR, bg=BG_COLOR, \
                 font=(None, 11)).grid(row=2, column=0, sticky="w")
        self.project_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.project_var, font=(None, 11)).grid(row=2, column=1)

        # Script Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for dimension in ["1D", "2D", "4D"]:
            tab_frame = ttk.Frame(self.tabs)
            self.tabs.add(tab_frame, text=dimension)
            self.create_script_panel(tab_frame, dimension)

        # Execution controls
            
        self.sequence_label = tk.Label(self.root, text="Selected scripts: None", 
                                     bg=BG_COLOR, fg=TEXT_COLOR)
        self.sequence_label.pack(pady=5)
        
        if sys.platform == "darwin":
            execute_btn = tk.Button(
                self.root, 
                text="Execute Sequence", 
                bg="#A9A9A9", 
                fg=TEXT_COLOR, 
                font=(None, 16),
                relief="groove", 
                command=self.run_sequence
            )
            execute_btn.bind("<Enter>", lambda e: execute_btn.config(fg="green"))
            execute_btn.bind("<Leave>", lambda e: execute_btn.config(fg="black"))
        else:
            execute_btn = tk.Button(
                self.root, 
                text="Execute Sequence", 
                bg="#A9A9A9", 
                fg=TEXT_COLOR, 
                font=(None, 16),
                relief="groove", 
                activebackground="lightgrey", 
                activeforeground="green",
                command=self.run_sequence
            )
        execute_btn.pack(pady=10)


        # Footer
        tk.Label(self.root, text="Quantum Dynamics Lab, IIT Ropar", bg=BG_COLOR, 
                fg=TEXT_COLOR).pack(side=tk.BOTTOM, pady=10)

        # Tab change handler
        self.tabs.bind("<<NotebookTabChanged>>", self.handle_tab_change)

    def create_script_panel(self, parent, dimension):
        for script in self.scripts[dimension]:
            frame = tk.Frame(parent, bg=SCRIPT_BOX_COLOR, padx=5, pady=2)
            frame.pack(fill=tk.X, pady=2)

            # Script name and checkbox
            tk.Label(frame, text=script, bg=SCRIPT_BOX_COLOR,
                   fg=OPTIONAL_SCRIPT_COLOR if "opt" in script else TEXT_COLOR).pack(side=tk.LEFT)
            
            check_var = tk.BooleanVar()
            tk.Checkbutton(frame, variable=check_var, bg=SCRIPT_BOX_COLOR,
                         command=lambda s=script, v=check_var: self.update_selection(s, v)).pack(side=tk.LEFT)
            self.check_vars[script] = check_var

            # Action buttons with hover effects
            btn_frame = tk.Frame(frame, bg=SCRIPT_BOX_COLOR)
            btn_frame.pack(side=tk.RIGHT)

            button_configs = [
                ("Open File", self.open_script_file),
                ("Run", self.run_script),
                ("Open Output Folder", self.open_script_folder)
            ]

            for btn_text, command in button_configs:
                if sys.platform == "darwin":
                    btn = tk.Button(
                        btn_frame, 
                        text=btn_text, 
                        bg="#A9A9A9", 
                        fg=TEXT_COLOR, 
                        font=(None, 16),
                        relief="groove", 
                        command=lambda s=script, cmd=command: cmd(s)
                    )
                    btn.bind("<Enter>", lambda e, b=btn: b.config(fg="green"))
                    btn.bind("<Leave>", lambda e, b=btn: b.config(fg="black"))
                else:
                    btn = tk.Button(
                        btn_frame, 
                        text=btn_text, 
                        bg="#A9A9A9", 
                        fg=TEXT_COLOR, 
                        font=(None, 16),
                        relief="groove", 
                        activebackground="lightgrey", 
                        activeforeground="green",
                        command=lambda s=script, cmd=command: cmd(s)
                    )
                btn.pack(side=tk.LEFT, padx=2)

    def handle_tab_change(self, event):
        # Clear selections when switching tabs
        current_tab = self.tabs.tab(self.tabs.select(), "text")
        for script, var in self.check_vars.items():
            if script in self.scripts[current_tab]:
                var.set(False)
        self.selected_scripts.clear()
        self.selected_category = None
        self.sequence_label.config(text="Selected scripts: None")

    def update_selection(self, script, var):
        script_cat = self.get_script_category(script)
        if var.get():
            # Check for mixing dimensions
            if self.selected_category and self.selected_category != script_cat:
                messagebox.showerror("Error", "Cannot mix script dimensions!")
                var.set(False)
                return
            # Set the category if not already set
            self.selected_category = script_cat
            # Add the script if it is not already in the list
            if script not in self.selected_scripts:
                self.selected_scripts.append(script)
            # Always sort the selected scripts based on their order in the full list (top-to-bottom)
            self.selected_scripts.sort(key=lambda s: self.scripts[self.selected_category].index(s))
        else:
            if script in self.selected_scripts:
                self.selected_scripts.remove(script)
            if not self.selected_scripts:
                self.selected_category = None

        # Update the label that displays the selected scripts.
        self.sequence_label.config(text=f"Selected scripts: {', '.join(self.selected_scripts) or 'None'}")


    def get_script_category(self, script):
        for dim, scripts in self.scripts.items():
            if script in scripts:
                return dim
        return None

    def select_folder(self):
        initial_dir = os.getcwd()
        folder = filedialog.askdirectory(initialdir=initial_dir)
        if folder:
            self.folder_var.set(folder)
            self.folder_entry.xview_moveto(1)  # <-- Add this line
            #os.chdir(folder)
            messagebox.showinfo("Info", f"Working directory changed to:\n{folder}")

    def copy_pes2mp_files(self):
        # Define source file paths
        src_file1 = os.path.join(os.getcwd(), "pes2mp.py")
        src_file2 = os.path.join(os.getcwd(), "pes2mp_driver.py")
        dest_folder = self.folder_var.get()  # Destination folder selected by the user

        # Check if source files exist
        missing_files = [f for f in [src_file1, src_file2] if not os.path.exists(f)]
        if missing_files:
            messagebox.showerror("Error", f"Source file(s) not found:\n{', '.join(missing_files)}")
            return

        try:
            shutil.copy(src_file1, dest_folder)
            shutil.copy(src_file2, dest_folder)
            messagebox.showinfo("Success", f"Copied PES2MP.py and PES2MP_driver.py to:\n{dest_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy files:\n{e}")

    def run_script(self, script):
        if not self.validate_project():
            return
            
        # Get the terminal command once
        #terminal_cmd = self.get_terminal_command()
        
        # Wrap folder and project variables in double quotes to handle spaces
        folder = self.folder_var.get()
        env = self.env_var.get()
        project = self.project_var.get()
        log_file = f"Projects/outv_{project}.log"  # Define your log file location

        inner_command = (
            f"source $(conda info --base)/etc/profile.d/conda.sh && "
            f"cd {folder} && "
            f"conda activate {env} && "
            f"export Proj_name={project} && "
            f"python3 pes2mp.py {script} ; "
            f"exec $SHELL"
        )
        if (sys.platform == "darwin"):
            
            apple_script = f'''
            tell application "Terminal"
                do script "{inner_command}"
                activate
            end tell '''
            subprocess.Popen(["osascript", "-e", apple_script])

        else:
            command = f'gnome-terminal -- bash -c \'{inner_command}\''
            subprocess.Popen(command, shell=True)

    def run_sequence(self):
        if not self.selected_scripts:
            messagebox.showwarning("Warning", "No scripts selected!")
            return
            
        if not self.validate_project():
            return
            
        # Get the terminal command once
        #terminal_cmd = self.get_terminal_command()
        
        # Wrap folder and project variables in double quotes to handle spaces
        folder = self.folder_var.get()
        env = self.env_var.get()
        project = self.project_var.get()
        log_file = f"Projects/outv_{project}.log"  # Define your log file location
        script_chain = " && ".join([f"python3 pes2mp.py {s} " for s in self.selected_scripts])

        inner_command = (
            f"source $(conda info --base)/etc/profile.d/conda.sh && "
            f"cd {folder} && "
            f"conda activate {env} && "
            f"export Proj_name={project} && "
            f"{script_chain}; "
            f"exec $SHELL"
        )
        if (sys.platform == "darwin"):
            
            apple_script = f'''
            tell application "Terminal"
                do script "{inner_command}"
                activate
            end tell '''
            subprocess.Popen(["osascript", "-e", apple_script])

        else:
            command = f'gnome-terminal -- bash -c \'{inner_command}\''
            subprocess.Popen(command, shell=True)

        
        #command = f"{terminal_cmd} -- $SHELL -c 'source $(conda info --base)/etc/profile.d/conda.sh \
        #&& cd {folder} && conda activate {env} && export Proj_name={project} && {script_chain} && exec $SHELL'"
        #subprocess.Popen(command, shell=True)

    def validate_project(self):
        if not self.project_var.get().strip():
            messagebox.showerror("Error", "Project name is required!")
            return False
        return True

    def open_script_file(self, script):
        file_path = os.path.join(self.folder_var.get(), f"{script}.py")
        if sys.platform == "darwin":
            subprocess.Popen(["open", file_path])
        elif sys.platform == "linux":
            subprocess.Popen(["xdg-open", file_path])

    def open_script_folder(self, script):
        project_name = self.project_var.get().strip()
        if not project_name:
            messagebox.showerror("Error", "Project name is required!")
            return
        # Use mapped folder name if available; otherwise, default to the script name.
        folder_mapping = self.script_folders.get(script, script)
        folder_path = os.path.join(self.folder_var.get(), "Projects", self.project_var.get(), folder_mapping)
        if sys.platform == "darwin":
            subprocess.Popen(["open", folder_path])
        elif sys.platform == "linux":
            subprocess.Popen(["xdg-open", folder_path])
    
    #def get_terminal_command(self):
    #    """Return the appropriate terminal command based on the platform."""
    #    if sys.platform == "darwin":  # macOS
    #        # Check for iTerm2, fallback to Terminal if not found
    #        if self.is_terminal_installed("iTerm"):
    #            return "open -a iTerm"
    #        else:
    #            return "open -a Terminal"
    #    elif sys.platform == "linux":  # Linux
    #        # Check for gnome-terminal, fallback to xterm if not found
    #        if self.is_terminal_installed("gnome-terminal"):
    #            return "gnome-terminal"
    #        else:
    #            return "xterm"
    #    else:
    #        raise ValueError("Unsupported platform")
    #def is_terminal_installed(self, terminal):
    #    return subprocess.call(["which", terminal], stdout=subprocess.DEVNULL) == 0

if __name__ == "__main__":
    root = tk.Tk()
    PES2MPGUI(root)
    root.mainloop()
