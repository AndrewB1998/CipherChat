from tkinter import *
from tkinter import simpledialog
import socket
import threading
import subprocess

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT = 1234

# Pitää asettaa alku UI erilliseks tost initist, eli aluks valitsee nimen, sit host tai join ja sit vasta käynnisttää servu

# Create the Tk instance
root = Tk()
root.title("Chatter")

class StartUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x500")
        self.selectUI(self.root)
        
    def selectUI(self, root):
        def raise_frame_join():
            btn_forget = [self.join_btn, self.host_btn, self.name_label, self.name_entry, self.save_name]
            for btn in btn_forget:
                btn.grid_forget()
            self.client = Client(HOST, PORT, root, self.name)
        
        def raise_frame_host(frame):
            pass   
        
        def set_name():
            self.name = self.name_entry.get()
            self.join_btn.configure(text="Join chat as "+ self.name), self.host_btn.configure(text="Host a chat as "+ self.name)
            self.join_btn.configure(state=NORMAL), self.host_btn.configure(state=NORMAL)
            
        # Row and column configuration
        Grid.rowconfigure(self.master, 3, weight=1)

        for col in range(5):
            Grid.columnconfigure(self.master, col, weight=1)
                
        self.join_btn = Button(self.root, text= "Join a chatroom", command=lambda: raise_frame_join(self.root), state=DISABLED)               
        self.host_btn = Button(self.root, text='Host a chatroom', command=lambda: raise_frame_host(self.root), state=DISABLED)
        self.name_label = Label(self.root, text="Username")
        self.name_entry = Entry(self.root)
        
        self.host_btn.grid(row=2, column=0, padx=5, pady=5, sticky="NSEW")
        self.join_btn.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        self.name_label.grid(row=3, column=0, padx=5, pady=5, sticky="NSEW")
        self.name_entry.grid(row=4, column=0, padx=5, pady=5, sticky="NSEW")
        
        self.save_name = Button(self.root, text="Save", command= set_name)
        self.save_name.grid(row=5, column=0, padx=5, pady=5, sticky="NSEW")

class Client:
    def __init__(self, host, port, root, name):
        self.root = root
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        self.name = name
        ui_thread = threading.Thread(target=self.mainUI)
        receive_thread = threading.Thread(target=self.receive)
        
        self.ui_done = False
        self.running = True
        ui_thread.start()
        receive_thread.start()
    
    def mainUI(self):
        # Row and column configuration
        Grid.columnconfigure(self.root, 1, weight=1)
        Grid.rowconfigure(self.root, 1, weight=1)
        
        # Messages
        self.messages = []
        self.users = []   
        
        # Scrollbar
        self.y_bar = Scrollbar(self.root, orient=VERTICAL)
        
        # Listbox to display chat
        self.msg_list = Listbox(self.root, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.msg_list.grid(row=1, columns=5, padx=5, pady=5, sticky="NSEW")
        self.y_bar.grid(row=1, column=5, sticky="ns")
        self.msg_list.grid_columnconfigure(0, weight=1)
        self.msg_list.grid_rowconfigure(0, weight=1)

        # Users list
        self.user_list = Listbox(self.root, width=15, height=15, yscrollcommand=self.y_bar.set)
        self.user_list.grid(row=1, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Chat label, box and send button
        self.chat_label = Label(self.root, text="Type your message")
        self.chat_label.grid(row=4, columns=3, sticky="nsew")
        self.chat_box = Text(self.root, height=3)
        self.chat_box.grid(row=5, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.send_button = Button(self.root, text="Send", width="20", command=self.send)
        self.send_button.grid(row=5, column=4, padx=5, pady=5, sticky="NSEW")
        
        # Bind F1 to send
        self.root.bind("<Return>", self.send)
        
        #Close window and loop
        self.ui_done = True
    
    
    
        
    def send(self, event=None):
        message = f"{self.name}: {self.chat_box.get('1.0', 'end')}"
        self.messages.append(message)
        self.sock.send(message.encode('utf-8'))
        self.chat_box.delete('1.0', 'end')
        
    def close(self):
        self.running = False
        self.self.root.self.destroy()
        self.sock.close()
        exit(0)
            
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NAME":
                    self.sock.send(self.name.encode('utf-8'))
                    
                elif self.ui_done:
                    self.msg_list.insert(END, message)
                    
            except ConnectionAbortedError:
                break
            
            except:
                print("Error")
                self.sock.close()
                break

start = StartUI(root)
root.mainloop()