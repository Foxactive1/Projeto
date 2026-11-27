import os
import tkinter.messagebox as messagebox
from datetime import date

import customtkinter as ctk
import requests

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


class EmployeeDesktop(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Employee Manager | InNovaIdeia")
        self.geometry("900x650")
        self.minsize(760, 560)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Employee Manager", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(22, 4))
        ctk.CTkLabel(self, text="Cadastro e consulta de funcionários via API REST").pack(pady=(0, 18))

        form = ctk.CTkFrame(self)
        form.pack(fill="x", padx=24, pady=8)
        self.fields = {}
        labels = [("nome", "Nome"), ("sobrenome", "Sobrenome"), ("cargo", "Cargo"), ("salario", "Salário"), ("data_contratacao", "Contratação (AAAA-MM-DD)")]
        for index, (key, label) in enumerate(labels):
            ctk.CTkLabel(form, text=label).grid(row=index // 2, column=(index % 2) * 2, padx=12, pady=10, sticky="w")
            entry = ctk.CTkEntry(form, width=240, placeholder_text=label)
            entry.grid(row=index // 2, column=(index % 2) * 2 + 1, padx=12, pady=10, sticky="ew")
            self.fields[key] = entry
        ctk.CTkButton(form, text="Cadastrar funcionário", command=self.create_employee).grid(row=3, column=0, columnspan=4, padx=12, pady=12, sticky="ew")
        form.grid_columnconfigure((1, 3), weight=1)

        toolbar = ctk.CTkFrame(self, fg_color="transparent")
        toolbar.pack(fill="x", padx=24, pady=8)
        ctk.CTkButton(toolbar, text="Atualizar lista", command=self.load_employees).pack(side="left")
        self.status = ctk.CTkLabel(toolbar, text="Conectando à API...")
        self.status.pack(side="left", padx=14)
        self.results = ctk.CTkTextbox(self, wrap="none")
        self.results.pack(fill="both", expand=True, padx=24, pady=(4, 24))
        self.load_employees()

    def create_employee(self):
        try:
            payload = {key: field.get().strip() for key, field in self.fields.items()}
            payload["salario"] = float(payload["salario"].replace(",", "."))
            date.fromisoformat(payload["data_contratacao"])
            response = requests.post(f"{API_URL}/employees", json=payload, timeout=8)
            response.raise_for_status()
            for field in self.fields.values():
                field.delete(0, "end")
            self.status.configure(text="Cadastro realizado.")
            self.load_employees()
        except (ValueError, requests.RequestException) as exc:
            messagebox.showerror("Não foi possível cadastrar", str(exc))

    def load_employees(self):
        try:
            response = requests.get(f"{API_URL}/employees", timeout=8)
            response.raise_for_status()
            employees = response.json()
            self.results.delete("1.0", "end")
            self.results.insert("end", f"Funcionários cadastrados: {len(employees)}\\n\\n")
            for item in employees:
                self.results.insert("end", f"#{item['id']} | {item['nome']} {item['sobrenome']} | {item['cargo']} | R$ {item['salario']:.2f} | {item['data_contratacao']}\\n")
            self.status.configure(text="API conectada.")
        except requests.RequestException as exc:
            self.status.configure(text="API indisponível. Inicie o servidor.")
            self.results.delete("1.0", "end")
            self.results.insert("end", f"Não foi possível consultar a API: {exc}\\nComando: uvicorn employee_manager.api:app --reload")


if __name__ == "__main__":
    EmployeeDesktop().mainloop()
