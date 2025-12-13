# groq_chat_gui.py
import os
import requests
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from dotenv import load_dotenv
import threading
from datetime import datetime

# Load .env file
load_dotenv()

class GroqChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Groq AI Chatbot")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize API
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            messagebox.showerror("Error", "GROQ_API_KEY not found in .env file!")
            self.root.destroy()
            return
        
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Available models
        self.GROQ_MODELS = [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "llama-3.2-3b-preview",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ]
        
        self.working_models = []
        self.selected_model = None
        
        # Chat history
        self.messages = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        
        # Setup UI
        self.setup_ui()
        
        # Test models in background
        self.test_models()
    
    def setup_ui(self):
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        accent_color = '#007acc'
        msg_user_bg = '#2b5278'
        msg_bot_bg = '#2d2d2d'
        
        self.root.configure(bg=bg_color)
        
        # Title frame
        title_frame = tk.Frame(self.root, bg=bg_color)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(title_frame, text="🤖 Groq AI Chatbot", 
                font=('Arial', 24, 'bold'), bg=bg_color, fg=fg_color).pack(side='left')
        
        # Model selector
        model_frame = tk.Frame(self.root, bg=bg_color)
        model_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(model_frame, text="Model:", bg=bg_color, fg=fg_color, 
                font=('Arial', 10)).pack(side='left')
        
        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                         state='readonly', width=30)
        self.model_dropdown.pack(side='left', padx=10)
        self.model_dropdown.bind('<<ComboboxSelected>>', self.on_model_change)
        
        # Status label
        self.status_label = tk.Label(model_frame, text="Testing models...", 
                                    bg=bg_color, fg='#888888', font=('Arial', 9))
        self.status_label.pack(side='left', padx=20)
        
        # Chat display area
        chat_frame = tk.Frame(self.root, bg=bg_color)
        chat_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Chat text widget with scrollbar
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, width=80, height=25,
            bg='#2d2d2d', fg=fg_color, font=('Arial', 11),
            relief='flat', borderwidth=0
        )
        self.chat_display.pack(fill='both', expand=True)
        self.chat_display.configure(state='disabled')
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=bg_color)
        input_frame.pack(fill='x', padx=20, pady=10)
        
        # Input field
        self.input_text = tk.Text(input_frame, height=3, width=60,
                                 bg='#3c3c3c', fg=fg_color, font=('Arial', 11),
                                 relief='flat', borderwidth=5)
        self.input_text.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.input_text.bind('<Return>', self.on_enter_pressed)
        self.input_text.bind('<Shift-Return>', lambda e: 'break')  # Shift+Enter for new line
        
        # Send button
        send_button = tk.Button(input_frame, text="Send", command=self.send_message,
                               bg=accent_color, fg=fg_color, font=('Arial', 11, 'bold'),
                               relief='flat', padx=20, pady=5, cursor='hand2')
        send_button.pack(side='right')
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg=bg_color)
        control_frame.pack(fill='x', padx=20, pady=5)
        
        # Clear button
        clear_btn = tk.Button(control_frame, text="🗑️ Clear Chat", command=self.clear_chat,
                             bg='#d32f2f', fg=fg_color, font=('Arial', 9),
                             relief='flat', padx=15, pady=3, cursor='hand2')
        clear_btn.pack(side='left', padx=5)
        
        # Copy button
        copy_btn = tk.Button(control_frame, text="📋 Copy Chat", command=self.copy_chat,
                            bg='#388e3c', fg=fg_color, font=('Arial', 9),
                            relief='flat', padx=15, pady=3, cursor='hand2')
        copy_btn.pack(side='left', padx=5)
        
        # Save button
        save_btn = tk.Button(control_frame, text="💾 Save Chat", command=self.save_chat,
                            bg='#f57c00', fg=fg_color, font=('Arial', 9),
                            relief='flat', padx=15, pady=3, cursor='hand2')
        save_btn.pack(side='left', padx=5)
        
        # Set focus to input
        self.input_text.focus()
        
        # Add welcome message
        self.add_message("system", "Welcome! Select a model and start chatting.")
    
    def test_models(self):
        """Test which Groq models are available"""
        def test_in_thread():
            self.working_models = []
            for model in self.GROQ_MODELS:
                try:
                    test_data = {
                        "model": model,
                        "messages": [{"role": "user", "content": "Say 'ready'"}],
                        "max_tokens": 5,
                        "temperature": 0.1
                    }
                    
                    response = requests.post(self.url, headers=self.headers, 
                                           json=test_data, timeout=10)
                    
                    if response.status_code == 200:
                        self.working_models.append(model)
                        self.status_label.config(text=f"✓ {model}")
                    else:
                        self.status_label.config(text=f"✗ {model}")
                        
                except Exception as e:
                    self.status_label.config(text=f"✗ {model}")
            
            # Update dropdown
            self.root.after(0, self.update_model_dropdown)
        
        # Start testing in background thread
        threading.Thread(target=test_in_thread, daemon=True).start()
    
    def update_model_dropdown(self):
        """Update model dropdown with available models"""
        if self.working_models:
            self.model_dropdown['values'] = self.working_models
            self.model_dropdown.set(self.working_models[0])
            self.selected_model = self.working_models[0]
            self.status_label.config(text=f"✅ {len(self.working_models)} models available")
            self.add_message("system", f"Ready! {len(self.working_models)} models available.")
        else:
            self.status_label.config(text="❌ No models available")
            messagebox.showerror("Error", "No Groq models available. Check API key.")
    
    def on_model_change(self, event):
        """Handle model selection change"""
        self.selected_model = self.model_var.get()
        self.add_message("system", f"Switched to model: {self.selected_model}")
    
    def add_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.configure(state='normal')
        
        # Get current time
        timestamp = datetime.now().strftime("%H:%M")
        
        # Configure tags for different senders
        if sender == "user":
            tag = "user"
            prefix = "👤 You"
            bg_color = "#2b5278"
        elif sender == "bot":
            tag = "bot"
            prefix = "🤖 Assistant"
            bg_color = "#2d2d2d"
        else:
            tag = "system"
            prefix = "⚙️ System"
            bg_color = "#5d4037"
        
        # Add message with styling
        self.chat_display.insert(tk.END, f"[{timestamp}] {prefix}:\n", tag)
        self.chat_display.insert(tk.END, f"{message}\n\n", f"{tag}_content")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')
    
    def on_enter_pressed(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # Not Shift key
            self.send_message()
            return 'break'  # Prevent default behavior
    
    def send_message(self):
        """Send user message to Groq API"""
        if not self.selected_model:
            messagebox.showerror("Error", "Please select a model first!")
            return
        
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return
        
        # Clear input
        self.input_text.delete("1.0", tk.END)
        
        # Add user message to display
        self.add_message("user", user_input)
        
        # Add to messages history
        self.messages.append({"role": "user", "content": user_input})
        
        # Show thinking indicator
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, "🤖 Thinking...\n\n", "thinking")
        self.chat_display.see(tk.END)
        self.chat_display.configure(state='disabled')
        
        # Send to API in background thread
        threading.Thread(target=self.get_ai_response, args=(user_input,), daemon=True).start()
    
    def get_ai_response(self, user_input):
        """Get response from Groq API"""
        try:
            data = {
                "model": self.selected_model,
                "messages": self.messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }
            
            response = requests.post(self.url, headers=self.headers, json=data, timeout=30)
            
            # Remove thinking indicator
            self.root.after(0, self.remove_thinking_indicator)
            
            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                
                # Add to messages history
                self.messages.append({"role": "assistant", "content": reply})
                
                # Keep conversation manageable
                if len(self.messages) > 21:
                    self.messages = [self.messages[0]] + self.messages[-20:]
                
                # Add bot message to display
                self.root.after(0, lambda: self.add_message("bot", reply))
                
            elif response.status_code == 429:
                error_msg = "Rate limited. Please wait..."
                self.root.after(0, lambda: self.add_message("system", error_msg))
                
            else:
                error_msg = f"API Error {response.status_code}"
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg += f": {error_data['error'].get('message', 'Unknown error')}"
                except:
                    pass
                self.root.after(0, lambda: self.add_message("system", error_msg))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.add_message("system", "Request timeout. Please try again."))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("system", f"Error: {str(e)[:100]}"))
    
    def remove_thinking_indicator(self):
        """Remove the 'Thinking...' message"""
        self.chat_display.configure(state='normal')
        # Find and remove the thinking line
        end_pos = self.chat_display.index(tk.END)
        lines = end_pos.split('.')[0]
        
        # Search backwards for thinking indicator
        for i in range(int(lines), 0, -1):
            line_start = f"{i}.0"
            line_end = f"{i}.end"
            line_text = self.chat_display.get(line_start, line_end)
            if "Thinking..." in line_text:
                self.chat_display.delete(line_start, f"{int(line_start.split('.')[0]) + 1}.0")
                break
        
        self.chat_display.configure(state='disabled')
    
    def clear_chat(self):
        """Clear the chat history"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat?"):
            self.messages = [self.messages[0]]  # Keep system message
            self.chat_display.configure(state='normal')
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.configure(state='disabled')
            self.add_message("system", "Chat cleared.")
    
    def copy_chat(self):
        """Copy chat to clipboard"""
        self.root.clipboard_clear()
        chat_text = self.chat_display.get("1.0", tk.END)
        self.root.clipboard_append(chat_text)
        messagebox.showinfo("Copied", "Chat copied to clipboard!")
    
    def save_chat(self):
        """Save chat to file"""
        chat_text = self.chat_display.get("1.0", tk.END)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Groq Chat History - {timestamp}\n")
                f.write(f"Model: {self.selected_model}\n")
                f.write("=" * 50 + "\n\n")
                f.write(chat_text)
            
            messagebox.showinfo("Saved", f"Chat saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

def main():
    root = tk.Tk()
    
    # Configure tags for text widget
    def configure_tags():
        # User messages
        root.chat_display.tag_config("user", foreground="#82b1ff", font=('Arial', 10, 'bold'))
        root.chat_display.tag_config("user_content", foreground="#e1f5fe")
        
        # Bot messages
        root.chat_display.tag_config("bot", foreground="#69f0ae", font=('Arial', 10, 'bold'))
        root.chat_display.tag_config("bot_content", foreground="#e8f5e9")
        
        # System messages
        root.chat_display.tag_config("system", foreground="#ffb74d", font=('Arial', 10, 'bold'))
        root.chat_display.tag_config("system_content", foreground="#fff3e0")
        
        # Thinking indicator
        root.chat_display.tag_config("thinking", foreground="#bb86fc", font=('Arial', 10, 'italic'))
    
    # Create app
    app = GroqChatGUI(root)
    
    # Configure tags after widget is created
    root.after(100, configure_tags)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()