import streamlit as st
import pandas as pd

def filter_data(df):


    column = st.sidebar.selectbox("Choose column to filter:", df.columns)

    # checking and processing on Numeric Data filtering
    if pd.api.types.is_numeric_dtype(df[column]):
        
        include_nulls = st.sidebar.checkbox("Include NaN Values?") # include nulls?

        col_non_null = df[column].dropna()

        # Range setting min to max, avoiding null value 
        if not col_non_null.empty:
            min_val = int(col_non_null.min())
            max_val = int(col_non_null.max())

            selected_range = st.sidebar.slider("Select value range:",min_value=min_val,max_value=max_val,
                value=(min_val, max_val))

            # Data within range -> [min,max]
            result = df[(df[column] >= selected_range[0]) & (df[column] <= selected_range[1])]

            if include_nulls:
                null_rows = df[df[column].isnull()]
                result = pd.concat([result, null_rows])
        else:
            result = df[df[column].isnull()]

    # Processing Categorical columns
    else:
        unique_vals = df[column].astype(str).unique()
        selected_val = st.sidebar.selectbox("Select value:", unique_vals)

        if selected_val.lower() == 'nan':
            result = df[df[column].isnull()]
        else:
            result = df[df[column].astype(str) == selected_val]

    st.sidebar.markdown(f"Count of rows: {len(result)}")
    st.write("### Filtered Data")
    st.dataframe(result)

    return result

def sort_data(df):

    col = st.sidebar.selectbox("Select column to sort by:", df.columns)
    descending = st.sidebar.checkbox("Sort descending?", value=True)

    sorted_df = df.sort_values(by=col, ascending=not descending)
    st.write("### Sorted Data")
    st.dataframe(sorted_df)
    return sorted_df

def group_data(df):
    st.sidebar.markdown("### 🧮 Group Data")

    group_col = st.sidebar.selectbox("Select column to group by:", df.columns)
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    target_col = st.sidebar.selectbox("Select target column:", numeric_cols)
    agg_func = st.sidebar.selectbox("Select aggregation function:", ['count', 'mean', 'sum', 'min', 'max'])
    
    grouped_df = df.groupby(group_col)[target_col].agg(agg_func).reset_index()
    st.write(f"Grouped by {group_col}, aggregated `{target_col}` using `{agg_func}`")
    st.dataframe(grouped_df)

    return grouped_df

def show_unique_values(df):

    col = st.sidebar.selectbox("Select column:", df.columns)
    unique_vals = df[col].dropna().unique()
    st.sidebar.markdown(f"**Unique Values in `{col}`:** {len(unique_vals)}")
    st.write(f" Unique values in `{col}`")
    st.write(unique_vals)
    return unique_vals

def describe_summary(df):
    if st.button("📋 Show Describe Summary"):
        st.write("Summary of Your Data")
        st.dataframe(df.describe(include='all'))

def data_analysis(df,data_source):
    if data_source == "Upload CSV":
        file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if file:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
    elif data_source == "Paste Data":
        raw_text = st.text_area("Paste your data (list of dicts or dict of lists):")
        try:
            data_dict = eval(raw_text)
            df = pd.DataFrame(data_dict)
        except:
            st.error("Invalid format. Make sure it’s a valid Python dictionary/list.")
            df = pd.DataFrame()

# If DataFrame exists
    if 'df' in locals() and not df.empty:
        describe_summary(df)
        st.markdown("<h4 style='text-align: center;'>🧠 Choose a Data Operation</h4>", unsafe_allow_html=True)

        operations = ["Filter Rows", "Sort by Column", "Group by Column", "Show Unique Values"]
        
        selected_op = st.selectbox("Select a data operation to perform:", operations)

        st.sidebar.markdown(" ⚙️ Operation Settings")
        if selected_op == "Filter Rows":
            filtered_df = filter_data(df)

        elif selected_op == "Sort by Column":
            df = sort_data(df)

        elif selected_op == "Group by Column":
            df = group_data(df)

        elif selected_op == "Show Unique Values":
            show_unique_values(df)

# Handling Missing Values
def null_nonnull_counts(df):
    return pd.DataFrame({
        'Null Count': df.isnull().sum(),
        'Non-Null Count': df.notnull().sum()
    })

def fillna_with_mean(df):
    num_cols = df.select_dtypes(include='number').columns
    return df.fillna({col: df[col].mean() for col in num_cols})

def fillna_with_median(df):
    num_cols = df.select_dtypes(include='number').columns
    return df.fillna({col: df[col].median() for col in num_cols})

def fillna_with_mode(df):
    num_cols = df.select_dtypes(include='number').columns
    return df.fillna({col: df[col].mode()[0] for col in num_cols})

def handle_missing_data(df,data_source):
    if data_source == "Upload CSV":
        file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
        if file:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
    elif data_source == "Paste Data":
        raw_text = st.text_area("Paste your data (list of dicts or dict of lists):")
        try:
            data_dict = eval(raw_text)
            df = pd.DataFrame(data_dict)
        except:
            st.error("Invalid format. Make sure it’s a valid Python dictionary/list.")
            df = pd.DataFrame()


    fill_option = st.sidebar.radio(
        "Fill numeric NaN with:",
        ("None", "Mean", "Median", "Mode")
    )
    if fill_option == "None":
        st.markdown("### This is summary for missing values")
        summary_df = null_nonnull_counts(df)
        st.dataframe(summary_df)
    elif fill_option == "Mean":
        mean_df = fillna_with_mean(df)
        st.sidebar.success("Filled numeric NaNs with mean values.")
        st.dataframe(mean_df)
    elif fill_option == "Median":
        median_df = fillna_with_median(df)
        st.sidebar.success("Filled numeric NaNs with median values.")
        st.dataframe(median_df)
    elif fill_option == "Mode":
        mode_df = fillna_with_mode(df)
        st.sidebar.success("Filled numeric NaNs with mode values.")
        st.dataframe(mode_df)
