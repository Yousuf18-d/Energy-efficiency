import random
import pandas as pd
from IPython.core.display import display, HTML

# Step 1: Simulate appliance schedule
APPLIANCES = {
    "Washing Machine": {"duration": 2, "flexible": True},
    "Dishwasher": {"duration": 1, "flexible": True},
    "Heater": {"duration": 4, "flexible": False, "preferred_time": [6, 7, 8, 9]},
    "EV Charger": {"duration": 3, "flexible": True}
}

TARIFF = [0.25 if 6 <= hour <= 22 else 0.10 for hour in range(24)]

def find_optimal_schedule(duration):
    min_cost = float('inf')
    best_start = 0
    for hour in range(24 - duration + 1):
        cost = sum(TARIFF[hour + d] for d in range(duration))
        if cost < min_cost:
            min_cost = cost
            best_start = hour
    return best_start, min_cost

def schedule_appliances():
    schedule = {}
    for name, info in APPLIANCES.items():
        duration = info["duration"]
        if info.get("flexible", False):
            start_hour, cost = find_optimal_schedule(duration)
        else:
            available_times = info.get("preferred_time", list(range(24)))
            start_hour = available_times[0]
            cost = sum(TARIFF[start_hour + d] for d in range(duration))
        schedule[name] = {"Start Hour": start_hour, "Duration (h)": duration, "Cost ($)": round(cost, 2)}
    return schedule

schedule = schedule_appliances()

# Step 2: Create dataframe
df = pd.DataFrame.from_dict(schedule, orient='index')
df.reset_index(inplace=True)
df.rename(columns={'index': 'Appliance'}, inplace=True)

# Step 3: Create dynamic text report
def generate_summary(df):
    total_cost = df["Cost ($)"].sum()
    cheapest = df.loc[df["Cost ($)"].idxmin()]
    expensive = df.loc[df["Cost ($)"].idxmax()]

    summary = f"""
    <div style="color:#FFFFFF; font-family:Arial, sans-serif; font-size:16px; margin:20px; text-shadow:0 0 15px #FF1493, 0 0 30px #FF1493;">
        <b style="font-size:18px;">✅ <span style="color:#FFD700;">Total Estimated Energy Cost:</span> <span style="color:#FF1493;">${round(total_cost,2)}</span></b><br><br>
        <b style="font-size:16px; color:#39FF14;">⚡ <i>Most Efficient Appliance:</i></b> {cheapest['Appliance']} (<span style="color:#00FFFF;">${cheapest['Cost ($)']}</span>)<br>
        <b style="font-size:16px; color:#FF4500;">🔥 <i>Highest Energy User:</i></b> {expensive['Appliance']} (<span style="color:#FF4500;">${expensive['Cost ($)']}</span>)<br><br>
        <b style="font-size:16px;">🚀 <i>Efficiency Score:</i> <span style="color:#FFD700;">{round((1 - cheapest['Cost ($)']/expensive['Cost ($)'])*100)}%</span></b><br><br>
        <i style="color:#FF69B4;">Tip:</i> <b style="font-size:16px; color:#FFD700;">Running flexible appliances at night reduces cost by up to 60% due to lower tariffs!</b>
    </div>
    """
    return summary

# Step 4: Display table with new exotic theme
def display_futuristic_table(df):
    styles = """
    <style>
    table {
      border-collapse: collapse;
      width: 80%;
      margin: 20px auto;
      font-family: 'Arial', sans-serif;
      color: #FFD700;
      background-color: #000000;
      border: 2px solid #ADD8E6; /* Light Blue Border */
      box-shadow: 0 0 20px #ADD8E6; /* Light Blue Glow */
    }
    th, td {
      border: 1px solid #ADD8E6; /* Light Blue Border */
      padding: 12px;
      text-align: center;
      font-size: 16px;
      color: #FFFFFF;
      text-shadow: 0 0 10px #FFFFFF;
    }
    th {
      background-color: #330033;
      color: #39FF14;
      font-size: 18px;
      text-shadow: 0 0 10px #FF1493;
    }
    tr:hover {
      background-color: #4B004B;
    }
    caption {
      font-size: 22px;
      margin: 10px;
      color: #FF00FF;
      text-shadow: 0 0 10px #FF00FF;
    }
    </style>
    """
    html_table = df.to_html(index=False, escape=False)
    html_table = html_table.replace('<table border="1" class="dataframe">', '<table>')
    display(HTML(styles + f"<caption>⚡ Optimized Appliance Schedule ⚡</caption>" + html_table))

# Show both text + table
display(HTML(generate_summary(df)))
display_futuristic_table(df)
