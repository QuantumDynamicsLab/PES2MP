import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os
import sys
import shutil
from tkinter import ttk

# color scheme
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
        
        # default folder
        default_folder = os.path.join(os.getcwd(), "GUI_examples")
        os.makedirs(default_folder, exist_ok=True)

        self.scripts = {
            "1D": ["1_pesgen1D", "opt_plot1D", "2_FnFit1D"],
            "2D": ["1_pesgen2D", "opt_NNfit2D", "opt_plot2D", "2_FnFit2D", "3_MPExp2D", "4_FnFit_Vlam2D", "opt_residual2D"],
            "4D": ["1_pesgen4D", "opt_NNfit4D", "opt_plot4D", "2_FnFit4D", "3_MPExp4D", "4_FnFit_Vlam4D", "opt_residual4D"]
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
            "4_FnFit_Vlam4D": "MP_files/VlamFnFit",
            "opt_residual4D": "MP_files/Residuals_Inv_Fit",
        }
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR)
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TNotebook', background=BG_COLOR)
        style.configure('TNotebook.Tab', background=HEADER_COLOR, foreground=TEXT_COLOR)
        style.configure('TCombobox', fieldbackground=BG_COLOR)
        style.configure('TButton', background=ACCENT_COLOR)
        
        self.create_widgets(default_folder)

        #  dynamic window size
        self.adjust_window_size()


    def adjust_window_size(self):
        # adjusting window size based on content
        self.root.update_idletasks()

        required_width = self.root.winfo_reqwidth()
        required_height = self.root.winfo_reqheight()

        # maximum and minimum threshold foe window
        max_width = 1000
        max_height = 800
        min_width = 400  # Minimum width
        min_height = 300  # Minimum height

        # Set the window size weith and height
        final_width = min(required_width, max_width)
        final_height = min(required_height, max_height)

        # ensure proper width 
        final_width = max(final_width, min_width)
        final_height = max(final_height, min_height)

        self.root.geometry(f"{final_width}x{final_height}")

        # Set the minimum window size (to prevent shrinking too small)
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
 
        ttk.Button(settings_frame, text="Select Folder & Copy PES2MP Files", command=self.select_folder).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
