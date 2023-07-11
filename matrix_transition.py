import pandas as pd
import datetime

def get_data(filename, weekday):
    df = pd.read_csv(filename, sep=";", parse_dates=["timestamp"])
    df["weekday"] = weekday
    return df

monday = get_data("./data/monday.csv", "monday")
tuesday = get_data("./data/tuesday.csv", "tuesday")
wednesday = get_data("./data/wednesday.csv", "wednesday")
thursday = get_data("./data/thursday.csv", "thursday")
friday = get_data("./data/friday.csv", "friday")
def new_customer_no(df, weekday):
    df["customer_no"] = df["customer_no"].astype(str) + "_" + weekday

new_customer_no(monday, "monday")
new_customer_no(tuesday, "tuesday")
new_customer_no(wednesday, "wednesday")
new_customer_no(thursday, "thursday")
new_customer_no(friday, "friday")

def add_missing_checkout_location(df):
    checkout_customers = df[df["location"] == "checkout"]["customer_no"].unique()
    whole_customers = df["customer_no"].unique()
    diff = set(whole_customers).difference(checkout_customers)
    new_timestamp = df["timestamp"].max() + pd.DateOffset(hours=2)
    missing_checkouts = pd.DataFrame({"timestamp": [new_timestamp] * len(diff),"customer_no": list(diff),"location": ["checkout"] * len(diff), "weekday":df["weekday"][0]})
    df = pd.concat([df, missing_checkouts], ignore_index=True)
    return df
monday = add_missing_checkout_location(monday)
tuesday = add_missing_checkout_location(tuesday)
wednesday = add_missing_checkout_location(wednesday)
thursday = add_missing_checkout_location(thursday)
friday = add_missing_checkout_location(friday)
def add_entrance_state(df):
    min_datetime = df.groupby("customer_no")["timestamp"].min().reset_index()
    one_minute = datetime.timedelta(minutes=1)
    entrance_entries = min_datetime.apply(lambda x: {"timestamp": x["timestamp"] - one_minute, "customer_no": x["customer_no"], "location": "entrance"}, axis=1)
    entrance_entries = pd.DataFrame(list(entrance_entries))
    df = pd.concat([df, entrance_entries], ignore_index=True)
    return df
monday = add_entrance_state(monday)
tuesday = add_entrance_state(tuesday)
wednesday = add_entrance_state(wednesday)
thursday = add_entrance_state(thursday)
friday = add_entrance_state(friday)

def make_Df_proper(comming_data):
    df = pd.concat(comming_data, ignore_index=True)
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)
    df=df[['customer_no', 'location']]
    df.rename(columns={'location': 'location0'}, inplace=True)
    return df
weekly_data_matrix=make_Df_proper([monday, tuesday, wednesday, thursday, friday])

weekly_data_matrix=weekly_data_matrix.groupby("customer_no")[["location0"]].resample(rule="1min").ffill()
weekly_data_matrix.reset_index(inplace=True)
weekly_data_matrix["location1"] =weekly_data_matrix.groupby("customer_no")["location0"].shift(-1)

weekly_data_matrix["location0"].fillna("entrance", inplace=True)
weekly_data_matrix["location1"].fillna("checkout", inplace=True)

transition=pd.crosstab(weekly_data_matrix['location0'], weekly_data_matrix['location1'], normalize="index")
transition_modified_animation=transition.copy()
transition_modified_animation["entrance"]= [0.050000,0.00000,0.00000,0.00000,0.00000,0.00000]
transition_modified_animation["checkout"]= [0.95,0.094521,0.210537,0.0000,0.189091,0.137560]

