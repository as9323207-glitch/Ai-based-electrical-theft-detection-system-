Python desktop application for reviewing smart-meter consumption patterns and prioritising field inspections. It uses Tkinter for the interface and SQLite for local account, score, and inspection storage.

## Run on Windows

1. Install Python 3.9 or newer and ensure the Tcl/Tk option is included.
2. Open PowerShell in this folder.
3. Install dependencies: `
4. Start the app: 
5. Create an account on the sign-in screen. Passwords are stored as salted PBKDF2 hashes.
6. Choose **Load demo data** to explore the app, or import a CSV.

The application creates `gridguard.db` in this folder at first launch. It runs offline. Keep the database file private because it can contain consumer identifiers and inspection notes.

## CSV format

Required columns:

| Column | Meaning |
| `consumer_id` | Stable consumer identifier |
| `date` | Reading date accepted by pandas, such as `2026-01-31` |
| `consumption_kwh` | Non-negative numeric energy reading in kWh |

Optional `label` column: `0` means normal and `1` means confirmed theft. Random Forest evaluation and scoring are used only when there are at least eight labelled consumers and both classes are present. Without suitable labels, Isolation Forest provides anomaly scores.

## How scoring works\
he importer removes unreadable/missing rows, negative readings, and duplicate consumer/date records, and reports those counts. Per-consumer features include mean, spread, coefficient of variation, trend, recent change, zero-reading rate, and observation count. The model screen can use Isolation Forest, Random Forest, or a combined score (60% supervised and 40% unsupervised when labels are usable). Otherwise the combined option falls back to Isolation Forest.

Risk bands are Low below 35, Medium from 35 to below 70, and High at 70 or above. Explanations are simple feature-based indicators. These scores are screening leads only; they do not establish theft. Legitimate changes in occupancy or equipment can also look anomalous. Verify cases in the field before taking action.

## Project files

- `main.py` - GUI, cleaning and feature pipeline, model scoring, and local storage.
- `sample_data.csv` - small illustrative dataset with both label classes.
- `requirements.txt` - Python package dependencies.
 created locally at runtime; do not commit real consumer data.


