import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class ImageEditor:
    """
    Main class for the image editor application, managing GUI and image processing functionality
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        
        # Initialize variables
        self.original_image = None
        self.current_image = None
        self.cropped_image = None
        self.scale_factor = 1.0
        self.history = []
        self.history_index = -1
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create image display area
        self.create_image_display()
        
        # Create control panel
        self.create_control_panel()
        
        # Bind shortcuts
        self.bind_shortcuts()
        
        # Initialize crop-related variables
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.crop_rect = None

    def create_toolbar(self):
        """
        Create toolbar with action buttons
        """
        toolbar = ttk.Frame(self.main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save", command=self.save_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Redo", command=self.redo).pack(side=tk.LEFT, padx=5)

    def create_image_display(self):
        """
        Create image display area with two canvases
        """
        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Original image display
        self.original_canvas = tk.Canvas(self.display_frame, bg='gray')
        self.original_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Cropped image display
        self.cropped_canvas = tk.Canvas(self.display_frame, bg='gray')
        self.cropped_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.original_canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.original_canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.original_canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def create_control_panel(self):
        """
        Create control panel with scale slider
        """
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Scale slider
        ttk.Label(control_frame, text="Scale:").pack(side=tk.LEFT, padx=5)
        self.scale_slider = ttk.Scale(control_frame, from_=0.1, to=2.0, 
                                    orient=tk.HORIZONTAL, command=self.on_scale_change)
        self.scale_slider.set(1.0)
        self.scale_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

    def bind_shortcuts(self):
        """
        Bind keyboard shortcuts
        """
        self.root.bind("<Control-s>", lambda e: self.save_image())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())

    def open_image(self):
        """
        Open image file
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.current_image = self.original_image.copy()
            self.update_image_display()
            self.clear_history()

    def save_image(self):
        """
        Save image
        """
        if self.cropped_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Success", "Image saved successfully")

    def on_mouse_down(self, event):
        """
        Handle mouse down event
        """
        self.start_x = self.original_canvas.canvasx(event.x)
        self.start_y = self.original_canvas.canvasy(event.y)
        if self.rect:
            self.original_canvas.delete(self.rect)
        self.rect = self.original_canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2)

    def on_mouse_move(self, event):
        """
        Handle mouse move event
        """
        if self.rect:
            cur_x = self.original_canvas.canvasx(event.x)
            cur_y = self.original_canvas.canvasy(event.y)
            self.original_canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_up(self, event):
        """
        Handle mouse up event
        """
        if self.rect:
            end_x = self.original_canvas.canvasx(event.x)
            end_y = self.original_canvas.canvasy(event.y)
            
            # Get crop area
            x1, y1 = min(self.start_x, end_x), min(self.start_y, end_y)
            x2, y2 = max(self.start_x, end_x), max(self.start_y, end_y)
            
            # Calculate image scale
            scale_x = self.original_image.shape[1] / self.original_canvas.winfo_width()
            scale_y = self.original_image.shape[0] / self.original_canvas.winfo_height()
            
            # Convert coordinates to original image size
            x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
            y1, y2 = int(y1 * scale_y), int(y2 * scale_y)
            
            # Crop image
            self.crop_image(x1, y1, x2, y2)

    def crop_image(self, x1, y1, x2, y2):
        """
        Crop image
        """
        if self.original_image is None:
            return
            
        self.cropped_image = self.original_image[y1:y2, x1:x2].copy()
        self.add_to_history(self.cropped_image)
        self.update_cropped_display()

    def on_scale_change(self, value):
        """
        Handle scale slider change
        """
        self.scale_factor = float(value)
        self.update_cropped_display()

    def update_image_display(self):
        """
        Update original image display
        """
        if self.original_image is None:
            return
            
        # Adjust image size to fit canvas
        canvas_width = self.original_canvas.winfo_width()
        canvas_height = self.original_canvas.winfo_height()
        
        # Calculate scale
        scale = min(canvas_width / self.original_image.shape[1],
                   canvas_height / self.original_image.shape[0])
        
        # Scale image
        width = int(self.original_image.shape[1] * scale)
        height = int(self.original_image.shape[0] * scale)
        
        resized = cv2.resize(self.original_image, (width, height))
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(resized))
        
        # Clear canvas and display new image
        self.original_canvas.delete("all")
        self.original_canvas.create_image(
            canvas_width // 2, canvas_height // 2,
            image=self.photo, anchor=tk.CENTER)

    def update_cropped_display(self):
        """
        Update cropped image display
        """
        if self.cropped_image is None:
            return
            
        # Adjust image size to fit canvas
        canvas_width = self.cropped_canvas.winfo_width()
        canvas_height = self.cropped_canvas.winfo_height()
        
        # Calculate scale
        scale = min(canvas_width / self.cropped_image.shape[1],
                   canvas_height / self.cropped_image.shape[0])
        
        # Apply user-defined scale factor
        scale *= self.scale_factor
        
        # Scale image
        width = int(self.cropped_image.shape[1] * scale)
        height = int(self.cropped_image.shape[0] * scale)
        
        resized = cv2.resize(self.cropped_image, (width, height))
        self.cropped_photo = ImageTk.PhotoImage(image=Image.fromarray(resized))
        
        # Clear canvas and display new image
        self.cropped_canvas.delete("all")
        self.cropped_canvas.create_image(
            canvas_width // 2, canvas_height // 2,
            image=self.cropped_photo, anchor=tk.CENTER)

    def add_to_history(self, image):
        """
        Add image to history
        """
        self.history = self.history[:self.history_index + 1]
        self.history.append(image.copy())
        self.history_index = len(self.history) - 1

    def undo(self):
        """
        Undo operation
        """
        if self.history_index > 0:
            self.history_index -= 1
            self.cropped_image = self.history[self.history_index].copy()
            self.update_cropped_display()

    def redo(self):
        """
        Redo operation
        """
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.cropped_image = self.history[self.history_index].copy()
            self.update_cropped_display()

    def clear_history(self):
        """
        Clear history
        """
        self.history = []
        self.history_index = -1

def main():
    root = tk.Tk()
    app = ImageEditor(root)
    root.geometry("1200x800")
    root.mainloop()

if __name__ == "__main__":
    main() 