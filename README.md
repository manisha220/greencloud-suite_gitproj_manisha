# GreenCloud Suite

An interactive Streamlit demonstration for Green Information Technology (GIT), Unit IV — Green Cloud Computing.

**Author:** Manisha Chaubey  
**USN:** 1NT23IS116  
**Institution:** Nitte Meenakshi Institute of Technology (NMIT), Bangalore

## What the application demonstrates

- **Overview Dashboard:** simulated server, VM, power, network, CPU, thermal and estimated savings summary.
- **GreenCloud Monitor:** power and energy calculations, trends, monitoring controls and threshold alerts.
- **GreenVM Optimizer:** greedy VM placement across five simulated physical hosts, with CPU and memory capacity checks and before/after estimates.
- **ThermalAware Scheduler:** illustrative workload-to-temperature relationship and capacity-aware balancing.
- **SNMP Traffic Analyzer:** simulated interface counters, traffic rate calculations, top talkers and utilization alerts.
- **About & Unit IV Concepts:** assignment details, concept links and simulation disclaimer.

The interface uses a dark green theme, including readable sidebar navigation, dark content panels and dark chart canvases. The Streamlit theme is configured in `.streamlit/config.toml`.

All measurements and savings are simulated. The app does not connect to SNMP agents, migrate real VMs, or control physical servers. Its example power, temperature and traffic values are educational estimates, not experimental results.

## Run locally

Requires Python 3.9 or later.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and start the app:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints a local URL (typically `http://localhost:8501`). Use the sidebar to switch modules. The reset button returns VM assignments and simulated optimization state to defaults.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository for the project.
2. Add `app.py`, `requirements.txt`, and `README.md` to the repository and push the files to GitHub.
3. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and choose **Create app**.
4. Select the repository, branch, and `app.py` as the main file.
5. Deploy. No secrets, environment variables, API keys, or external data files are required.

The app uses only the listed Python dependencies and is designed to run with `streamlit run app.py`.

## Assumptions

- Five sample hosts each provide 24 CPU cores and 64 GB of memory; ten sample VMs carry consistent CPU, memory and network demand across modules.
- Example host power is modeled as 90 W idle plus 1.5 W per allocated CPU core.
- Example temperature is modeled as 23 °C + 0.27 × CPU utilization (%) + 0.004 × network demand (Mbps).
- Interface capacity is simulated as 1 Gbps. Polling-derived rates use counter differences divided by the selected interval.
- These simplified models make calculations inspectable and should not be interpreted as facility-grade predictions.
