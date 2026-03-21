import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import psycopg2
import os

# CONFIGURATION (Matches your Docker setup)
DB_CONFIG = {
    "dbname": "videodb",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}

class VideoManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Docker Video Vault")
        self.root.geometry("500x400")

        # UI Elements
        tk.Label(root, text="PostgreSQL + Docker Video Store", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.upload_btn = tk.Button(root, text="Upload New Video", command=self.upload_video, bg="#4CAF50", fg="white")
        self.upload_btn.pack(pady=5)

        self.refresh_btn = tk.Button(root, text="Refresh List", command=self.load_video_list)
        self.refresh_btn.pack(pady=5)

        # Table to show stored videos
        self.tree = ttk.Treeview(root, columns=("ID", "Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Video Filename")
        self.tree.pack(pady=10, fill="x", padx=20)

        self.load_video_list()

    def get_connection(self):
        return psycopg2.connect(**DB_CONFIG)

    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if not file_path:
            return

        try:
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                video_bytes = f.read()

            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO video_store (video_name, video_data) VALUES (%s, %s)", 
                        (file_name, psycopg2.Binary(video_bytes)))
            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Success", f"Uploaded {file_name} successfully!")
            self.load_video_list()
        except Exception as e:
            messagebox.showerror("Error", f"Upload failed: {e}")

    def load_video_list(self):
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, video_name FROM video_store ORDER BY id DESC")
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error loading list: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoManager(root)
    root.mainloop()