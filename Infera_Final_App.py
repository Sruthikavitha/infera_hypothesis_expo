
import matplotlib.pyplot as plt
import streamlit as st
from scipy import stats
import statistics

st.title("INFERA: Hypothesis Testing Made Simple")

# Sidebar menu
test_choice = st.sidebar.radio(
    "Select Test:",
    (
        "Guide me (I don't know)",
        "One-sample t-test",
        "Two-sample F-test",
        "One-sample t-test (manual stats)",
        "Z-test for proportion (large sample)",
        "Z-test for mean (large sample)"
    )
)

# Guide me section
if test_choice == "Guide me (I don't know)":
    st.header("🧭 Let’s Help You Choose the Right Test")
    data_type = st.radio("What type of data are you working with?", ["Numerical data", "Proportions (Success/Failure)"])
    if data_type == "Numerical data":
        sample_count = st.radio("How many samples do you have?", ["One sample", "Two samples"])
        if sample_count == "One sample":
            data_detail = st.radio("Do you have full data or just summary (mean, std)?", ["Full data", "Summary only"])
            if data_detail == "Full data":
                st.info("👉 Use: One-sample t-test")
            else:
                st.info("👉 Use: One-sample t-test (manual stats)")
        else:
            st.info("👉 Use: Two-sample F-test")
    else:
        prop_test = st.radio("What do you want to test?", ["Single proportion", "Compare two proportions"])
        if prop_test == "Single proportion":
            st.info("👉 Use: Z-test for proportion (large sample)")
        else:
            st.warning("⚠️ Two-proportion Z-test not added yet")

# One-sample t-test
elif test_choice == "One-sample t-test":
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

# Manual t-test
elif test_choice == "One-sample t-test (manual stats)":
    st.header("🟢 One-sample t-Test (Manual Summary Statistics)")
    sample_mean = st.number_input("Enter sample mean (x̄):")
    sample_std = st.number_input("Enter sample standard deviation (s or σ):")
    sample_size = st.number_input("Enter sample size (n):", min_value=1, step=1)
    hypothesized_mean = st.number_input("Enter hypothesized population mean (μ₀):", value=0.0)
    alpha = st.slider("Select Significance Level (α):", 0.01, 0.10, 0.05, key='manual_alpha')
    if st.button("Run Manual t-Test"):
        try:
            t_stat = (sample_mean - hypothesized_mean) / (sample_std / (sample_size ** 0.5))
            df = sample_size - 1
            p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
            t_critical = stats.t.ppf(1 - alpha/2, df)
            margin = t_critical * (sample_std / (sample_size ** 0.5))
            lower = sample_mean - margin
            upper = sample_mean + margin
            st.subheader("Result:")
            st.write(f"**Sample Mean (x̄):** {sample_mean}")
            st.write(f"**Hypothesized Mean (μ₀):** {hypothesized_mean}")
            st.write(f"**t-statistic:** {t_stat:.4f}")
            st.write(f"**Degrees of Freedom:** {df}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.write(f"**Critical t-value (two-tailed):** ±{t_critical:.4f}")
            if abs(t_stat) < t_critical:
                st.success("✅ Fail to Reject Null Hypothesis")
            else:
                st.error("❌ Reject Null Hypothesis")
            st.subheader("📏 Confidence Interval:")
            st.write(f"**{100*(1-alpha):.0f}% CI:** ({lower:.4f}, {upper:.4f})")
        except Exception as e:
            st.error(f"Error: {e}")

# F-test
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
                    st.error("Reject Null Hypothesis ❌")
                else:
                    st.success("Fail to Reject Null Hypothesis ✅")
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

# Z-test for proportion
elif test_choice == "Z-test for proportion (large sample)":
    st.header("🧪 Z-test for Proportion (Large Sample)")
    x = st.number_input("Enter number of successes (x):", min_value=0)
    n = st.number_input("Enter sample size (n):", min_value=1)
    p0 = st.number_input("Enter hypothesized population proportion (p₀):", min_value=0.0, max_value=1.0, value=0.5)
    alpha = st.slider("Select Significance Level (α):", 0.01, 0.10, 0.05, key='z_alpha')
    if st.button("Run Z-test"):
        try:
            p_hat = x / n
            z_stat = (p_hat - p0) / ((p0 * (1 - p0) / n) ** 0.5)
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            st.subheader("Result:")
            st.write(f"**Sample proportion (p̂):** {p_hat:.4f}")
            st.write(f"**Z-statistic:** {z_stat:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            if p_value < alpha:
                st.error("Reject Null Hypothesis ❌")
            else:
                st.success("Fail to Reject Null Hypothesis ✅")
        except Exception as e:
            st.error(f"Error: {e}")

# Z-test for population mean
elif test_choice == "Z-test for mean (large sample)":
    st.header("📏 Z-test for Population Mean (Large Sample)")
    sample_mean = st.number_input("Enter sample mean (x̄):")
    std_dev = st.number_input("Enter population standard deviation (σ):")
    sample_size = st.number_input("Enter sample size (n):", min_value=1, step=1)
    hypothesized_mean = st.number_input("Enter hypothesized population mean (μ₀):", value=0.0)
    alpha = st.slider("Select Significance Level (α):", 0.01, 0.10, 0.05, key='zmean_alpha')
    if st.button("Run Z-test for Mean"):
        try:
            z_stat = (sample_mean - hypothesized_mean) / (std_dev / (sample_size ** 0.5))
            p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
            z_critical = stats.norm.ppf(1 - alpha / 2)
            margin = z_critical * (std_dev / (sample_size ** 0.5))
            lower = sample_mean - margin
            upper = sample_mean + margin
            st.subheader("Result:")
            st.write(f"**Z-statistic:** {z_stat:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.write(f"**Critical Z (two-tailed):** ±{z_critical:.2f}")
            if abs(z_stat) < z_critical:
                st.success("✅ Fail to Reject Null Hypothesis")
            else:
                st.error("❌ Reject Null Hypothesis")
            st.subheader("📏 Confidence Interval:")
            st.write(f"**{100*(1-alpha):.0f}% CI:** ({lower:.4f}, {upper:.4f})")
        except Exception as e:
            st.error(f"Error: {e}")
