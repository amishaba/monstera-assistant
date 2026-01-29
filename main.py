import asyncio
import threading
import pyaudio
import os
import io
import wave
import tkinter as tk # Keep standard tk for Canvas
import customtkinter as ctk # Add CustomTkinter for modern UI
from ctypes import windll
import math
import random
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- 1. CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Audio Settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Gemini Config
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp") # Defaults if .env fails
SYSTEM_PROMPT = _default_prompt = "You are a helpful assistant. Please answer simply in English."
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", _default_prompt).replace("\\n", "\n")

# Global State
audio_buffer = []
is_recording = False

# Set appearance mode and default color theme for CustomTkinter
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# --- 2.  MASCOT CLASS: MONSTERA  ---
class MonsteraMascot(tk.Canvas):
    """A High-Definition Animated Monstera."""
    
    def __init__(self, parent, **kwargs):
        # 1. Handle Background safely
        if 'bg' not in kwargs:
            kwargs['bg'] = "#F4F0E6" # Default Cream
        
        self.bg_color = kwargs['bg']

        # 2. Init Canvas
        super().__init__(parent, width=220, height=250, 
                         highlightthickness=0, **kwargs)
        
        # --- PALETTE (Jet Set / First Class) ---
        self.C_LEAF       = "#1E5128"  # Deep Forest Green
        self.C_LEAF_SHADOW= "#143D1F"  # Darker Green for depth
        self.C_POT        = "#D35400"  # International Orange
        self.C_POT_SHADOW = "#A04000"  # Darker Rust
        self.C_STEM       = "#145A32"
        self.C_SHADOW     = "#D0D3D4"  # Floor Shadow
        
        # Animation State
        self.state = 'idle'
        self.time = 0
        
        # Physics
        self.scale_y = 1.0 
        self.is_blinking = False
        
        self.create_plant()
        self.animate()

    def create_plant(self):
        self.cx = 110
        self.cy = 200 
        
        # 1. Floor Shadow (Smoothed)
        self.shadow = self.create_oval(
            70, 238, 150, 248, 
            fill=self.C_SHADOW, outline=""
        )

        # 2. Stem (Curved Line)
        self.stem = self.create_line(self.cx, self.cy, self.cx, self.cy - 60, 
                                     width=6, fill=self.C_STEM, capstyle='round')

        # 3. Leaf Group
        # We use a polygon with smooth=True for a vector-like organic shape
        self.leaf_body = self.create_polygon(
            0,0,0,0, fill=self.C_LEAF, smooth=True, outline=""
        )
        
        # Leaf Detail (Shadow on the left side for depth)
        self.leaf_shadow = self.create_polygon(
            0,0,0,0, fill=self.C_LEAF_SHADOW, smooth=True, outline=""
        )

        # The "Cuts" (Masks) - Using BG color
        self.cut1 = self.create_oval(0,0,0,0, fill=self.bg_color, outline="")
        self.cut2 = self.create_oval(0,0,0,0, fill=self.bg_color, outline="")
        self.cut3 = self.create_oval(0,0,0,0, fill=self.bg_color, outline="")

        # 4. Face (Crisper eyes)
        self.eye_l = self.create_oval(0,0,0,0, fill="white", outline=self.C_STEM, width=1)
        self.pupil_l = self.create_oval(0,0,0,0, fill="black")
        
        self.eye_r = self.create_oval(0,0,0,0, fill="white", outline=self.C_STEM, width=1)
        self.pupil_r = self.create_oval(0,0,0,0, fill="black")
        
        self.mouth = self.create_line(0,0,0,0, fill="black", smooth=True, width=2, capstyle="round")

        # 5. Sprout (Hidden)
        self.sprout_stem = self.create_line(0,0,0,0, width=3, fill="#2ECC71", capstyle='round')
        self.sprout_leaf = self.create_oval(0,0,0,0, fill="#2ECC71", outline="")

        # 6. The Pot (High Def - with Shading)
        # Main Pot
        self.pot = self.create_polygon(
            80, 200, 140, 200, 130, 245, 90, 245,
            fill=self.C_POT, outline="", width=0
        )
        # Pot Shadow (Right side)
        self.pot_shadow = self.create_polygon(
            110, 200, 140, 200, 130, 245, 110, 245,
            fill=self.C_POT_SHADOW, outline=""
        )
        # Pot Rim
        self.pot_rim = self.create_line(78, 200, 142, 200, width=5, fill="#E67E22", capstyle="round")

    def set_state(self, new_state):
        self.state = new_state
        if new_state != 'thinking':
            self.coords(self.sprout_stem, 0,0,0,0)
            self.coords(self.sprout_leaf, 0,0,0,0)

    def generate_leaf_shape(self, x, y, w, h):
        # Generates points for a nice heart-shaped leaf
        return [
            x, y + h*0.3,       # Bottom tip
            x - w, y - h*0.2,   # Left mid
            x - w*0.8, y - h,   # Left top
            x, y - h*0.6,       # Center dip
            x + w*0.8, y - h,   # Right top
            x + w, y - h*0.2    # Right mid
        ]

    def animate(self):
        dt = 0.05
        self.time += dt
        
        # Physics
        sway_speed = 2.0
        sway_amp = 5.0
        target_scale = 1.0
        
        if self.state == 'listening':
            sway_speed = 8.0 
            sway_amp = 2.5
            target_scale = 1.05 
        elif self.state == 'thinking':
            sway_speed = 4.0
            sway_amp = 3.0
        
        # Smooth scale
        self.scale_y += (target_scale - self.scale_y) * 0.1
        
        # Sway
        tip_sway = math.sin(self.time * sway_speed) * sway_amp
        
        # --- DRAWING UPDATE ---
        
        # 1. Stem
        head_x = self.cx + tip_sway
        head_y = self.cy - 100 * self.scale_y
        self.coords(self.stem, self.cx, self.cy, head_x, head_y)
        
        # 2. Leaf Body (Using Spline Polygon for smooth edges)
        lw = 55
        lh = 70 * self.scale_y
        
        # Generate the spline points
        leaf_pts = self.generate_leaf_shape(head_x, head_y, lw, lh)
        self.coords(self.leaf_body, *leaf_pts)
        
        # Leaf Shadow (Left half of the same shape)
        shadow_pts = self.generate_leaf_shape(head_x - 5, head_y, lw * 0.9, lh)
        self.coords(self.leaf_shadow, *shadow_pts) 
        
        # 3. Cuts (The Fenestrations)
        # Cut 1 (Left)
        self.coords(self.cut1, head_x - 35, head_y - 50, head_x - 15, head_y - 30)
        # Cut 2 (Right Top)
        self.coords(self.cut2, head_x + 15, head_y - 65, head_x + 35, head_y - 45)
        # Cut 3 (Right Bottom)
        self.coords(self.cut3, head_x + 20, head_y - 20, head_x + 40, head_y)

        # 4. Face
        face_y = head_y - 25 * self.scale_y
        ex_l = head_x - 15
        ex_r = head_x + 15
        
        # Blink Logic
        if not self.is_blinking and random.random() < 0.01: self.is_blinking = True
        eye_h = 6
        if self.is_blinking:
            eye_h = 1
            if random.random() < 0.1: self.is_blinking = False
            
        self.coords(self.eye_l, ex_l - 6, face_y - eye_h, ex_l + 6, face_y + eye_h)
        self.coords(self.pupil_l, ex_l - 2, face_y - 2, ex_l + 2, face_y + 2)
        
        self.coords(self.eye_r, ex_r - 6, face_y - eye_h, ex_r + 6, face_y + eye_h)
        self.coords(self.pupil_r, ex_r - 2, face_y - 2, ex_r + 2, face_y + 2)
        
        # Mouth
        if self.state == 'listening':
            self.coords(self.mouth, head_x - 5, face_y + 15, head_x + 5, face_y + 15)
        else:
            self.coords(self.mouth, head_x - 8, face_y + 12, head_x, face_y + 16, head_x + 8, face_y + 12)

        # 5. Sprout (Thinking)
        if self.state == 'thinking':
            bob = abs(math.sin(self.time * 8)) * 30
            sx = self.cx + 45
            sy_base = 200
            sy_tip = sy_base - bob
            self.coords(self.sprout_stem, sx, sy_base, sx, sy_tip)
            self.coords(self.sprout_leaf, sx - 10, sy_tip - 10, sx + 10, sy_tip + 5)

        self.after(20, self.animate)


