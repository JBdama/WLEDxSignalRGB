import tkinter as tk
from controller import Controller
from serial.tools.list_ports import comports

class Application(tk.Frame):

    coms = [""]
    controller = Controller()

    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.create_widgets()
        self.refresh()

    # Creates the widgets for the GUI
    def create_widgets(self):
        # Create a frame to hold the inputs
        self.inputs_frame = tk.Frame(self)
        self.inputs_frame.grid(row=1, column=1, pady=10)
        
        # Create an entry for the user to input the IP address
        self.ip_entry = tk.Entry(self.inputs_frame)
        self.ip_entry.insert(1, "192.168.178.25")
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)
        self.ip_label = tk.Label(self.inputs_frame, text="IP address:")
        self.ip_label.grid(row=0, column=0, padx=10, pady=10)

        # Create an entry for the user to input the UDP port
        self.port_entry = tk.Entry(self.inputs_frame)
        self.port_entry.insert(1, "21324")
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)
        self.port_label = tk.Label(self.inputs_frame, text="Port:")
        self.port_label.grid(row=1, column=0, padx=10, pady=10)
        self.port_test_button = tk.Button(self.inputs_frame, text="Test UDP", command=self.test_udp)
        self.port_test_button.grid(row=1, column=2, padx=10, pady=10)

        # Create an option menu for the user to select the LED count
        self.led_count_label = tk.Label(self.inputs_frame, text="LED Count:")
        self.led_count_label.grid(row=2, column=0, padx=10, pady=10)
        self.led_count_entry = tk.Entry(self.inputs_frame)
        self.led_count_entry.insert(1, "60")
        self.led_count_entry.grid(row=2, column=1, padx=10, pady=10)

        # Create an option menu for the user to select the com port
        self.coms_label = tk.Label(self.inputs_frame, text="COM Port:")
        self.coms_label.grid(row=3, column=0, padx=10, pady=10)
        self.coms_var = tk.StringVar(value="No Port Selected")
        self.coms_menu = tk.OptionMenu(self.inputs_frame, self.coms_var, *self.coms, command=self.set_coms)
        self.coms_menu.config(width=15, anchor="w")
        self.coms_menu.grid(row=3, column=1, padx=10, pady=10)
        self.refresh_button = tk.Button(self.inputs_frame, text="Refresh", command=self.refresh)
        self.refresh_button.grid(row=3, column=2)

        # Create a button to start/stop the program
        self.button = tk.Button(self, text="Start",height=3,width=10, command=self.toggle_start_stop)
        self.button.grid(row=2, column=1, pady=10)

        self.input_widgets = [self.ip_entry, self.port_entry, self.led_count_entry, self.coms_menu]

    # Toggles the start/stop button
    def toggle_start_stop(self):
        if self.button["text"] == "Start":
            self.init_controller()
            self.button["text"] = "Stop"
        else:
            self.stop()
            self.button["text"] = "Start"

    # Sets the coms variable
    def set_coms(self, coms):
        self.coms = coms

    # Initializes the controller and disables the inputs
    def init_controller(self):
        self.controller.set_serial(self.coms_var.get())
        self.controller.set_transmitter(self.port_entry.get(), self.ip_entry.get())
        self.controller.start()
        for widget in self.input_widgets:
            widget["state"] = "disabled"

    # Stops the controller, toggles the start/stop button, and enables the inputs
    def stop(self):
        self.controller.stop()
        for widget in self.input_widgets:
            widget["state"] = "normal"

    # Tests the UDP connection
    def test_udp(self):
        self.controller.set_transmitter(self.port_entry.get(), self.ip_entry.get())
        self.controller.test_udp()

    # Refreshes the coms menu
    def refresh(self):
            self.coms_menu["menu"].delete(0, "end")
            new_ports = []
            for port in comports():
                new_ports.append(port)
                print(port)
            if (len(new_ports) == 0):
                print("No Port Available")
            for com in new_ports:
                self.coms_menu["menu"].add_command(label=com, command=tk._setit(self.coms_var, com))
                self.coms_var.set(com)
