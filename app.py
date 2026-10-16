"""GreenCloud Suite — simulated Green IT Unit IV demonstration."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="GreenCloud Suite", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

GREEN = "#176B45"
PALETTE = ["#176B45", "#49A078", "#8FCB9B", "#E8B04A", "#D95D5D"]
HOSTS = ["Host-01", "Host-02", "Host-03", "Host-04", "Host-05"]
VM_NAMES = [f"VM-{i:02d}" for i in range(1, 11)]

def defaults():
    # Deterministic, internally consistent demonstration data.
    vm = pd.DataFrame({
        "VM": VM_NAMES,
        "CPU demand (cores)": [8, 6, 6, 5, 5, 4, 4, 3, 3, 2],
        "Memory demand (GB)": [24, 20, 18, 16, 14, 12, 10, 8, 8, 6],
        "Network demand (Mbps)": [420, 350, 300, 260, 220, 180, 140, 110, 90, 70],
        "Host": HOSTS + HOSTS,
    })
    capacities = [24, 24, 24, 24, 24]
    memcaps = [64, 64, 64, 64, 64]
    hosts = pd.DataFrame({"Host": HOSTS, "CPU capacity (cores)": capacities, "Memory capacity (GB)": memcaps})
    return vm, hosts

if "vm_data" not in st.session_state:
    st.session_state.vm_data, st.session_state.host_data = defaults()
if "optimized" not in st.session_state:
    st.session_state.optimized = False
if "balanced" not in st.session_state:
    st.session_state.balanced = False

def host_summary(vm=None):
    vm = st.session_state.vm_data if vm is None else vm
    h = st.session_state.host_data.copy()
    use = vm.groupby("Host").agg(cpu_used=("CPU demand (cores)", "sum"), mem_used=("Memory demand (GB)", "sum"), network=("Network demand (Mbps)", "sum")).reset_index()
    h = h.merge(use, on="Host", how="left").fillna(0)
    h["CPU utilization (%)"] = (100*h.cpu_used/h["CPU capacity (cores)"]).clip(0, 100)
    h["Memory utilization (%)"] = (100*h.mem_used/h["Memory capacity (GB)"]).clip(0, 100)
    # Illustrative power model: 90 W idle + up to 150 W proportional to CPU load.
    h["Power (W)"] = 90 + 1.5*h.cpu_used
    h["Temperature (°C)"] = 23 + .27*h["CPU utilization (%)"] + .004*h.network
    h["Status"] = np.where(h["CPU utilization (%)"] >= 85, "Warning", "Normal")
    return h

def energy_saving(vm=None):
    h = host_summary(vm)
    active = int((h.cpu_used > 0).sum())
    # Consolidation estimate compared with the same illustrative power model at fewer active hosts.
    before = h["Power (W)"].sum()
    after = max(1, int(np.ceil(vm["CPU demand (cores)"].sum()/24)))*90 + vm["CPU demand (cores)"].sum()*1.5
    return max(0, before-after), before, after

def chart(fig, height=320):
    fig.update_layout(height=height, margin=dict(l=8,r=8,t=35,b=8), paper_bgcolor="#14221a", plot_bgcolor="#14221a", font=dict(color="#dce9df"), legend_title_text="")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def kpis(items):
    cols = st.columns(len(items))
    for col, (icon, label, value, note) in zip(cols, items):
        with col:
            st.markdown(f'<div class="kpi"><div class="kpi-top">{icon} <span>{label}</span></div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)

def title(text, sub=None):
    st.title(text)
    if sub: st.caption(sub)

def concept_box(heading, text):
    with st.expander(heading): st.write(text)

st.markdown("""<style>
:root{color-scheme:dark}
.stApp{background:#0b1410;color:#e6efe9;font-family:'DM Sans',sans-serif}.block-container{padding-top:1.5rem;max-width:1500px}
[data-testid="stHeader"]{background:#0b1410}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0b2118,#123d2a);border-right:1px solid #244735}
[data-testid="stSidebar"] *{color:#e6f2e9}
[data-testid="stSidebar"] [data-testid="stRadio"] label{color:#e6f2e9!important;font-weight:600}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{color:#e6f2e9!important}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"]{gap:5px}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]{background:#133624;border:1px solid #28543b;border-radius:8px;padding:8px 10px}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"]:hover{background:#1b4a32}
[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"]{background:#236440;border-color:#59aa75}
.kpi{background:#14221a;border:1px solid #2c4535;border-top:3px solid #49a078;border-radius:13px;padding:16px 18px;min-height:116px;box-shadow:0 4px 16px #0004}
.kpi-top{color:#adbdaf;font-size:13px;font-weight:600}.kpi-top span{margin-left:6px}.kpi-value{font-family:Manrope,sans-serif;color:#e7f5e9;font-size:27px;font-weight:800;margin:8px 0 2px}.kpi-note{font-size:11px;color:#91a496}
h1,h2,h3{font-family:Manrope,sans-serif;color:#e6f2e9}p,li,label,.stCaption{color:#c4d2c8} [data-testid="stMarkdownContainer"]{color:#d4e0d7}
.stButton>button{background:#23764a;color:white;border:1px solid #4d996b;border-radius:8px;font-weight:700;padding:.55rem 1rem}.stButton>button:hover{background:#2d8a58;color:white;border-color:#7bc391}
[data-testid="stDataFrame"],.stDataFrame{background:#14221a;border-radius:10px}
div[data-baseweb="input"] input,div[data-baseweb="select"]>div,div[data-baseweb="textarea"] textarea{background:#14221a;color:#e6efe9}
[data-testid="stSlider"] label,[data-testid="stSelectbox"] label{color:#d9e6dc}
.stAlert{border-radius:10px}.footer{color:#94a99a;font-size:12px;border-top:1px solid #2a4032;padding-top:14px;margin-top:28px}
hr{border-color:#2a4032}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌿 GreenCloud Suite")
    st.caption("GREEN IT · UNIT IV")
    page = st.radio("Navigate", ["Overview Dashboard", "GreenCloud Monitor", "GreenVM Optimizer", "ThermalAware Scheduler", "SNMP Traffic Analyzer", "About & Unit IV Concepts"], label_visibility="collapsed")
    st.divider()
    if st.button("↺ Reset to default data", use_container_width=True):
        st.session_state.vm_data, st.session_state.host_data = defaults()
        st.session_state.optimized = False
        st.session_state.balanced = False
        st.success("Demo data and optimization results reset.")
    st.caption("All values are simulated for learning.")

vm = st.session_state.vm_data.copy()
hosts = host_summary(vm)
total_cpu = vm["CPU demand (cores)"].sum()
avg_cpu = hosts["CPU utilization (%)"].mean()
saving_w, power_before, power_after = energy_saving(vm)
network_total = vm["Network demand (Mbps)"].sum()
hotspots = int((hosts["Temperature (°C)"] >= 35).sum())

if page == "Overview Dashboard":
    title("Overview Dashboard", "A simulated data-center view across energy, compute, temperature and network activity.")
    kpis([("🖥️","Physical servers","5","Fixed demonstration fleet"),("▣","Active VMs",str(len(vm)),"Across five physical hosts"),("⚡","Estimated power",f"{hosts['Power (W)'].sum():,.0f} W","Illustrative host power model"),("⇄","Aggregate traffic",f"{network_total:,.0f} Mbps","Configured VM demand"),("◉","Average CPU",f"{avg_cpu:.1f}%","Mean across all hosts"),("🌡️","Thermal hot spots",str(hotspots),"At or above 35 °C"),("🌱","Potential power reduction",f"{saving_w:.0f} W","Consolidation estimate")])
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Power profile by host")
        chart(px.bar(hosts,x="Host",y="Power (W)",color="Power (W)",color_continuous_scale=["#a8d5b4",GREEN],labels={"Power (W)":"Estimated power (W)"}))
    with c2:
        st.subheader("CPU utilization by host")
        chart(px.bar(hosts,x="Host",y="CPU utilization (%)",color="CPU utilization (%)",color_continuous_scale=["#9bd3a8","#e8b04a","#d95d5d"],range_color=[0,100]))
    a,b=st.columns([1.2,1])
    with a:
        st.subheader("Server status")
        view=hosts[["Host","cpu_used","CPU capacity (cores)","CPU utilization (%)","Memory utilization (%)","Power (W)","Temperature (°C)","Status"]].rename(columns={"cpu_used":"CPU used (cores)"})
        st.dataframe(view.style.format({"CPU utilization (%)":"{:.1f}%","Memory utilization (%)":"{:.1f}%","Power (W)":"{:.0f} W","Temperature (°C)":"{:.1f} °C"}).map(lambda x:"color:#b23b3b;font-weight:700" if x=="Warning" else "color:#176b45;font-weight:700",subset=["Status"]),use_container_width=True,hide_index=True)
    with b:
        st.subheader("Energy-saving opportunities")
        for x in ["Consolidate low-load VMs onto fewer hosts when capacity allows.","Use network traffic and workload statistics to identify idle VMs.","Avoid concentrating CPU load on hosts above the thermal threshold.","Review idle capacity before provisioning additional infrastructure.","Track power and utilization together to validate each policy."]:
            st.markdown(f"✅ {x}")
    st.info("Networking adds interface and switching load; virtualization improves utilization by sharing physical capacity; thermal management can reduce cooling demand by keeping workloads within a balanced temperature range.")

elif page == "GreenCloud Monitor":
    title("GreenCloud Monitor", "Explore how workload, operating power and monitoring duration shape estimated energy use.")
    left,right=st.columns([1,2])
    with left:
        active_power=st.slider("Active power (W)",100,600,320,10)
        idle_power=st.slider("Idle power (W)",20,250,95,5)
        duration=st.slider("Monitoring duration (hours)",1,24,8)
        alert=st.slider("Power alert threshold (W)",200,1200,850,25)
    active_duration=duration*.72; idle_duration=duration-active_duration
    active_energy=active_power*active_duration; idle_energy=idle_power*idle_duration
    current_power=hosts["Power (W)"].sum()
    with right:
        kpis([("⚡","Estimated power",f"{current_power:,.0f} W","Aggregate host estimate"),("🔋","Energy consumed",f"{(active_energy+idle_energy)/1000:.2f} kWh",f"Over {duration} monitoring hours"),("⇄","Network traffic",f"{network_total:,.0f} Mbps","Simulated aggregate demand"),("🖥️","Active servers",f"{(hosts.cpu_used>0).sum()} / 5","Hosts carrying VMs"),("🌱","Savings estimate",f"{saving_w:.0f} W","If consolidation is feasible")])
    if current_power>alert: st.error(f"Power alert: estimated aggregate power ({current_power:.0f} W) exceeds the configured {alert} W threshold.")
    else: st.success(f"Power estimate is within the configured {alert} W alert threshold.")
    st.markdown(f"**Energy contribution:** active = {active_power} W × {active_duration:.1f} h = **{active_energy/1000:.2f} kWh** · idle = {idle_power} W × {idle_duration:.1f} h = **{idle_energy/1000:.2f} kWh**")
    st.caption("Energy in Wh = power in W × time in hours. Active and idle periods are an illustrative split of the selected monitoring window.")
    t=np.arange(0,duration+.1,max(duration/12,.1)); p=idle_power+(active_power-idle_power)*(0.65+0.12*np.sin(t*2*np.pi/max(duration,1)))
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Power consumption trend")
        chart(px.line(pd.DataFrame({"Hour":t,"Power (W)":p}),x="Hour",y="Power (W)",markers=True))
    with c2:
        st.subheader("Network traffic trend")
        traffic=network_total*(.72+.14*np.sin(t*2*np.pi/max(duration,1)+.6))
        chart(px.area(pd.DataFrame({"Hour":t,"Traffic (Mbps)":traffic}),x="Hour",y="Traffic (Mbps)",markers=True))
    st.subheader("Server utilization and energy")
    st.dataframe(hosts[["Host","CPU utilization (%)","Memory utilization (%)","Power (W)","Temperature (°C)","Status"]].style.format({"CPU utilization (%)":"{:.1f}%","Memory utilization (%)":"{:.1f}%","Power (W)":"{:.0f} W","Temperature (°C)":"{:.1f} °C"}),use_container_width=True,hide_index=True)
    st.markdown("**Recommendations:** consolidate lightly loaded VMs; right-size provisioned CPU and memory; measure network traffic alongside compute; compare active and idle energy over the same interval.")
    concept_box("Unit IV links: Green IT and the Cloud · IaaS and Power · Network Processes and Power · Gathering and Using Statistics", "Cloud infrastructure turns compute and networking demand into facility energy use. IaaS capacity choices influence powered server resources. Network interfaces and switching carry workload traffic and consume energy. Collecting consistent time-series statistics helps operators identify idle capacity and evaluate efficiency policies.")

elif page == "GreenVM Optimizer":
    title("GreenVM Optimizer", "A greedy consolidation demonstration using shared five-host and ten-VM sample data.")
    st.caption("Simulation only: no real VM is moved and no physical host is powered off. Capacity limits: 24 CPU cores and 64 GB RAM per host.")
    pre=host_summary(vm)
    kpis([("🧩","Virtual machines",str(len(vm)),"Sample workload set"),("🖥️","Active hosts",str((pre.cpu_used>0).sum()),"Before current simulation"),("◉","Average CPU",f"{pre['CPU utilization (%)'].mean():.1f}%","Across five hosts"),("⚡","Estimated power",f"{pre['Power (W)'].sum():.0f} W","Illustrative power model")])
    if st.button("▶ Run Optimization",key="optimize"):
        # First-fit decreasing by CPU demand, with both CPU and memory checked.
        placements=[]; loads={h:{"cpu":0,"mem":0} for h in HOSTS}
        ordered=vm.sort_values(["CPU demand (cores)","Memory demand (GB)"],ascending=False)
        for _,row in ordered.iterrows():
            chosen=next((h for h in HOSTS if loads[h]["cpu"]+row["CPU demand (cores)"]<=24 and loads[h]["mem"]+row["Memory demand (GB)"]<=64),None)
            if chosen is None: chosen=row["Host"]
            loads[chosen]["cpu"]+=row["CPU demand (cores)"]; loads[chosen]["mem"]+=row["Memory demand (GB)"]
            placements.append((row.VM,chosen))
        assign=dict(placements); st.session_state.vm_data["Host"]=st.session_state.vm_data.VM.map(assign)
        st.session_state.optimized=True
        st.success("Greedy placement completed. The displayed host assignments now reflect the simulated optimization.")
    post=host_summary()
    before=st.session_state.vm_data.copy()
    # Recover original assignments for a meaningful comparison snapshot.
    if "before_vm" not in st.session_state: st.session_state.before_vm=defaults()[0]
    if st.session_state.optimized and not st.session_state.get("before_saved",False):
        st.session_state.before_vm=defaults()[0]; st.session_state.before_saved=True
    # Default baseline is the original deterministic spread.
    baseline=st.session_state.before_vm.copy()
    bsum=host_summary(baseline); asum=host_summary(vm)
    saved=max(0,bsum["Power (W)"].sum()-asum["Power (W)"].sum())
    c1,c2=st.columns(2)
    with c1:
        st.subheader("CPU and memory utilization")
        util=post.melt(id_vars="Host",value_vars=["CPU utilization (%)","Memory utilization (%)"],var_name="Resource",value_name="Utilization (%)")
        chart(px.bar(util,x="Host",y="Utilization (%)",color="Resource",barmode="group",color_discrete_sequence=PALETTE))
    with c2:
        st.subheader("Power: baseline and current")
        cmp=pd.DataFrame({"Host":HOSTS,"Baseline (W)":bsum["Power (W)"].values,"Current (W)":asum["Power (W)"].values}).melt("Host",var_name="Scenario",value_name="Power (W)")
        chart(px.bar(cmp,x="Host",y="Power (W)",color="Scenario",barmode="group",color_discrete_sequence=["#9db9a4",GREEN]))
    kpis([("⚡","Baseline power",f"{bsum['Power (W)'].sum():.0f} W","Illustrative estimate"),("🌿","Current power",f"{asum['Power (W)'].sum():.0f} W","After placement simulation"),("↓","Estimated reduction",f"{saved:.0f} W","Compared with original assignments"),("🌙","Dormant candidates",str(int((asum.cpu_used==0).sum())),"Only if separately validated")])
    st.subheader("VM allocation")
    alloc=vm.merge(baseline[["VM","Host"]].rename(columns={"Host":"Baseline host"}),on="VM")
    st.dataframe(alloc.rename(columns={"Host":"Current host"}),use_container_width=True,hide_index=True)
    st.markdown("**Migration suggestions:** consolidate VMs currently spread across lightly loaded hosts, after checking application affinity, latency, redundancy, and memory pressure. Hosts with no assigned VM are simulated dormant candidates only.")
    if (post["CPU utilization (%)"]>100).any() or (post["Memory utilization (%)"]>100).any(): st.warning("Capacity warning: one or more hosts exceed a configured limit. Review placement before using as a real policy.")
    concept_box("Unit IV links: Virtualization Behavior · Sustainability with VM Management · Importance of Virtualization Management · Green Cloud as a Network Management Problem", "Consolidation raises useful utilization on fewer machines and can reduce idle server power. A manager needs placement visibility, CPU and memory limits, workload compatibility, and traffic context. Network demand and latency can constrain otherwise efficient placement.")

elif page == "ThermalAware Scheduler":
    title("ThermalAware Scheduler", "A transparent workload-to-temperature model for exploring heat-aware placement.")
    threshold=st.slider("Hot-spot threshold (°C)",28,45,35)
    st.caption("Illustrative temperature model: 23 °C + 0.27 × CPU utilization (%) + 0.004 × network demand (Mbps). Not a physical thermal model.")
    h=host_summary()
    kpis([("🌡️","Mean host temperature",f"{h['Temperature (°C)'].mean():.1f} °C","Simulated estimate"),("🔥","Hosts above threshold",str(int((h["Temperature (°C)"]>=threshold).sum())),f"Threshold {threshold} °C"),("◉","Mean CPU utilization",f"{h['CPU utilization (%)'].mean():.1f}%","Across five hosts"),("❄️","Cooling opportunity",f"{max(0,(h['Temperature (°C)'].max()-threshold)):.1f} °C","Excess above threshold, if any")])
    c1,c2=st.columns([1,1.2])
    with c1:
        st.subheader("Server temperature map")
        chart(px.imshow([h["Temperature (°C)"].values],x=h.Host,y=["Temperature"],text_auto=".1f",color_continuous_scale=["#b8e0c0","#f1c453","#d95852"],range_color=[25,42]),height=200)
        card_cols=st.columns(5)
        for col,(_,r) in zip(card_cols,h.iterrows()):
            with col: st.metric(r.Host,f"{r['Temperature (°C)']:.1f} °C",f"CPU {r['CPU utilization (%)']:.0f}%")
    with c2:
        st.subheader("CPU utilization versus temperature")
        chart(px.scatter(h,x="CPU utilization (%)",y="Temperature (°C)",text="Host",color="Temperature (°C)",color_continuous_scale=["#8fc99b","#d95d5d"],range_color=[threshold-6,threshold+6]))
    if (h["Temperature (°C)"]>=threshold).any(): st.warning("Hot-spot warning: one or more simulated hosts meet or exceed the selected threshold.")
    else: st.success("No simulated host is above the selected threshold.")
    if st.button("⚖ Balance Workloads",key="balance"):
        # Greedy transfer from hottest host to coolest host with CPU/RAM headroom.
        work=st.session_state.vm_data.copy(); changed=False
        for _ in range(5):
            hh=host_summary(work).sort_values("Temperature (°C)",ascending=False)
            hot=hh.iloc[0]; cools=hh.sort_values("Temperature (°C)")
            if hot["Temperature (°C)"]<threshold: break
            candidates=work[work.Host==hot.Host].sort_values("CPU demand (cores)")
            moved=False
            for idx,row in candidates.iterrows():
                for _,cool in cools.iterrows():
                    if cool.Host==hot.Host: continue
                    current=work[work.Host==cool.Host]
                    if current["CPU demand (cores)"].sum()+row["CPU demand (cores)"]<=24 and current["Memory demand (GB)"].sum()+row["Memory demand (GB)"]<=64:
                        work.loc[work.VM==row.VM,"Host"]=cool.Host; changed=moved=True; break
                if moved: break
            if not moved: break
        st.session_state.vm_data=work; st.session_state.balanced=True
        if changed: st.success("Workload balance simulated. Host temperatures and assignments have updated; migration overhead is represented as a 2% temporary energy allowance.")
        else: st.info("No capacity-safe move was found under the current temperature rule.")
    after=host_summary()
    compare=pd.concat([h.assign(Scenario="Before"),after.assign(Scenario="After")])
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Workload distribution")
        chart(px.bar(compare,x="Host",y="CPU utilization (%)",color="Scenario",barmode="group",color_discrete_sequence=["#9db9a4",GREEN]))
    with c2:
        st.subheader("Temperature comparison")
        chart(px.bar(compare,x="Host",y="Temperature (°C)",color="Scenario",barmode="group",color_discrete_sequence=["#efbf65","#55a879"]))
    if st.session_state.balanced: st.caption("Migration overhead allowance: 2% temporary energy per moved workload, an illustrative modeling assumption.")
    st.markdown("**Cooling guidance:** avoid sustained hotspots; distribute CPU-heavy workloads when memory capacity permits; consider workload affinity and migration cost; treat temperature readings as model outputs, not sensor data.")
    concept_box("Unit IV links: Need for Thermal-Aware Virtualization · Achieving Sustainability on the Cloud · Virtualization Management", "Virtualization gives a scheduler a way to redistribute workloads. Thermal-aware placement can avoid concentrating heat, while workload management balances energy, capacity, performance, and migration overhead. Cooling savings depend on facility design and are not calculated as actual energy here.")

elif page == "SNMP Traffic Analyzer":
    title("SNMP Green Traffic Analyzer", "Simulated interface counters demonstrate polling, rate calculation and traffic characterization.")
    interval=st.slider("Polling interval (seconds)",5,120,30,5)
    threshold=st.slider("Interface utilization alert threshold (%)",10,100,70,5)
    st.caption("No SNMP agents are contacted. Counter values are simulated and derive from VM network demand.")
    rng=np.random.default_rng(42)
    records=[]
    for i,row in vm.iterrows():
        rate_mbps=float(row["Network demand (Mbps)"])*rng.uniform(.65,1.0)
        in_mbps=rate_mbps*rng.uniform(.42,.66); out_mbps=rate_mbps-in_mbps
        cap=1000.0; in_bps=in_mbps*1_000_000/8; out_bps=out_mbps*1_000_000/8
        in_oct=int(in_bps*interval); out_oct=int(out_bps*interval)
        in_rate=(in_oct/interval)*8; out_rate=(out_oct/interval)*8
        util=100*(in_rate+out_rate)/(cap*1_000_000)
        records.append({"VM":row.VM,"Host":row.Host,"Interface":"eth0","ifInOctets":in_oct,"ifOutOctets":out_oct,"ifSpeed":"1 Gbps","Incoming (Mbps)":in_rate/1e6,"Outgoing (Mbps)":out_rate/1e6,"Utilization (%)":min(100,util)})
    traffic=pd.DataFrame(records)
    kpis([("⇣","Incoming traffic",f"{traffic['Incoming (Mbps)'].sum():.0f} Mbps","Across simulated interfaces"),("⇡","Outgoing traffic",f"{traffic['Outgoing (Mbps)'].sum():.0f} Mbps","Across simulated interfaces"),("◉","Mean interface use",f"{traffic['Utilization (%)'].mean():.1f}%","Capacity is 1 Gbps per interface"),("⚠️","High-use interfaces",str(int((traffic["Utilization (%)"]>=threshold).sum())),f"At or above {threshold}%")])
    if (traffic["Utilization (%)"]>=threshold).any(): st.warning("Traffic alert: at least one simulated interface is at or above the selected utilization threshold.")
    else: st.success("No simulated interface is above the selected utilization threshold.")
    st.subheader("Simulated interface counters and rates")
    st.dataframe(traffic.style.format({"Incoming (Mbps)":"{:.2f}","Outgoing (Mbps)":"{:.2f}","Utilization (%)":"{:.1f}%"}),use_container_width=True,hide_index=True)
    st.caption("Rates use successive-counter differences over the polling interval: bytes/s = Δoctets ÷ seconds; bits/s = bytes/s × 8; utilization = combined bits/s ÷ ifSpeed × 100. The displayed counters represent one simulated polling interval.")
    top=traffic.assign(Total=traffic["Incoming (Mbps)"]+traffic["Outgoing (Mbps)"]).sort_values("Total",ascending=False)
    c1,c2=st.columns(2)
    with c1:
        st.subheader("Top talkers: incoming and outgoing")
        chart(px.bar(top.head(8).melt(id_vars="VM",value_vars=["Incoming (Mbps)","Outgoing (Mbps)"],var_name="Direction",value_name="Traffic (Mbps)"),x="VM",y="Traffic (Mbps)",color="Direction",barmode="group",color_discrete_sequence=[GREEN,"#91c9a0"]))
    with c2:
        st.subheader("Interface utilization")
        chart(px.bar(traffic.sort_values("Utilization (%)",ascending=False),x="VM",y="Utilization (%)",color="Utilization (%)",color_continuous_scale=["#8fc99b","#e8b04a","#d95d5d"],range_color=[0,100]))
    low=traffic[traffic["Utilization (%)"]<10]
    st.markdown("**Relatively idle VMs/interfaces:** " + (", ".join(low.VM) if len(low) else "none below 10% utilization in this sample"))
    st.markdown("**Energy recommendations:** identify persistent low-traffic VMs for consolidation review; correlate traffic with CPU and memory demand; retain headroom for bursts; use interface utilization trends before changing placement.")
    concept_box("Unit IV links: Networking and Power · Traffic Characterization in Virtualized Environments · Hypervisors · SNMP in Green Clouds · Network Management Model", "A network manager polls interface counters and derives rates from differences over time. VM and host metadata lets operators correlate traffic with workloads. Hypervisors expose virtual network activity that can be associated with VM placement. These statistics help identify underused infrastructure and guide consolidation, subject to performance and latency needs.")

else:
    title("About & Unit IV Concepts", "GreenCloud Suite · Green Information Technology · Unit IV — Green Cloud Computing")
    st.markdown("### Project profile")
    c1,c2=st.columns([1.1,1])
    with c1:
        st.markdown("**Author:** Manisha Chaubey  \n**USN:** 1NT23IS116  \n**Institution:** Nitte Meenakshi Institute of Technology (NMIT), Bangalore  \n**Subject:** Green Information Technology (GIT)  \n**Assignment:** Unit IV — Green Cloud Computing")
        st.markdown("### Objective")
        st.write("Demonstrate four practical green cloud concepts through consistent simulated data, transparent calculations, interactive visualizations, and capacity-aware optimization examples.")
    with c2:
        st.markdown("### Four applications")
        st.markdown("1. **GreenCloud Monitor** — power, energy, network trends and alerts.\n2. **GreenVM Optimizer** — VM placement and host consolidation.\n3. **ThermalAware Scheduler** — temperature-aware workload balancing.\n4. **SNMP Traffic Analyzer** — interface counter and traffic-rate analysis.")
    st.markdown("### Unit IV concepts demonstrated")
    st.write("Green IT and cloud infrastructure; IaaS and power; networking and energy consumption; cloud statistics; virtualization behavior and management; sustainable VM placement; thermal-aware virtualization; traffic characterization; hypervisor visibility; SNMP polling and green network management.")
    st.info("Traffic-aware VM management can reduce energy use when low-traffic or underused workloads are safely consolidated onto fewer active hosts. Placement decisions must still honor CPU, memory, latency, availability, and workload affinity.")
    st.warning("Disclaimer: all measurements, counters, temperatures, optimizations, and savings are simulated estimates for an academic demonstration. No physical infrastructure or real SNMP agent is monitored or controlled.")
    st.markdown('<div class="footer">Developed by <b>Manisha Chaubey</b> · NMIT Bangalore · USN 1NT23IS116</div>',unsafe_allow_html=True)

if page != "About & Unit IV Concepts":
    st.markdown('<div class="footer">GreenCloud Suite · Academic simulation · Manisha Chaubey · NMIT Bangalore</div>',unsafe_allow_html=True)
