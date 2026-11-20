import csv
import tkinter as tk
from collections import defaultdict
from tkinter import filedialog, messagebox, ttk


class TheftChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Electricity Usage Checker")
        self.geometry("760x480")
        self.results = []
        ttk.Label(self, text="Electricity Usage Risk Checker", font=("Arial", 18, "bold")).pack(pady=12)
        ttk.Label(self, text="Import a CSV with consumer_id and consumption_kwh columns.").pack()
        bar = ttk.Frame(self); bar.pack(pady=10)
        ttk.Button(bar, text="Open CSV", command=self.open_csv).pack(side="left", padx=5)
        ttk.Button(bar, text="Export Results", command=self.export).pack(side="left", padx=5)
        self.table = ttk.Treeview(self, columns=("id", "score", "risk", "reason"), show="headings")
        for col, title, width in [("id", "Consumer", 130), ("score", "Score / 100", 100), ("risk", "Risk", 100), ("reason", "Reason", 380)]:
            self.table.heading(col, text=title); self.table.column(col, width=width)
        self.table.pack(fill="both", expand=True, padx=12, pady=10)
        ttk.Label(self, text="A high score is a reason to inspect, not proof of theft.", foreground="#a34a29").pack(pady=5)

    def open_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            groups = defaultdict(list)
            with open(path, newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                if not {"consumer_id", "consumption_kwh"}.issubset(reader.fieldnames or []):
                    raise ValueError("CSV needs consumer_id and consumption_kwh columns.")
                for row in reader:
                    value = float(row["consumption_kwh"])
                    if value < 0: continue
                    groups[row["consumer_id"].strip()].append(value)
            if not groups: raise ValueError("No valid readings found.")
            self.results = []
            for consumer, values in groups.items():
                half = max(1, len(values) // 2)
                earlier, recent = sum(values[:half]) / half, sum(values[-half:]) / half
                drop = max(0, (earlier - recent) / earlier) if earlier else 0
                score = round(min(100, drop * 125))
                risk = "High" if score >= 70 else "Medium" if score >= 35 else "Low"
                reason = f"Recent usage fell {drop:.0%}" if drop else "No sharp usage drop found"
                self.results.append((consumer, score, risk, reason))
            self.results.sort(key=lambda r: r[1], reverse=True)
            self.table.delete(*self.table.get_children())
            for result in self.results: self.table.insert("", "end", values=result)
        except (OSError, ValueError, TypeError, KeyError) as error:
            messagebox.showerror("Import error", str(error))

    def export(self):
        if not self.results:
            messagebox.showinfo("No results", "Open a CSV file first."); return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["consumer_id", "score", "risk", "reason"])
                writer.writerows(self.results)
            messagebox.showinfo("Exported", "Results saved successfully.")


if __name__ == "__main__":
    TheftChecker().mainloop()