# --- 3. AUDIO LOGIC ---
def create_wav_bytes(pcm_data):
    wav_io = io.BytesIO()
    with wave.open(wav_io, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wav_file.setframerate(RATE)
        wav_file.writeframes(pcm_data)
    wav_io.seek(0)
    return wav_io.read()


async def process_audio_chunk(app_instance, pcm_data):
    client = genai.Client(api_key=API_KEY)
    
    app_instance.update_output("Thinking...")
    app_instance.mascot.set_state('thinking')
    
    # --- SAFETY SETTINGS (GUARDRAILS TO THE MOON) ---
    # We set everything to BLOCK_LOW_AND_ABOVE to catch even minor infractions.
    safety_config = [
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_LOW_AND_ABOVE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_LOW_AND_ABOVE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_LOW_AND_ABOVE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_LOW_AND_ABOVE"
        ),
    ]

    try:
        wav_bytes = create_wav_bytes(pcm_data)
        
        response = await client.aio.models.generate_content(
            model=MODEL,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_bytes(data=wav_bytes, mime_type="audio/wav")]
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_modalities=["TEXT"],
                temperature=0.5, # Lower temp = more predictable/safe answers
                safety_settings=safety_config # Apply the guardrails
            )
        )

        if response.text:
            app_instance.update_output(response.text)
            app_instance.mascot.set_state('idle')
        else:
            # If safety filters blocked the response, response.text might be empty
            app_instance.update_output("Oops! I can't talk about that. Let's talk about nature instead!")
            app_instance.mascot.set_state('idle')

    except Exception as e:
        # Catch errors smoothly for non-tech users
        print(f"Debug Error: {e}") # Keep detailed error in console
        app_instance.update_output("My leaves are a bit confused. Can you say that again?")
        app_instance.mascot.set_state('idle')



