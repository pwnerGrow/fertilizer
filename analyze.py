class FertilizerComposition:
    def __init__(self):
        self.constants = {
            "P": 0.72,  # Phosphorus conversion factor
            "K": 1.25,  # Potassium conversion factor
            "Ca": 0.19, # Calcium conversion factor
            "Mg": 0.14, # Magnesium conversion factor
            "S": 0.31,  # Sulfur conversion factor
            "Micronutrients": 0.005  # Micronutrients percentage
        }

    def calculate_ppm(self, target_ec, ratio):
        # Split ratio A:B:C
        ratio_a, ratio_b, ratio_c = map(float, ratio.split(":"))
        total_ratio = ratio_a + ratio_b + ratio_c

        if total_ratio == 0:
            raise ValueError("Total ratio cannot be zero")

        # Base PPM from EC
        base_ppm = target_ec * 1000

        # Calculate individual nutrients
        ppm_n = (ratio_a / total_ratio) * base_ppm
        ppm_p = (ratio_b / total_ratio) * base_ppm * self.constants["P"]
        ppm_k = (ratio_c / total_ratio) * base_ppm * self.constants["K"]
        ppm_ca = (ratio_a / total_ratio) * base_ppm * self.constants["Ca"]
        ppm_mg = (ratio_b / total_ratio) * base_ppm * self.constants["Mg"]
        ppm_s = (ratio_c / total_ratio) * base_ppm * self.constants["S"]
        micronutrients = base_ppm * self.constants["Micronutrients"]

        return {
            "N (ppm)": ppm_n,
            "P (ppm)": ppm_p,
            "K (ppm)": ppm_k,
            "Ca (ppm)": ppm_ca,
            "Mg (ppm)": ppm_mg,
            "S (ppm)": ppm_s,
            "Micronutrients (ppm)": micronutrients
        }


class FeedChartAnalyzer:
    def __init__(self, feed_chart, composition):
        self.feed_chart = feed_chart
        self.composition = composition

    def analyze(self):
        results = []
        for stage in self.feed_chart:
            try:
                ppm = self.composition.calculate_ppm(stage["Target EC"], stage["Ratio"])
                results.append({
                    "Stage": stage["Stage"],
                    "Days": stage["Days"],
                    "Target EC": stage["Target EC"],
                    "Ratio": stage["Ratio"],
                    **ppm,
                    "HOCL (mL/L)": stage["HOCL"],
                    "DLI (mol/m²/day)": stage["DLI"]
                })
            except ValueError as e:
                print(f"Error in stage {stage['Stage']}: {e}")
                continue
        return results


# Example feed chart (Burn and Turn Feed Chart)
feed_chart = [
    {"Stage": "Veg Days", "Days": "1–10", "Target EC": 2.5, "Ratio": "2:2:1", "HOCL": 1.33, "DLI": 20.00},
    {"Stage": "Early Bloom", "Days": "1–10", "Target EC": 2.8, "Ratio": "1:2:2", "HOCL": 1.33, "DLI": 30.00},
    {"Stage": "Bulking P1", "Days": "11–20", "Target EC": 3.0, "Ratio": "0.5:2:2.5", "HOCL": 1.33, "DLI": 40.00},
    {"Stage": "Bulking P2", "Days": "21–42", "Target EC": 3.0, "Ratio": "0.3:1.5:2.5", "HOCL": 1.33, "DLI": 40.00},
    {"Stage": "Late Bloom P1", "Days": "43–49", "Target EC": 1.8, "Ratio": "0.3:1.5:3", "HOCL": 1.33, "DLI": 40.00},
    {"Stage": "Late Bloom P2", "Days": "50–53", "Target EC": 0.8, "Ratio": "0.2:1.2:2.8", "HOCL": 1.33, "DLI": 30.00},
    {"Stage": "Flush", "Days": "54–56", "Target EC": 0.2, "Ratio": "0:0:0", "HOCL": 5.33, "DLI": 20.00}
]

# Initialize composition and analyzer
composition = FertilizerComposition()
analyzer = FeedChartAnalyzer(feed_chart, composition)

# Analyze feed chart and print results
results = analyzer.analyze()

# Display results
import pandas as pd
df = pd.DataFrame(results)
print(df)

# Save to a file if needed
#df.to_csv("feed_chart_analysis.csv", index=False)