#        ttk.Button(settings_frame, text="Browse", command=self.select_folder).grid(row=1, column=2, padx=5, pady=5)
#        ttk.Button(settings_frame, text="Copy PES2MP Files", command=self.copy_pes2mp_files).grid(row=1, column=3, padx=5, pady=5)


        # Project Name
        tk.Label(settings_frame, text="Project Name:", fg=TEXT_COLOR, bg=BG_COLOR, \
                 font=(None, 11)).grid(row=2, column=0, sticky="w")
        self.project_var = tk.StringVar()
        ttk.Entry(settings_frame, textvariable=self.project_var, width=20, font=(None, 11)).grid(row=2, column=1, sticky="w")

        # Create/Open Project Folder button
        ttk.Button(settings_frame, text="Create Project Folder", command=self.create_project_folder).grid(row=2, column=2, padx=5)
        ttk.Button(settings_frame, text="Open Project Folder", command=self.open_project_folder).grid(row=2, column=3, padx=5)




        # Custom File Name Input
        custom_file_frame = ttk.Frame(self.root)
        custom_file_frame.pack(padx=20, pady=2, fill=tk.X)

        #ttk.Separator(custom_file_frame, orient="horizontal").grid(row=-1, column=0, columnspan=6, sticky="ew", pady=5)
        ttk.Label(custom_file_frame, text="---------------- Optional Entry (Run Custom Scripts) ----------------", foreground="gray").grid(row=0, column=0, columnspan=6, pady=2)
      
        # File name input
        tk.Label(custom_file_frame, text="Custom Script:", bg=BG_COLOR, fg=TEXT_COLOR, font=(None, 11)).grid(row=1, column=1, sticky="w")
        self.file_name_var = tk.StringVar()
        ttk.Entry(custom_file_frame, textvariable=self.file_name_var, width=30, font=(None, 11)).grid(row=1, column=2, sticky="w")
        
        # Static .py label (not editable)
        tk.Label(custom_file_frame, text=".py", bg=BG_COLOR, fg=TEXT_COLOR, font=(None, 11)).grid(row=1, column=3, sticky="w")
        
        # Open button
        ttk.Button(custom_file_frame, text="Open File", command=self.open_custom_file).grid(row=1, column=4, padx=5)
        
        # Run button
        ttk.Button(custom_file_frame, text="Run", command=self.run_custom_file).grid(row=1, column=5, padx=5)        
        
        tab_labels = {
            "1D": ("Atom - Atom Collision", "●  → ←  ○"),
            "2D": ("Rigid Rotor - Atom Collision", "/  → ←  ∘"),
            "4D": ("Rigid Rotor - Rigid Rotor Collision", "/  → ←  \\"),
        }
        # Script Tabs
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for dimension in ["1D", "2D", "4D"]:
            tab_frame = ttk.Frame(self.tabs)
            self.tabs.add(tab_frame, text=dimension)
            self.create_script_panel(tab_frame, dimension)
            # Add bottom labels
            title, symbol = tab_labels[dimension]
            if title:
                ttk.Label(tab_frame, text=title, font=("Arial", 14, "bold")).pack(side="bottom", pady=(2, 0))
            if symbol:
                ttk.Label(tab_frame, text=symbol, font=("Segoe UI Symbol", 20)).pack(side="bottom", pady=(0, 0))
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


        # Footer heading
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
            # Check for mixing dimensions (redundant check along with tabs)
            if self.selected_category and self.selected_category != script_cat:
                messagebox.showerror("Error", "Cannot mix script dimensions!")
                var.set(False)
                return
            # Set the category if not already set
            self.selected_category = script_cat
            # Add the script if it is not already in the list
            if script not in self.selected_scripts:
                self.selected_scripts.append(script)
            # sort selected scripts based on order in the full list (top-to-bottom)
            self.selected_scripts.sort(key=lambda s: self.scripts[self.selected_category].index(s))
        else:
            if script in self.selected_scripts:
                self.selected_scripts.remove(script)
            if not self.selected_scripts:
                self.selected_category = None

        # Update the label display.
        self.sequence_label.config(text=f"Selected scripts: {', '.join(self.selected_scripts) or 'None'}")


    def get_script_category(self, script):
        for dim, scripts in self.scripts.items():
            if script in scripts:
                return dim
        return None

    def select_folder(self):
        try:
            initial_dir = self.folder_var.get()
        except:
            initial_dir = os.getcwd()
        folder = filedialog.askdirectory(initialdir=initial_dir)
        if folder:
            self.folder_var.set(folder)
            self.folder_entry.xview_moveto(1) 
            #os.chdir(folder)
            messagebox.showinfo("Info", f"Working directory changed to:\n{folder}")
            self.copy_pes2mp_files()

    def copy_pes2mp_files(self):
        # source file paths
        src_file1 = os.path.join(os.getcwd(), "pes2mp.py")
        src_file2 = os.path.join(os.getcwd(), "pes2mp_driver.py")
        dest_folder = self.folder_var.get()  # Destination folder selected by the user

        # Check if source files exist
        missing_files = [f for f in [src_file1, src_file2] if not os.path.exists(f)]
        if missing_files:
            messagebox.showerror("Error", f"Source file(s) not found:\n{', '.join(missing_files)}")
            return
            
        # Destination file paths
        dest_file1 = os.path.join(dest_folder, "pes2mp.py")
        dest_file2 = os.path.join(dest_folder, "pes2mp_driver.py") 
               
        # Check for existing files
        existing_files = [f for f in [dest_file1, dest_file2] if os.path.exists(f)]
        if existing_files:
            response = messagebox.askyesno(
                "Overwrite Confirmation",
                f"The following file(s) already exist:\n\n" +
                "\n".join(os.path.basename(f) for f in existing_files) +
                "\n\nDo you want to overwrite them?"
            )
            if not response:
                return  # User chose not to overwrite
            
        try:
            shutil.copy(src_file1, dest_folder)
            shutil.copy(src_file2, dest_folder)
            messagebox.showinfo("Success", f"Copied PES2MP.py and PES2MP_driver.py to:\n{dest_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy files:\n{e}")


    def run_script(self, script):
        if not self.validate_project():
            return
            
        # Get the terminal command
        #terminal_cmd = self.get_terminal_command()
        
        folder = self.folder_var.get()
        env = self.env_var.get()
        project = self.project_var.get()
        log_file = f"Projects/outv_{project}.log"  # log file location

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

    def run_custom_file(self):
        file_name = self.file_name_var.get().strip()
        if not file_name:
            messagebox.showerror("Error", "Please provide a file name!")
            return
        folder = self.folder_var.get()
        env = self.env_var.get()
        project = self.project_var.get()
        inner_command = (
            f"source $(conda info --base)/etc/profile.d/conda.sh && "
            f"cd {folder} && "
            f"conda activate {env} && "
            f"python3 pes2mp.py {file_name} ; "
            f"exec $SHELL"
        )
        if sys.platform == "darwin":
            apple_script = f'''
            tell application "Terminal"
                do script "{inner_command}"
                activate
            end tell'''
            subprocess.Popen(["osascript", "-e", apple_script])
        else:
            subprocess.Popen(inner_command, shell=True)

    def run_sequence(self):
        if not self.selected_scripts:
            messagebox.showwarning("Warning", "No scripts selected!")
            return
            
        if not self.validate_project():
            return
            
        #terminal_cmd = self.get_terminal_command()
        
        folder = self.folder_var.get()
        env = self.env_var.get()
        project = self.project_var.get()
        log_file = f"Projects/outv_{project}.log"  # log file location
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


    def open_custom_file(self):
        file_name = self.file_name_var.get().strip()
        if not file_name:
            messagebox.showerror("Error", "Please provide a file name!")
            return
        file_path = os.path.join(self.folder_var.get(), f"{file_name}.py")
        if sys.platform == "darwin":
            subprocess.Popen(["open", file_path])
        elif sys.platform == "linux":
            subprocess.Popen(["xdg-open", file_path])


    def open_script_folder(self, script):
        project_name = self.project_var.get().strip()
        if not project_name:
            messagebox.showerror("Error", "Project name is required!")
            return
        folder_mapping = self.script_folders.get(script, script)
        folder_path = os.path.join(self.folder_var.get(), "Projects", self.project_var.get(), folder_mapping)
        if sys.platform == "darwin":
            subprocess.Popen(["open", folder_path])
        elif sys.platform == "linux":
            subprocess.Popen(["xdg-open", folder_path])

    def create_project_folder(self):
        project_name = self.project_var.get().strip()
        if not project_name:
            messagebox.showerror("Error", "Project name is required!")
            return
    
        # Define the folder path
        folder_path = os.path.join(self.folder_var.get(), "Projects", project_name)
        
        # Create folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

    def open_project_folder(self):
        project_name = self.project_var.get().strip()
        if not project_name:
            messagebox.showerror("Error", "Project name is required!")
            return
        folder_path = os.path.join(self.folder_var.get(), "Projects", project_name)
        # Check if the folder exists
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", f"The folder does not exist:\n{folder_path}")
            return
 
        # Open the folder based on the OS
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", folder_path])
            elif sys.platform == "linux":
                subprocess.Popen(["xdg-open", folder_path])
            else:
                messagebox.showerror("Error", "Unsupported operating system!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")



    
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
