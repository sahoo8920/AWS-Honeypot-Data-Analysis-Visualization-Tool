# filtering functions for the datafrane
# used by main.py


def search_query(df, query_string):
    temp_df = df.copy()
    key_value_list = query_string.split(",")
    for key_value in key_value_list:
        key = key_value.split(":")[0]
        value = key_value.split(":")[1]
        regexp = r"\b" + r"\b|\b".join(value.split("|")) + r"\b"
        if key == "host":
            temp_df = temp_df[temp_df["host"].str.contains(regexp, regex=True, na=False, case=False)]
        elif key.lower() == "proto":
            temp_df = temp_df[temp_df["proto"].str.contains(regexp, regex=True, na=False, case=False)]
        elif key.lower() == "spt":
            temp_df = temp_df[temp_df["spt"].str.contains(regexp, regex=True, na=False, case=False)]
        elif key.lower() == "dpt":
            temp_df = temp_df[temp_df["dpt"].str.contains(regexp, regex=True, na=False, case=False)]
        elif key.lower() == "srcstr":
            temp_df = temp_df[temp_df["srcstr"].str.contains(regexp, regex=True, na=False, case=False)]
        elif key.lower() == "country":
            temp_df = temp_df[temp_df["country"].str.contains(regexp, regex=True, na=False, case=False)]
    return temp_df


def search_period(df, start_date, end_date):
    return df[(df["datetime"] >= start_date) & (df["datetime"] <= end_date)]

