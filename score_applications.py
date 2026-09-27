#!/usr/bin/env python3
"""Hitung risk_score aplikasi kredit berdasarkan aturan node Risk Score di n8n."""

import csv

INPUT_FILE = "test_applications.csv"
OUTPUT_FILE = "scored_applications.csv"


def parse_float(value):
    if value is None or str(value).strip() == "":
        return None
    return float(value)


def score_row(row):
    factors = []  # list of (label, points) for explanation generation
    data_flag = ""

    ext_source_2_raw = parse_float(row["EXT_SOURCE_2"])
    if ext_source_2_raw is None:
        ext_source_2 = 0.5
        data_flag = "EXT_SOURCE_2 kosong - wajib review manual"
    else:
        ext_source_2 = ext_source_2_raw

    score = (1 - ext_source_2) * 40
    if ext_source_2_raw is None:
        factors.append((f"skor eksternal (EXT_SOURCE_2) tidak tersedia sehingga dinilai netral-berisiko",
                         (1 - ext_source_2) * 40))
    else:
        factors.append((f"skor eksternal (EXT_SOURCE_2) rendah sebesar {ext_source_2_raw:.2f}",
                         (1 - ext_source_2) * 40))

    income = parse_float(row["AMT_INCOME_TOTAL"])
    credit = parse_float(row["AMT_CREDIT"])
    credit_to_income = credit / income if income else None

    if credit_to_income is not None and credit_to_income > 5:
        score += 15
        factors.append((f"rasio cicilan kredit terhadap pendapatan yang sangat tinggi ({credit_to_income:.1f}x)", 15))
    elif credit_to_income is not None and credit_to_income > 3:
        score += 8
        factors.append((f"rasio kredit terhadap pendapatan yang cukup tinggi ({credit_to_income:.1f}x)", 8))

    housing = (row["NAME_HOUSING_TYPE"] or "").strip()
    is_rented_or_with_parents = housing in ("Rented apartment", "With parents")
    if is_rented_or_with_parents:
        score += 15
        factors.append((f"status tempat tinggal yang belum mandiri ({housing.lower()})", 15))

    education = (row["NAME_EDUCATION_TYPE"] or "").strip()
    if education == "Lower secondary":
        score += 10
        factors.append(("tingkat pendidikan yang tergolong rendah (lower secondary)", 10))

    region_rating = parse_float(row["REGION_RATING_CLIENT"])
    if region_rating == 3:
        score += 10
        factors.append(("rating wilayah tempat tinggal yang buruk (rating 3)", 10))
    elif region_rating == 2:
        score += 5
        factors.append(("rating wilayah tempat tinggal yang cukup rendah (rating 2)", 5))

    years_employed = parse_float(row["YEARS_EMPLOYED"])
    if years_employed is not None and years_employed < 1:
        score += 10
        factors.append((f"masa kerja yang masih sangat singkat ({years_employed:g} tahun)", 10))

    if ext_source_2 < 0.3 and is_rented_or_with_parents:
        score += 10
        factors.append(("kombinasi skor eksternal rendah dengan status tempat tinggal yang belum stabil", 10))

    score = round(score)
    score = min(score, 100)

    if score > 70:
        category = "High"
    elif score >= 40:
        category = "Medium"
    else:
        category = "Low"

    needs_review = score > 70 or ext_source_2_raw is None

    return score, category, credit_to_income, data_flag, needs_review, factors


def build_explanation(factors, category):
    top_factors = sorted(factors, key=lambda f: f[1], reverse=True)[:2]
    factor_text = " dan ".join(f[0] for f in top_factors)
    level_word = {
        "High": "tinggi",
        "Medium": "menengah",
        "Low": "rendah",
    }[category]
    return (
        f"Profil risiko pemohon berada pada level {level_word}, "
        f"terutama dipengaruhi oleh {factor_text}."
    )


def main():
    with open(INPUT_FILE, newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        rows_out = []
        for row in reader:
            score, category, ratio, data_flag, needs_review, factors = score_row(row)
            explanation = build_explanation(factors, category)
            rows_out.append(
                {
                    "app_id": row["app_id"],
                    "risk_score": score,
                    "risk_category": category,
                    "credit_to_income": round(ratio, 2) if ratio is not None else "",
                    "data_flag": data_flag,
                    "needs_review": needs_review,
                    "explanation": explanation,
                }
            )

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f_out:
        fieldnames = [
            "app_id",
            "risk_score",
            "risk_category",
            "credit_to_income",
            "data_flag",
            "needs_review",
            "explanation",
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Selesai. {len(rows_out)} baris ditulis ke {OUTPUT_FILE}")
    return rows_out


if __name__ == "__main__":
    main()
