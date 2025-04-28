
import matplotlib.pyplot as plt

import streamlit as st
from scipy import stats
import statistics

st.title("INFERA:Hypothesis Testing Made Simple")

# Sidebar menu
test_choice = st.sidebar.radio(
    "Select Test:",
    ("One-sample t-test", "Two-sample F-test")
)



if test_choice == "One-sample t-test":
    st.header("🔵 One-sample t-Test")

    data_input = st.text_area("Enter sample data (comma separated):")
    hypothesized_mean = st.number_input("Enter hypothesized population mean:", value=0.0)
    alpha = st.slider("Select Significance Level (α):", 0.01, 0.10, 0.05)

    if st.button("Run t-Test"):
        if data_input:
            try:
                sample = list(map(float, data_input.split(',')))
                t_stat, p_value = stats.ttest_1samp(sample, hypothesized_mean)

                st.subheader("Result:")
                st.write(f"**t-statistic:** {t_stat:.4f}")
                st.write(f"**p-value:** {p_value:.4f}")

                if p_value < alpha:
                    st.error("Reject Null Hypothesis ❌")
                else:
                    st.success("Fail to Reject Null Hypothesis ✅")                
                # Plot Histogram for One-sample t-test
                st.subheader("📊 Histogram of Sample Data")

                fig, ax = plt.subplots()
                ax.hist(sample, bins=10, edgecolor='black', color='skyblue')
                ax.set_xlabel('Sample Value')
                ax.set_ylabel('Frequency')
                ax.set_title('Histogram of Sample Data')
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please input sample data!")





elif test_choice == "Two-sample F-test":
    st.header("🟠 Two-sample F-Test")

    sample1_input = st.text_area("Enter Sample 1 data (comma separated):")
    sample2_input = st.text_area("Enter Sample 2 data (comma separated):")
    alpha = st.slider("Select Significance Level (α):", 0.01, 0.10, 0.05, key='f_alpha')

    if st.button("Run F-Test"):
        if sample1_input and sample2_input:
            try:
                sample1 = list(map(float, sample1_input.split(',')))
                sample2 = list(map(float, sample2_input.split(',')))

                var1 = statistics.variance(sample1)
                var2 = statistics.variance(sample2)

                # Ensure larger variance is numerator
                if var1 < var2:
                    var1, var2 = var2, var1
                    sample1, sample2 = sample2, sample1

                f_stat = var1 / var2
                dfn = len(sample1) - 1
                dfd = len(sample2) - 1

                p_value = 1 - stats.f.cdf(f_stat, dfn, dfd)

                st.subheader("Result:")
                st.write(f"**F-statistic:** {f_stat:.4f}")
                st.write(f"**Degrees of Freedom:** ({dfn}, {dfd})")
                st.write(f"**p-value:** {p_value:.4f}")

                if p_value < alpha:
                    st.error("Reject Null Hypothesis ❌ (Variances are significantly different)")
                else:
                    st.success("Fail to Reject Null Hypothesis ✅ (No significant difference)")
                # 📊 Plot Histograms for Two-sample F-test
                st.subheader("📊 Histograms of Both Samples")

                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

                ax1.hist(sample1, bins=10, edgecolor='black', color='lightgreen')
                ax1.set_title('Sample 1 Histogram')
                ax1.set_xlabel('Value')
                ax1.set_ylabel('Frequency')

                ax2.hist(sample2, bins=10, edgecolor='black', color='lightcoral')
                ax2.set_title('Sample 2 Histogram')
                ax2.set_xlabel('Value')
                ax2.set_ylabel('Frequency')

                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please input both samples!")
