import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk
import subprocess

class LogoScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Logo Screen")
        self.attributes('-fullscreen', True)  # Make the window fullscreen
        self.configure(bg="black")

        # Load logo image and resize
        current_dir = "adminFiles"
        logo_path = os.path.join(current_dir, "logo.jpg")
        # folderPath = "adminFiles"
        # logo_path = os.path.join(folderPath, "logo.jpg")
        original_logo = Image.open(logo_path)
        width, height = original_logo.size
        ratio = min(300 / width, 200 / height)
        new_size = (int(width * ratio), int(height * ratio))
        resized_logo = original_logo.resize(new_size)
        self.logo_image = ImageTk.PhotoImage(resized_logo)

        # Display logo on the label
        self.logo_label = tk.Label(self, image=self.logo_image, bg="black")
        self.logo_label.pack(pady=100)

        # Text below logo
        bold_text_label = tk.Label(self, text="HandWave", font=("Helvetica", 14, "bold"), fg="white", bg="black")
        bold_text_label.pack()

        # Additional text
        additional_text_label = tk.Label(self, text="Made by Ritesh Kumar and Hirdhya Khanna", font=("Helvetica", 12), fg="white", bg="black")
        additional_text_label.pack()

        # After 1 second, transition to the main screen
        self.after(2000, self.open_main_app)

    def open_main_app(self):
        # Close the logo screen
        self.destroy()

        # Open the main app
        MainApp()   # MainApp().mainloop()
class LoadingScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Loading...")
        self.attributes('-fullscreen', True)  # Make the window fullscreen
        self.configure(bg="black")

        # Loading text
        loading_label = ttk.Label(self, text="Loading...", font=("Helvetica", 20), background="black", foreground="white")
        loading_label.pack(pady=50)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HandWave")
        self.attributes('-fullscreen', True)  # Make the window fullscreen
        self.configure(bg="black")

        # Get the screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()


        # Create heading label with larger font size
        heading_label = tk.Label(self, text="Handwave", font=("Helvetica", 36), fg="white", bg="black")  # Increased font size to 36
        heading_label.pack(pady=(100, 20))  # Padding (100 px from top, 20 px from bottom)

        # Create frame for left side
        left_frame = tk.Frame(self, bg="black")
        left_frame.pack(side="left", fill="both", expand=True)

        # # Label to display instructions
        # self.instruction_label = ttk.Label(left_frame, background="white")
        # self.instruction_label.pack(side="left", padx=10)

        # Label to display instructions
        self.instruction_label = ttk.Label(left_frame, background="white")
        self.instruction_label.pack(side="left", padx=10, pady=(0, 50), expand=True)


        # Create frame for right side
        right_frame = tk.Frame(self, bg="black")
        right_frame.pack(side="right", fill="both", expand=True)

        # Label to display the total number of pictures
        self.pic_count_label = tk.Label(right_frame, text="Total Pictures: 0", font=("Helvetica", 14), background="black", foreground="white")
        self.pic_count_label.pack(pady=(50, 20))
        
        # Reset the Presentation folder automatically
        self.reset_photos()
        # Create a frame to center the buttons vertically
        button_frame = tk.Frame(right_frame, bg="black")
        button_frame.pack(expand=True)

        # Button to add photos
        add_photos_button = tk.Button(button_frame, text="Add Photos", fg="white", bg="black", font=("Helvetica", 14), width=10, command=self.add_photos)
        add_photos_button.pack(pady=5)
        
        # Button to add folder
        add_folder_button = tk.Button(button_frame, text="Add Folder", fg="white", bg="black", font=("Helvetica", 14), width=10, command=self.add_folder)
        add_folder_button.pack(pady=5)

        # Button to reset photos
        reset_button = tk.Button(button_frame, text="Reset Photos", fg="white", bg="black", font=("Helvetica", 14), width=10, command=self.reset_photos)
        reset_button.pack(pady=5)

        # Close button
        close_button = tk.Button(right_frame, text="Close", fg="white", bg="black", font=("Helvetica", 14), command=self.close_app)
        close_button.pack(side="bottom", pady=(20, 50), anchor='s')  # Move the close button down and add extra padding, align to south

        # Create a new button aligned with close button
        open_exe_button = tk.Button(right_frame, text="AutoPresent", fg="white", bg="black", font=("Helvetica", 14), width=10,command=self.open_main_exe)
        open_exe_button.pack(side="bottom", pady=(20, 50), anchor='s')  # Move the new button down and add extra padding, align to south
        # # Button to open the other executable
        # open_exe_button = ttk.Button(self, text="Open Main Exe", command=self.open_main_exe)
        # open_exe_button.pack(pady=10)
        # Counter to generate unique filenames
        self.file_counter = 1

        # Start displaying instructions
        self.display_instructions()



    def open_main_exe(self):
        # Check if Presentation folder is empty
        presentation_folder = "Presentation"
        if os.listdir(presentation_folder):
            # Open the other executable
            exe_path = "main.exe"
            subprocess.Popen(exe_path)

            # Show the loading screen
            loading_screen = LoadingScreen(self)

            # Schedule the closing of the loading screen after 12 seconds
            self.after(12000, loading_screen.destroy)

            # Close the main screen after 12 seconds
            self.after(12000, self.destroy)
        else:
            # Inform the user that the Presentation folder is empty
            messagebox.showinfo("Info", "The Presentation folder is empty.")

    def close_app(self):
        # Close the main app
        self.destroy()

    def add_photos(self):
        # Open file dialog to select photos
        file_paths = filedialog.askopenfilenames(title="Select Photos", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])

        if file_paths:
            # Resize images and copy them to Presentation folder
            for file_path in file_paths:
                self.resize_and_copy_image(file_path)

    def add_folder(self):
        # Open directory dialog to select a folder
        folder_path = filedialog.askdirectory(title="Select Folder")

        if folder_path:
            # Get all image files in the selected folder
            image_files = [file for file in os.listdir(folder_path) if file.endswith((".jpg", ".jpeg", ".png", ".gif"))]
            if image_files:
                # Resize images and copy them to Presentation folder
                for image_file in image_files:
                    file_path = os.path.join(folder_path, image_file)
                    self.resize_and_copy_image(file_path)
            else:
                messagebox.showwarning("Warning", "No image files found in the selected folder.")

    def resize_and_copy_image(self, file_path):
        # Create the Presentation folder if it doesn't exist
        presentation_folder = "Presentation"
        os.makedirs(presentation_folder, exist_ok=True)

        # Open image
        image = Image.open(file_path)
                
        # Resize image according to screen size
        resized_image = self.resize_image(image)
                
        # Save resized image with unique filename
        _, file_extension = os.path.splitext(file_path)
        new_file_name = os.path.join(presentation_folder, f"{self.file_counter}{file_extension}")
        resized_image.save(new_file_name)

        # Increment counter for next photo
        self.file_counter += 1

        # Update total number of pictures label
        total_pics = len(os.listdir(presentation_folder))
        self.pic_count_label.config(text=f"Total Pictures: {total_pics}")

    def resize_image(self, image):
        # Resize image to full screen size
        resized_image = image.resize((self.screen_width, self.screen_height))
        return resized_image
    
    def reset_photos(self):
        # Get the Presentation folder path
        presentation_folder = os.path.join("Presentation")

        # Delete all files in the Presentation folder
        for file_name in os.listdir(presentation_folder):
            file_path = os.path.join(presentation_folder, file_name)
            os.remove(file_path)

        # Reset the counter
        self.file_counter = 1

        # Update the total number of pictures label
        self.pic_count_label.config(text="Total Pictures: 0")

    def close_app(self):
        # Close the main app
        self.destroy()

    def display_instructions(self):
        # Get the instruction folder path
        # instruction_folder = os.path.join(current_dir, "Instruction")
        instruction_folder = os.path.join("adminFiles", "Instruction")

        # Get the list of image files in the instruction folder
        image_files = [file for file in os.listdir(instruction_folder) if file.endswith((".jpg", ".jpeg", ".png", ".gif"))]

        # Initialize current index
        current_index = 0

        def show_image():
            nonlocal current_index
            # Load the current image
            image_path = os.path.join(instruction_folder, image_files[current_index])
            image = Image.open(image_path)
            image = image.resize((900, 600))  # Resize the image to fit the window
            photo = ImageTk.PhotoImage(image)

            # Update the instruction label
            self.instruction_label.config(image=photo)
            self.instruction_label.image = photo

            # Increment the index for the next image
            current_index = (current_index + 1) % len(image_files)

            # Schedule the next image update after 2 seconds
            self.after(3000, show_image)

        # Display the first image
        show_image()

if __name__ == "__main__":
    app = LogoScreen()
    app.mainloop()
