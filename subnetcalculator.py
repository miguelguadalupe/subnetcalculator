import tkinter as tk
from tkinter import messagebox, ttk
import ipaddress

class SubnetCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Subnet Calculator')
        self.geometry('400x300')

        # Define style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure(bg='black')

        # Define colors
        self.style.configure('.', background='black', foreground='white', font=('Helvetica', 10))
        self.style.configure('TButton', background='black', foreground='white', font=('Helvetica', 12))
        self.style.configure('TLabel', background='black', foreground='white', font=('Helvetica', 12))
        self.style.configure('TEntry', fieldbackground='grey', foreground='white', font=('Helvetica', 12))

        self.create_widgets()

    def create_widgets(self):
        # network address entry
        self.net_addr_label = ttk.Label(self, text="Network Address")
        self.net_addr_label.pack(pady=10)
        self.net_addr_entry = ttk.Entry(self)
        self.net_addr_entry.pack(pady=10)

        # calculate button
        self.calculate_button = ttk.Button(self, text='Calculate', command=self.calculate_subnet)
        self.calculate_button.pack(pady=10)

        # display result
        self.result_text = tk.Text(self, bg='grey', fg='white', height=8)
        self.result_text.pack(pady=10)

        # make the text widget readonly and allow copying text
        self.result_text.config(state='disabled')
        self.result_text.bind("<Control-c>", self.copy)

    def calculate_subnet(self):
        network_address = self.net_addr_entry.get()

        try:
            net = ipaddress.ip_network(network_address, strict=False)
        except ValueError:
            messagebox.showerror('Invalid network address', 'Please enter a valid network address')
            return

        # subnet calculations
        net_address = str(net.network_address)
        broadcast_address = str(net.broadcast_address)
        num_addresses = net.num_addresses
        num_usable_addresses = num_addresses - 2 if num_addresses > 2 else num_addresses
        usable_ips = list(net.hosts())

        # get the range of usable IPs if they exist
        if usable_ips:
            first_usable_ip = str(usable_ips[0])
            last_usable_ip = str(usable_ips[-1])
        else:
            first_usable_ip = last_usable_ip = 'None'

        # get the subnet mask
        subnet_mask = str(net.netmask)

        # insert result into text widget
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f'Network Address: {net_address}\n')
        self.result_text.insert(tk.END, f'Subnet Mask: {subnet_mask}\n')
        self.result_text.insert(tk.END, f'Broadcast Address: {broadcast_address}\n')
        self.result_text.insert(tk.END, f'Total Addresses: {num_addresses}\n')
        self.result_text.insert(tk.END, f'Usable Addresses: {num_usable_addresses}\n')
        self.result_text.insert(tk.END, f'First Usable IP: {first_usable_ip}\n')
        self.result_text.insert(tk.END, f'Last Usable IP: {last_usable_ip}\n')
        self.result_text.config(state='disabled')

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.result_text.get("sel.first", "sel.last")
        self.clipboard_append(text)

if __name__ == "__main__":
    app = SubnetCalculator()
    app.mainloop()
