import pandas as pd
import datetime

# Function to load data for a specific day
def load_data(day: str):
    return pd.read_csv(f"./data/{day}.csv", sep=";", parse_dates=["timestamp"])

# Function to modify 'customer_no' column by appending weekday
def modify_customer_no(df, weekday):
    df["customer_no"] = df["customer_no"].astype(str) + "_" + weekday

# Function to add missing checkout locations
def add_missing_checkout_location(df, weekday):
    checkout_customers = df[df["location"] == "checkout"]["customer_no"].unique()
    all_customers = df["customer_no"].unique()
    missing_customers = set(all_customers).difference(checkout_customers)
    new_timestamp = df["timestamp"].max() + pd.DateOffset(hours=2)
    missing_checkouts_data = {
        "timestamp": [new_timestamp] * len(missing_customers),
        "customer_no": list(missing_customers),
        "location": ["checkout"] * len(missing_customers),
        "weekday": weekday
    }
    return pd.concat([df, pd.DataFrame(missing_checkouts_data)], ignore_index=True)

# Function to add entrance state for customers
def add_entrance_state(df):
    min_timestamp_per_customer = df.groupby("customer_no")["timestamp"].min().reset_index()
    one_minute = datetime.timedelta(minutes=1)
    entrance_entries = min_timestamp_per_customer.apply(
        lambda x: {
            "timestamp": x["timestamp"] - one_minute,
            "customer_no": x["customer_no"],
            "location": "entrance"
        },
        axis=1
    )
    entrance_entries_df = pd.DataFrame(list(entrance_entries))
    return pd.concat([df, entrance_entries_df], ignore_index=True)

# Function to create a proper DataFrame structure
def make_df_proper(coming_data: list):
    df = pd.concat(coming_data).set_index('timestamp').sort_index()
    df = df[['customer_no', 'location']].rename(columns={'location': 'location0'})
    return df

# Load data for each weekday and modify 'customer_no' column
week_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
dataframes = []
for day in week_days:
    df = load_data(day)
    modify_customer_no(df, day)
    dataframes.append(df)

# Process dataframes
for i, df in enumerate(dataframes):
    dataframes[i] = add_missing_checkout_location(df, week_days[i])
    dataframes[i] = add_entrance_state(dataframes[i])

# Create a proper weekly data matrix
weekly_data_matrix = make_df_proper(dataframes)

# Group by customer number and resample
weekly_data_matrix = weekly_data_matrix.groupby("customer_no")["location0"].resample(rule="1min").ffill().reset_index()

# Create location1 column by shifting location0 within each customer group
weekly_data_matrix["location1"] = weekly_data_matrix.groupby("customer_no")["location0"].shift(-1)

# Fill missing values in location0 and location1
weekly_data_matrix["location0"].fillna("entrance", inplace=True)
weekly_data_matrix["location1"].fillna("checkout", inplace=True)

# Create transition matrix
transition_matrix = pd.crosstab(weekly_data_matrix['location0'],
                                weekly_data_matrix['location1'], normalize="index")

# Make a copy of the original transition matrix
transition_modified_animation = transition_matrix.copy()

# Modify transition probabilities for "entrance" and "checkout"
entrance_probs = [0.025, 0, 0, 0, 0, 0]
transition_modified_animation["entrance"] = entrance_probs
transition_modified_animation["checkout"].iloc[0] = 0.975