def run_audio_loop(app_instance):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    pya = pyaudio.PyAudio()
    stream = pya.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    
    while True:
        if is_recording:
            try:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                audio_buffer.append(data)
            except: pass
        else:
            if len(audio_buffer) > 0:
                complete_pcm = b''.join(audio_buffer)
                audio_buffer.clear()
                loop.run_until_complete(process_audio_chunk(app_instance, complete_pcm))
            threading.Event().wait(0.01)


# --- 4. APP GUI ---
class DesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        try: windll.shcore.SetProcessDpiAwareness(1)
        except: pass
        
        # --- THEME CONFIGURATION ---
        self.THEME = {
            "bg": "#F4F0E6",           # Cream Background
            "glass_frame": "#F4F0E6",  # Same as BG for transparent effect
            "text_fg": "#003366",      # Navy Blue Text
            "btn_idle": "#D35400",     # International Orange
            "btn_hover": "#E67E22",    # Lighter Orange
            "btn_active": "#A04000",   # Darker Orange (Recording)
            "font_main": ("Georgia", 16),
            "font_bold": ("Georgia", 16, "bold")
        }
        
        self.title("minmax monstera - First Class")
        self.geometry("420x750")
        self.configure(fg_color=self.THEME["bg"]) # Set window background
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Mascot
        self.grid_rowconfigure(1, weight=1) # Chat
        self.grid_rowconfigure(2, weight=0) # Button

        # 1. THE MASCOT
        self.mascot = MonsteraMascot(self, bg=self.THEME["bg"])
        self.mascot.grid(row=0, column=0, pady=(40, 20))

        # 2. TEXT AREA (The "Glass" Box)
        self.chat_frame = ctk.CTkFrame(
            self, 
            fg_color=self.THEME["glass_frame"], # Makes it look semi-transparent
            corner_radius=20,                   # The iOS-style rounded corners
            border_width=2,                     # Subtle border definition
            border_color=self.THEME["text_fg"]  # Navy border
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=10)
        
        # Inside the frame, we use a CTkLabel for text
        self.chat_box = ctk.CTkTextbox(
            self.chat_frame,
            font=self.THEME["font_main"],
            text_color=self.THEME["text_fg"],
            fg_color="transparent",  # Make it blend into the frame
            wrap="word",             # Wrap words properly
            activate_scrollbars=False # Hides scrollbar (optional, set True if you prefer)
        )
        self.chat_box.pack(fill="both", expand=True, padx=20, pady=20)

        # Insert startup text
        self.chat_box.insert("0.0", "SYSTEM READY.\nminmax monstera is at your service.")
        
        # Lock it so user can copy but not type
        self.chat_box.configure(state="disabled")

        # 3. BUTTON (Rounded & Modern)
        self.ptt_btn = ctk.CTkButton(
            self, 
            text="HOLD SPACE TO SPEAK", 
            height=60,
            font=self.THEME["font_bold"],
            fg_color=self.THEME["btn_idle"], 
            hover_color=self.THEME["btn_hover"],
            text_color="white",
            corner_radius=30, # Perfectly rounded ends
            cursor="hand2"
        )
        self.ptt_btn.grid(row=2, column=0, sticky="ew", pady=(20, 40), padx=30)

        # Bindings
        self.ptt_btn.bind("<ButtonPress-1>", self.start_talking)
        self.ptt_btn.bind("<ButtonRelease-1>", self.stop_talking)
        self.bind("<KeyPress-space>", self.start_talking)
        self.bind("<KeyRelease-space>", self.stop_talking)

    def start_talking(self, event=None):
        global is_recording
        if not is_recording:
            is_recording = True
            # Visual Feedback
            self.ptt_btn.configure(fg_color=self.THEME["btn_active"], text="LISTENING...")
            self.mascot.set_state('listening')

    def stop_talking(self, event=None):
        global is_recording
        if is_recording:
            is_recording = False
            # Visual Feedback
            self.ptt_btn.configure(fg_color=self.THEME["btn_idle"], text="HOLD SPACE TO SPEAK")

    def update_output(self, text):
        def _update():
            self.chat_box.configure(state="normal")   # Unlock to write
            self.chat_box.delete("0.0", "end")        # Clear old text
            self.chat_box.insert("0.0", text)         # Insert new text
            self.chat_box.configure(state="disabled") # Lock to read-only
        
        self.after(0, _update)

if __name__ == "__main__":
    app = DesktopApp()
    t = threading.Thread(target=run_audio_loop, args=(app,), daemon=True)
    t.start()
    app.mainloop()