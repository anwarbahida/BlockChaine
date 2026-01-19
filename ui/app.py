import customtkinter as ctk
from tkinter import messagebox
from blockchain.blockchain import Blockchain


class BlockchainApp:
    def __init__(self):
        self.blockchain = Blockchain()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.colors = {
            'primary': '#1F6AA1',
            'primary_dark': '#164D75',
            'accent': '#2196F3',
            'success': '#4CAF50',
            'danger': '#E53935',
            'bg_light': '#F8F9FA',
            'bg_card': '#FFFFFF',
            'border': '#E0E0E0',
            'text_dark': '#212121',
            'text_light': '#757575'
        }

        self.window = ctk.CTk()
        self.window.title("Blockchain Manager Pro")
        self.window.geometry("1100x750")
        self.window.configure(fg_color=self.colors['bg_light'])

        self.setup_ui()

    def setup_ui(self):
        # HEADER
        header = ctk.CTkFrame(self.window, fg_color=self.colors['primary'], height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⛓️ BLOCKCHAIN MANAGER",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # MAIN
        main = ctk.CTkFrame(self.window, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=25, pady=20)

        # LEFT PANEL
        left = ctk.CTkFrame(main, fg_color=self.colors['bg_card'], corner_radius=15)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.configure(width=380)
        left.pack_propagate(False)

        self._input(left, " Expéditeur", "sender")
        self._input(left, " Destinataire", "receiver")
        self._input(left, " Montant", "amount")

        ctk.CTkButton(
            left,
            text="Ajouter Transaction",
            height=45,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_dark'],
            command=self.add_transaction
        ).pack(fill="x", padx=20, pady=(20, 8))

        ctk.CTkButton(
            left,
            text="✓ Vérifier Blockchain",
            height=40,
            fg_color=self.colors['success'],
            command=self.verify_blockchain
        ).pack(fill="x", padx=20)

        self.stats = ctk.CTkLabel(
            left,
            text=f"Nombre de blocs : {len(self.blockchain.chain)}",
            font=ctk.CTkFont(size=12)
        )
        self.stats.pack(pady=20)

        # RIGHT PANEL
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        header_chain = ctk.CTkFrame(right, fg_color=self.colors['bg_card'], height=50)
        header_chain.pack(fill="x")
        header_chain.pack_propagate(False)

        ctk.CTkLabel(
            header_chain,
            text="🔗 Chaîne de blocs",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['primary']
        ).pack(side="left", padx=20)

        self.chain_status = ctk.CTkLabel(
            header_chain,
            text="● Actif",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors['success']
        )
        self.chain_status.pack(side="right", padx=20)

        self.scroll = ctk.CTkScrollableFrame(right)
        self.scroll.pack(fill="both", expand=True, pady=15)

        self.update_display()


    def _input(self, parent, label, attr):
        ctk.CTkLabel(parent, text=label, anchor="w").pack(fill="x", padx=20, pady=(15, 5))
        entry = ctk.CTkEntry(parent, height=40)
        entry.pack(fill="x", padx=20)
        setattr(self, attr, entry)

    def add_transaction(self):
        s, r, a = self.sender.get().strip(), self.receiver.get().strip(), self.amount.get().strip()

        if not s or not r or not a:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return

        try:
            a = float(a)
            if a <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erreur", "Montant invalide")
            return

        self.blockchain.add_block(f"{s} → {r} : {a}")
        self.sender.delete(0, "end")
        self.receiver.delete(0, "end")
        self.amount.delete(0, "end")

        self.update_display()

    def verify_blockchain(self):
        valid = self.blockchain.is_chain_valid()
        if valid:
            self.chain_status.configure(text="● Valide", text_color=self.colors['success'])
            messagebox.showinfo("Blockchain", "Blockchain valide")
        else:
            self.chain_status.configure(text="● Invalide", text_color=self.colors['danger'])
            messagebox.showerror("Blockchain", "Blockchain corrompue")

    def update_display(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        for i, block in enumerate(self.blockchain.chain):
            frame = ctk.CTkFrame(self.scroll, fg_color="white", corner_radius=12)
            frame.pack(fill="x", pady=8, padx=8)

            ctk.CTkLabel(
                frame,
                text=f"Bloc #{block.index}",
                font=ctk.CTkFont(size=15, weight="bold")
            ).pack(anchor="w", padx=10, pady=(8, 2))

            for label, val in [
                ("Transaction", block.transactions),
                ("Date", block.timestamp),
                ("Hash", block.hash),
                ("Previous Hash", block.previous_hash)
            ]:
                ctk.CTkLabel(
                    frame,
                    text=f"{label} : {val}",
                    wraplength=650,
                    font=ctk.CTkFont(size=11)
                ).pack(anchor="w", padx=10, pady=2)

        self.stats.configure(text=f"Nombre de blocs : {len(self.blockchain.chain)}")

    def run(self):
        self.window.mainloop()
