import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="CSV Analytics Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CSV Analytics Assistant")

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Normalize columns
    df.columns = df.columns.str.lower()

    # --------------------------------------------------
    # DATASET PREVIEW
    # --------------------------------------------------
    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    # --------------------------------------------------
    # DATASET INFO
    # --------------------------------------------------
    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # --------------------------------------------------
    # SUMMARY STATISTICS
    # --------------------------------------------------
    st.subheader("Summary Statistics")

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        st.dataframe(numeric_df.describe())
    else:
        st.info("No numeric columns found.")

    # --------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------
    st.subheader("Missing Values")

    missing_values = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_values)

    # --------------------------------------------------
    # VISUAL ANALYTICS
    # --------------------------------------------------
    st.subheader("📈 Visual Analytics")

    numeric_columns = numeric_df.columns.tolist()

    if len(numeric_columns) > 0:

        selected_column = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        chart_type = st.selectbox(
            "Select Chart Type",
            [
                "Bar Chart",
                "Line Chart",
                "Histogram"
            ]
        )

        fig, ax = plt.subplots()

        if chart_type == "Bar Chart":

            ax.bar(
                range(len(df)),
                df[selected_column]
            )

            ax.set_title(
                f"Bar Chart - {selected_column}"
            )

        elif chart_type == "Line Chart":

            ax.plot(
                df[selected_column]
            )

            ax.set_title(
                f"Line Chart - {selected_column}"
            )

        elif chart_type == "Histogram":

            ax.hist(
                df[selected_column]
            )

            ax.set_title(
                f"Histogram - {selected_column}"
            )

        st.pyplot(fig)

    # --------------------------------------------------
    # CORRELATION MATRIX
    # --------------------------------------------------
    st.subheader("Correlation Matrix")

    if not numeric_df.empty:

        corr_matrix = numeric_df.corr()

        st.dataframe(corr_matrix)

    # --------------------------------------------------
    # DOWNLOAD BUTTON
    # --------------------------------------------------
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Dataset",
        data=csv,
        file_name="processed_dataset.csv",
        mime="text/csv"
    )

    # --------------------------------------------------
    # QUESTION ANSWERING
    # --------------------------------------------------
    st.subheader("🤖 Ask Questions About Your Dataset")

    question = st.text_input(
        "Examples: highest total revenue, average unit price, how many rows"
    )

    if question:

        question = question.lower()

        column_name = None

        for col in df.columns:
            if col in question:
                column_name = col
                break

        # --------------------------
        # GENERAL QUESTIONS
        # --------------------------
        if "rows" in question:

            st.success(
                f"Number of rows: {df.shape[0]}"
            )

        elif "columns" in question:

            st.success(
                f"Number of columns: {df.shape[1]}"
            )

        elif "missing" in question:

            st.dataframe(missing_values)

        elif "summary" in question or "describe" in question:

            st.dataframe(numeric_df.describe())

        # --------------------------
        # COLUMN OPERATIONS
        # --------------------------
        elif column_name:

            try:

                if "highest" in question or "max" in question:

                    result = df[column_name].max()

                    st.success(
                        f"The highest value in '{column_name}' is {result}"
                    )

                elif "lowest" in question or "min" in question:

                    result = df[column_name].min()

                    st.success(
                        f"The lowest value in '{column_name}' is {result}"
                    )

                elif "average" in question or "mean" in question:

                    result = df[column_name].mean()

                    st.success(
                        f"The average value of '{column_name}' is {result:.2f}"
                    )

                elif "total" in question or "sum" in question:

                    result = df[column_name].sum()

                    st.success(
                        f"The total of '{column_name}' is {result}"
                    )

                else:

                    st.warning(
                        "Operation not recognized. Try highest, lowest, average, or total."
                    )

            except Exception:

                st.error(
                    f"Operation cannot be performed on '{column_name}'."
                )

        else:

            st.warning(
                "I couldn't understand the question."
            )