import customtkinter
import threading
import socket


def client_connection(data_to_send,output_textbox):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.connect(('10.0.0.222', 12345))
    client_socket.connect(('127.0.0.1', 12345))
    payload = data_to_send

    

    try:
        while True:
            client_socket.send(payload.encode())
            data = client_socket.recv(1024)
            # print(data.decode())
            output_textbox.configure(state="normal")
            output_textbox.insert("end", data.decode() + "\n")
            output_textbox.configure(state="disabled")
            break
    except KeyboardInterrupt:
        output_textbox.configure(state="normal")
        output_textbox.insert("end", "Exited by the user\n")
        output_textbox.configure(state="disabled")


        # print("Exited by user")
    client_socket.close()

def server_connection(output_textbox):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(5)
    
    receiving = {"help": "show me help",
                 "dir": "show me dir",
                 "ls": "show me ls",
                 "cd": "show me cd"}
    
    correct_query = False

    while True:
        # print("Server is listening...")
        output_textbox.configure(state="normal")
        output_textbox.insert("end", "Server is listening...\n")
        output_textbox.configure(state="disabled")
        client_socket, addr = server_socket.accept()
        # print("Client connected from", addr)
        output_textbox.configure(state="normal")
        output_textbox.insert("end", "Client connected from " + str(addr) + "\n")
        output_textbox.configure(state="disabled")
        while True:
            data=client_socket.recv(1024)
            if not data or data.decode('utf-8') == 'END':
                break
            # print("Received from client: %s" % data.decode('utf-8'))
            output_textbox.configure(state="normal")
            output_textbox.insert("end", "Received from client: " + str(data.decode('utf-8')) + "\n")
            output_textbox.configure(state="disabled")


            for key in receiving.keys():
                if key in data.decode('utf-8'):
                    client_socket.send(bytes(receiving[key], 'utf-8'))
                    correct_query = True
                    break
            print("wrong query")
            if not correct_query:
                client_socket.send(bytes("Wrong query", 'utf-8'))
            correct_query = False
            # if data.decode('utf-8').strip() == "help":
                
            #     client_socket.send(bytes('Hello from server', 'utf-8'))

            break
            # try:
            #     client_socket.send(bytes('Hello from server', 'utf-8'))
            # except:
        output_textbox.configure(state="normal")
        output_textbox.insert("end", "Exited by the user\n")
        output_textbox.configure(state="disabled")
        # print("Exited by the user")
        client_socket.close()

class frontend(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Server - Client")
        self.geometry("1200x400")
        self.minsize(920,600)
        

        self.client_FE()
        self.server_FE()

        self.run_server()

    def client_FE(self):
        label = customtkinter.CTkLabel(self, text="Client", font=("Arial", 20))
        label.pack()
        label.place(x=100, y=50)


        self.text_box_receive = customtkinter.CTkTextbox(self, width=400, height=300)
        self.text_box_receive.pack()
        self.text_box_receive.place(x=100, y=100)
        self.text_box_receive.configure(state="disabled")

        self.text_box_send = customtkinter.CTkTextbox(self, width=400, height=50)
        self.text_box_send.pack()
        self.text_box_send.place(x=100, y=450)


        button = customtkinter.CTkButton(self, text="Send", command=self.run_client)
        button.pack()
        button.place(x=100, y=500)

    def server_FE(self):
        label = customtkinter.CTkLabel(self, text="Server", font=("Arial", 20))
        label.pack()
        label.place(x=700, y=50)

        self.text_box_output = customtkinter.CTkTextbox(self, width=400, height=300)
        self.text_box_output.pack()
        self.text_box_output.place(x=700, y=100)
        self.text_box_output.configure(state="disabled")

    def run_server(self):
        t1 = threading.Thread(target=server_connection, args=(self.text_box_output,))
        t1.start()

    def run_client(self):
        data = self.text_box_send.get("1.0", "end")
        if len(data) > 1:
            t2 = threading.Thread(target=client_connection, args=(data,self.text_box_receive,))
            t2.start()
        else:
            print("No data to send")

    

if __name__ == "__main__":
    frontend().mainloop()