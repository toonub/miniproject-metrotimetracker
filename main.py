from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from datetime import datetime, timedelta

class MetroDisplay:
    def __init__(self, root):
        self.root = root
        self.walk_time = timedelta(minutes=12)
        
        # Load metro timings    
        self.load_metro_timings()
        
        # Load and resize background image to 1920x1080
        self.bg_image = Image.open("Electronic_City.jpg")
        self.bg_image = self.bg_image.resize((1920, 1080), Image.LANCZOS)
        self.width, self.height = 1920, 1080
        
        #customfont
        self.font_xlarge = ImageFont.truetype("OpenSauceOne-Bold.ttf", 95)      # next train
        self.font_large = ImageFont.truetype("OpenSauceOne-Bold.ttf", 55)        # countdown
        self.font_medium = ImageFont.truetype("OpenSauceOne-Bold.ttf", 60)       # current time
        self.font_station = ImageFont.truetype("OpenSauceOne-Bold.ttf", 75)      # station name
        self.font_station_sub = ImageFont.truetype("OpenSauceOne-Bold.ttf", 28)  # metro station
        self.font_status = ImageFont.truetype("OpenSauceOne-Bold.ttf", 38)       # status text
        self.font_upcoming = ImageFont.truetype("OpenSauceOne-Bold.ttf", 30)   # upcoming trains
        self.font_upcoming1 = ImageFont.truetype("OpenSauceOne-Bold.ttf", 25)   # upcoming trains
    
        # Setup window
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)
        
        # Create label to display image
        self.display_label = tk.Label(root)
        self.display_label.pack()
        
        # Start update loop
        self.update_display()
    
    def load_metro_timings(self):
        """Load train timings from CSV file"""
        with open("metro.csv", "r") as f:
            self.timings = [line.strip() for line in f.readlines()]
    
    def get_next_train(self):
        """Find the actual next train and determine if reachable"""
        current_time = datetime.now()
        y = current_time.year
        m = current_time.month
        d = current_time.day
        
        next_train = None
        can_reach = False
        
        for timing in self.timings:
            h, min_str = timing.split(":")
            metro_time = datetime(y, m, d, int(h), int(min_str))
            time_to_train = metro_time - current_time
            
            if time_to_train > timedelta(seconds=0):
                next_train = metro_time
                can_reach = (time_to_train >= self.walk_time)
                break
        
        return next_train, can_reach
    
    def get_upcoming_trains(self, count=4):
        """Get list of next N trains"""
        current_time = datetime.now()
        y = current_time.year
        m = current_time.month
        d = current_time.day
        
        upcoming = []
        for timing in self.timings:
            h, min_str = timing.split(":")
            metro_time = datetime(y, m, d, int(h), int(min_str))
            
            if metro_time > current_time:
                upcoming.append(metro_time)
                if len(upcoming) == count:
                    break
        
        return upcoming
    
    def draw_rounded_rectangle(self, draw, xy, radius, fill):
        """Draw a rounded rectangle"""
        x1, y1, x2, y2 = xy
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
        draw.pieslice([x1, y1, x1 + radius * 2, y1 + radius * 2], 180, 270, fill=fill)
        draw.pieslice([x2 - radius * 2, y1, x2, y1 + radius * 2], 270, 360, fill=fill)
        draw.pieslice([x1, y2 - radius * 2, x1 + radius * 2, y2], 90, 180, fill=fill)
        draw.pieslice([x2 - radius * 2, y2 - radius * 2, x2, y2], 0, 90, fill=fill)
    
    def draw_text_centered(self, draw, text, x, y, font, fill):
        """Draw text centered at position"""
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text((x - text_width // 2, y - text_height // 2), text, font=font, fill=fill)
    
    def update_display(self):
        """Update the display with current information"""
        # Create a fresh copy of the background
        img = self.bg_image.copy()
        draw = ImageDraw.Draw(img)
        
        current_time = datetime.now()
        next_train, can_reach = self.get_next_train()
        
        # 1. Draw current time (top left - rounded yellow pill)
        time_text = current_time.strftime("%H:%M:%S").lstrip("0")
        ## self.draw_rounded_rectangle(draw, (30, 60, 350, 140), 40, "#FFD700")
        self.draw_text_centered(draw, time_text, 170, 95, self.font_medium, "black")
        
        # 3. Draw next train time (center-top)
        if next_train:
            next_train_text = f"             {next_train.strftime("%H:%M")}"
            self.draw_text_centered(draw, next_train_text, 1000, 337, self.font_xlarge, "#FFFFFF")
            
            # 4. Draw countdown box (green or red)
            time_left = next_train - current_time
            total_seconds = int(time_left.total_seconds())
            mins = total_seconds // 60
            secs = total_seconds % 60
            
            if can_reach:
                # Green box with full countdown
                box_color = "#00D98E"
                countdown_text = f"{mins:02d} mins {secs:02d} seconds left"
                self.draw_rounded_rectangle(draw, (490, 480, 1430, 726), 30, box_color)
                self.draw_text_centered(draw, countdown_text, 960, 588, self.font_large, "white")
            else:
                # Red box with only "hurry up"
                box_color = "#FF3B3B"
                countdown_text = f"{mins:02d} mins {secs:02d} seconds left"
                self.draw_rounded_rectangle(draw, (490, 480, 1430, 726), 30, box_color)
                self.draw_text_centered(draw, countdown_text, 960, 588, self.font_large, "white")
        else:
            # No more trains
            self.draw_text_centered(draw, "No more trains today", 960, 330, self.font_xlarge, "#FFD700")
        
        # 5. Draw upcoming trains bar (bottom)
        ##draw.rectangle([440, 920, 1480, 990], fill="#FFD700")
        draw.text((425, 920), "Upcoming Trains", font=self.font_upcoming1, fill="black")
        
        upcoming = self.get_upcoming_trains(4)
        x_positions = [738, 957, 1173 , 1391]
        for i, x in enumerate(x_positions):
            if i < len(upcoming):
                time_str = upcoming[i].strftime("%H:%M")
            else:
                time_str = "--:--"
            self.draw_text_centered(draw, time_str, x, 928, self.font_upcoming, "black")
        
        # Convert to PhotoImage and display
        photo = ImageTk.PhotoImage(img)
        self.display_label.config(image=photo)
        self.display_label.image = photo  # Keep reference
        
        # Schedule next update in 1 second
        self.root.after(1000, self.update_display)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Electronic City Metro Station")
    app = MetroDisplay(root)
    root.mainloop()