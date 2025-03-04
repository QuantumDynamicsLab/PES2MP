import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import tkinter.font as tkFont
#from tkinter import ttk

class InstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Installer GUI")
        self.root.config(bg="#f7f7f7")
        
        # frame 1
        signature_frame = tk.Frame(self.root, bg="#FAF0E6", pady=10, bd=2, relief="solid")
        signature_frame.pack(fill=tk.X)

        signature_label = tk.Label(signature_frame, text="PES2MP Installer", bg="#FAF0E6", fg="black",
                                   font=(None, 26, "bold"))
        signature_label.pack()
        
        self.create_widgets()

        signature_frame2 = tk.Frame(self.root, bg="white", pady=10, bd=2, relief="solid")
        signature_frame2.pack(fill=tk.X)

        it_font=tkFont.Font(family = None, size=12, weight='normal', slant = 'roman')
        signature_label5 = tk.Label(signature_frame2, text="-- Quantum Dynamics Lab, IIT Ropar",
                                   font=it_font, bg="white", fg="black")
        signature_label5.pack(anchor="e",ipadx=20)
          
        # dynamic size
        self.adjust_window_size()

    
    def adjust_window_size(self):
        self.root.update_idletasks()

        required_width = self.root.winfo_reqwidth()
        required_height = self.root.winfo_reqheight()

        # maximum and minimum threshold for window
        max_width = 1000
        max_height = 700
        min_width = 600  # Minimum width
        min_height = 300  # Minimum height

        final_width = min(required_width, max_width)
        final_height = min(required_height, max_height)

        final_width = max(final_width, min_width)
        final_height = max(final_height, min_height)

        self.root.geometry(f"{final_width}x{final_height}")

        # Set a minimum window size (to prevent shrinking too small)
        self.root.minsize(min_width, min_height)
    
    def create_widgets(self):

        frame = tk.Frame(self.root, bg="#f7f7f7")
        frame.pack(padx=20, pady=20, expand=True, fill="both")

        # List of scripts to run
        self.scripts = [
            {"name": "Install PES2MP", "script": "install_pes2mp.sh"},
            {"name": "Install PES2MP Quick", "script": "install_pes2mp_quick.sh"},
            {"name": "Uninstall PES2MP", "script": "uninstall_pes2mp.sh"},
            {"name": "Uninstall PES2MP Quick", "script": "uninstall_pes2mp_quick.sh"},            
            {"name": "Install Anaconda \u2192 Linux", "script": "install_anaconda_linux.sh"},
            {"name": "MacOS-Intel", "script": "install_anaconda_mac_intel.sh"},
            {"name": "MacOS-Apple Silicon", "script": "install_anaconda_mac_apple_silicon.sh.sh"},
            {"name": "Install Psi4 (API)", "script": "installu_psi4.sh"},
            {"name": "Install BLAS/LAPACK", "script": "installu_blas_lapack.sh"},
            {"name": "Install Miscellaneous", "script": "installu_etc.sh"},
            {"name": "Install Homebrew", "script": "install_brew.sh"},
            {"name": "Install BLAS/LAPACK", "script": "install_blas_lapack.sh"},
            {"name": "Install Miscellaneous", "script": "install_etc.sh"},
            ]
        # distribute space evenly
        for i in range(2):  # For each row
            frame.grid_rowconfigure(i, weight=1, uniform="equal")  # All rows should have the same weight
        for i in range(2):  # For each column
            frame.grid_columnconfigure(i, weight=1, uniform="equal")  # All columns should have the same weight

        # directories to change to
        self.script_dirs = (
            ["/makefiles"] * 2 +
            ["/makefiles/uninstall_pes2mp"] * 2 +
            ["/makefiles/anaconda_install"] * 3 +
            ["/makefiles/linux_essentials"] * 3 +
            ["/makefiles/macos_essentials"] * 3
        )


        self.buttons = []
        for i in range(4):
            row = i // 2  # Two columns per row
            col = i % 2  # Two columns per row

            script_name = self.scripts[i]["name"]
            #print(sys.platform)

            # Check if the system is macOS
            if (sys.platform == "darwin"):
                button = tk.Button(frame, text=script_name, bg="#A9A9A9", fg="black", font=(None, 16),
                                   relief="groove", command=lambda idx=i: self.run_script(idx))
                # Add hover effects
                button.bind("<Enter>", lambda event, btn=button, idx=i: self.on_hover(event, idx, btn))
                button.bind("<Leave>", lambda event, btn=button: self.on_leave(event, btn))

            else:
                if (i==2 or i==3):
                    button = tk.Button(frame, text=script_name, bg="#A9A9A9", fg="black", font=(None, 16),
                                       relief="groove", activebackground="silver", activeforeground="red",
                                       command=lambda idx=i: self.run_script(idx)) # width=30, height=2,
                else:
                    button = tk.Button(frame, text=script_name, bg="#A9A9A9", fg="black", font=(None, 16),
                                       relief="groove", activebackground="silver", activeforeground="green",
                                       command=lambda idx=i: self.run_script(idx)) # width=30, height=2,
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            #self.buttons.append(button)
        

        sections = [
            ("Anaconda Installer (Visit 'docs.anaconda.com' for latest version)", [4, 5, 6]),
            ("Linux Essentials  (Optional)", [7, 8, 9]),
            ("MacOS Essentials  (Optional)", [10, 11, 12])
        ]
        
        section_start_row = 2
        for s, (heading, indices) in enumerate(sections):
            #optional_heading = tk.Label(frame, text="Optional Installs", font=("Arial", 20, "bold"), bg="#f7f7f7", fg="black",)
            #optional_heading.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
            section_frame = tk.Frame(frame, bg="#f7f7f7")
            section_frame.grid(row=section_start_row + s, column=0, columnspan=2, sticky="ew", pady=5)
            
            heading_label = tk.Label(section_frame, text=heading, font=("Arial", 16, "bold"), bg="#f7f7f7", fg="black",)
            heading_label.pack(anchor="w", padx=10, pady=2)
            
            buttons_frame = tk.Frame(section_frame, bg="#f7f7f7")
            buttons_frame.pack(fill="x", padx=10)
            
           # buttons_frame.grid_rowconfigure(0, weight=1, uniform="equal")

            for j, idx in enumerate(indices):
                script_name = self.scripts[idx]["name"]
                if sys.platform == "darwin":
                    btn = tk.Button(buttons_frame, text=script_name, bg="#A9A9A9", fg="black", font=(None, 16),
                                    relief="groove", command=lambda idx=idx: self.run_script(idx))
                    btn.bind("<Enter>", lambda event, btn=btn, idx=idx: self.on_hover(event, idx, btn))
                    btn.bind("<Leave>", lambda event, btn=btn: self.on_leave(event, btn))
                else:
                    btn = tk.Button(buttons_frame, text=script_name, bg="#A9A9A9", fg="black", font=(None, 16),
                                    relief="groove", activebackground="silver", activeforeground="green",
                                    command=lambda idx=idx: self.run_script(idx))
                btn.grid(row=0, column=j, padx=10, pady=10, sticky="nsew")
                buttons_frame.grid_columnconfigure(j, weight=1, uniform="equal")

    def on_hover(self, event, i, button):
        """Handle hover event (mouse enter)"""
        #print(i)
        if (i==2 or i==3):
            button.config(bg="#228B22", fg="red")  # Darker green and white text
        else:
            button.config(bg="#228B22", fg="green")  # Darker green and white text
    def on_leave(self, event, button):
        """Handle leave event (mouse leave)"""
        button.config(bg="#32CD32", fg="black")  # Reset to original color            

    # def run_script(self, idx):
    #     """Runs the selected script from the list."""
    #     script = self.scripts[idx]["script"]  # Get the script name from the list
    #     #script_name = self.scripts[idx]["name"]  # Get the descriptive name
    #     script_dir = self.script_dirs[idx]  # Get the directory for the current script
    #     cwd = os.getcwd()

    #     try:
    #         os.chdir(cwd+script_dir)
    #         print()
    #         os.chmod(script, 0o755)

    #         # Run the Script using subprocess
    #         result = subprocess.run(["bash", script], capture_output=True, text=True)

    #         # Check if the Script(s) ran successfully
    #         if result.returncode == 0:
    #             messagebox.showinfo("Success", f"Script {script} ran successfully!")
    #         else:
    #             messagebox.showerror("Error", f"Script {script} failed:\n{result.stderr}")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"An error occurred while running {script}: {str(e)}")
        
    #     os.chdir(cwd)

    def run_script(self, idx):
        """Runs the selected script from the list by opening a new terminal window."""
        script = self.scripts[idx]["script"]  # e.g., "install_brew.sh"
        script_dir = self.script_dirs[idx]     # e.g., "/makefiles/uninstall_pes2mp"
        cwd = os.getcwd()
        target_dir = cwd+script_dir
        #print(target_dir)

        # save command to execute in the new terminal.
        command = f"cd '{target_dir}' && chmod +x {script} && ./{script}; exec $SHELL"
    
        try:
            if sys.platform == "darwin":
                # For macOS, use AppleScript to tell Terminal to run the command.
                apple_script = f'''
                tell application "Terminal"
                    do script "{command}"
                    activate
                end tell
                '''
                subprocess.Popen(["osascript", "-e", apple_script])
            else:
                # For Ubuntu (or other Linux distros with gnome-terminal installed)
                gnome_cmd = f'gnome-terminal -- bash -c "{command}"'
                subprocess.Popen(gnome_cmd, shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while running {script}: {str(e)}")



if __name__ == "__main__":
    # Create the Tkinter window
    root = tk.Tk()
    #root.tk.call('tk', 'scaling', 1.0)
    #style = ttk.Style()
    #style.theme_use("clam")  # Other themes: "alt", "default", "classic", "clam"

    #dpi = root.winfo_fpixels('1i')
    #print(dpi)
    app = InstallerGUI(root)
    root.mainloop()



