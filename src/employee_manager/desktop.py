"""Small Tkinter desktop client for the local Employee Manager API."""
import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
import requests

API_URL = os.getenv("EMPLOYEE_API_URL", "http://127.0.0.1:8000")


class EmployeeDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("InNovaIdeia | Employee Manager")
        self.geometry("850x560")
        self.minsize(720, 460)
        self.entries = {}
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = ttk.Frame(self, padding=18)
        root.pack(fill="both", expand=True)
        ttk.Label(root, text="Employee Manager", font=("Segoe UI", 20, "bold")).pack(anchor="w")
        ttk.Label(root, text="Gestão de funcionários via API FastAPI", foreground="#64748b").pack(anchor="w", pady=(0, 14))
        form = ttk.LabelFrame(root, text="Novo funcionário", padding=12)
        form.pack(fill="x")
        fields = [("nome", "Nome"), ("sobrenome", "Sobrenome"), ("cargo", "Cargo"), ("salario", "Salário"), ("data_contratacao", "Contratação (AAAA-MM-DD)")]
        for index, (key, label) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=index, sticky="w", padx=4)
            entry = ttk.Entry(form, width=19)
            entry.grid(row=1, column=index, sticky="ew", padx=4, pady=5)
            self.entries[key] = entry
        ttk.Button(form, text="Cadastrar", command=self.create).grid(row=1, column=len(fields), padx=8)
        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, pady=16)
        columns = ("id", "nome", "sobrenome", "cargo", "salario", "data_contratacao")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")
        labels = ("ID", "Nome", "Sobrenome", "Cargo", "Salário", "Contratação")
        for col, label in zip(columns, labels):
            self.table.heading(col, text=label)
            self.table.column(col, width=110, anchor="w")
        self.table.pack(fill="both", expand=True)
        footer = ttk.Frame(root)
        footer.pack(fill="x")
        ttk.Button(footer, text="Atualizar lista", command=self.refresh).pack(side="left")
        ttk.Button(footer, text="Excluir selecionado", command=self.delete_selected).pack(side="left", padx=8)
        self.status = ttk.Label(footer, text=f"API: {API_URL}")
        self.status.pack(side="right")

    def create(self):
        try:
            data = {key: entry.get().strip() for key, entry in self.entries.items()}
            data["salario"] = float(data["salario"])
            date.fromisoformat(data["data_contratacao"])
            response = requests.post(f"{API_URL}/employees", json=data, timeout=8)
            response.raise_for_status()
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.refresh()
            self.status.config(text="Funcionário cadastrado.")
        except (ValueError, requests.RequestException) as exc:
            messagebox.showerror("Não foi possível cadastrar", str(exc))

    def refresh(self):
        try:
            response = requests.get(f"{API_URL}/employees", timeout=8)
            response.raise_for_status()
            self.table.delete(*self.table.get_children())
            for item in response.json():
                self.table.insert("", tk.END, values=(item["id"], item["nome"], item["sobrenome"], item["cargo"], f"R$ {item['salario']:.2f}", item["data_contratacao"]))
            self.status.config(text=f"{len(response.json())} registro(s)")
        except requests.RequestException as exc:
            self.status.config(text="API indisponível")
            if self.table.get_children():
                return
            messagebox.showwarning("API indisponível", f"Inicie a API primeiro.\n{exc}")

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Seleção", "Selecione um funcionário.")
            return
        employee_id = self.table.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirmar", f"Excluir o funcionário #{employee_id}?"):
            return
        try:
            response = requests.delete(f"{API_URL}/employees/{employee_id}", timeout=8)
            response.raise_for_status()
            self.refresh()
        except requests.RequestException as exc:
            messagebox.showerror("Erro", str(exc))


if __name__ == "__main__":
    EmployeeDesktop().mainloop()
