"""Baking Pan Sizing Notes — free educational Streamlit app."""
from __future__ import annotations

import math
import streamlit as st

st.set_page_config(
    page_title="Baking Pan Size & Recipe Scaling Guide",
    page_icon="🍰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stAppViewContainer"] { background: #faf9f5; color:#183037; }
[data-testid="stHeader"] { background:rgba(250,249,245,.9); }
.block-container {max-width:1120px;padding-top:2rem;padding-bottom:5rem;}
h1,h2,h3 {font-family:'Libre Baskerville',Georgia,serif !important; color:#19343a;}
.hero {background:linear-gradient(112deg,#e7f2ee 0%,#f5f2ea 100%);border:1px solid #dde8e3;border-radius:20px;padding:36px 38px 32px;margin-bottom:28px;}
.eyebrow {color:#ab562d;font-weight:800;font-size:.74rem;letter-spacing:.18em;text-transform:uppercase;margin-bottom:1.2rem;}
.hero h1 {font-size:clamp(1.85rem,3.8vw,3.05rem);line-height:1.21;letter-spacing:-.035em;margin:.2rem 0 1rem;}
.hero p {font-size:1.09rem;line-height:1.7;color:#415a5c;max-width:790px;margin:0;}
.guide-note {background:white;padding:21px 23px;border:1px solid #e4e8e5;border-radius:16px; margin:10px 0 22px;line-height:1.75;}
.guide-note h3 {font-size:1.05rem;margin:0 0 .6rem;}
.guide-note p {margin:0;color:#52666a;}
.section-label {font-size:.76rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#ad633b;margin:20px 0 8px;}
.resource {background:#fff;border:1px solid #d7e5df;padding:25px 27px;border-radius:18px;margin:22px 0;line-height:1.85;}
.resource a {color:#086d76;font-weight:700;text-decoration:underline;text-underline-offset:3px;}
.small {font-size:.88rem;color:#58696b;}
hr {border-color:#e7ebe8;}
[data-testid="stMetric"] {background:#fff;border-radius:14px;border:1px solid #e0e8e4;padding:15px;}
[data-testid="stMetricLabel"] {font-weight:650;color:#526267;}
[data-testid="stMetricValue"] {color:#1b5055;}
[data-testid="stAlert"] {border-radius:12px;}
[data-testid="stNumberInput"] input {background:white;}
footer {visibility:hidden;}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <div class="eyebrow">Practical baking notes · Pan conversions</div>
  <h1>How to Adjust a Baking Recipe for a Different Pan Size</h1>
  <p>A practical guide for home bakers: compare round, square, and rectangular pans, estimate a starting batch multiplier, and understand when the arithmetic is not enough.</p>
</div>
""",
    unsafe_allow_html=True,
)

main, sidebar = st.columns([3.1, 1.1], gap="large")

with sidebar:
    st.markdown(
        """<div class="guide-note"><h3>In this guide</h3>
        <p>01 · The pan area method<br>02 · Interactive recipe scaler<br>03 · Example pan swaps<br>04 · When to adjust bake time<br>05 · Ingredient measuring resources<br>06 · FAQs & sources</p></div>""",
        unsafe_allow_html=True,
    )
    st.info("Tip: Keep batter depth similar when using an area-based multiplier. Check the pan's safe fill level.")

with main:
    st.markdown("## The pan area method")
    st.write(
        "If you substitute one baking pan for another, simply swapping the pan without changing "
        "the recipe can make the cake thicker or thinner. For pans of similar depth and shape behavior, "
        "a useful starting estimate is the ratio of their base areas: **new area ÷ original area**. "
        "This works best for straightforward batters, bars, and brownies; it is not a universal rule."
    )
    st.markdown(
        '<div class="section-label">Interactive tool</div>', unsafe_allow_html=True
    )
    st.markdown("## Baking Pan & Recipe Scaling Calculator")
    st.write("Choose your original pan and target pan. Both sets of dimensions use the same unit.")

    units = st.radio("Measurement units", ["Inches", "Centimeters"], horizontal=True)
    unit_symbol = "in" if units == "Inches" else "cm"
    shape_options = ["Round", "Square", "Rectangle"]
    a, b = st.columns(2, gap="medium")

    def dimensions(container, key: str, heading: str, default_shape: str):
        with container:
            st.markdown(f"### {heading}")
            shape = st.selectbox("Pan shape", shape_options, index=shape_options.index(default_shape), key=f"{key}_shape")
            default = 9.0 if units == "Inches" else 23.0
            if shape == "Round":
                diameter = st.number_input(f"Diameter ({unit_symbol})", min_value=1.0, max_value=200.0,
                                           value=default, step=0.5, key=f"{key}_diam")
                area = math.pi * (diameter / 2) ** 2
                description = f"{diameter:g} {unit_symbol} round"
            elif shape == "Square":
                side = st.number_input(f"Side length ({unit_symbol})", min_value=1.0, max_value=200.0,
                                       value=default if key == "original" else (8.0 if units == "Inches" else 20.0),
                                       step=0.5, key=f"{key}_side")
                area = side ** 2
                description = f"{side:g} × {side:g} {unit_symbol} square"
            else:
                length = st.number_input(f"Length ({unit_symbol})", min_value=1.0, max_value=200.0,
                                         value=13.0 if units == "Inches" else 33.0,
                                         step=0.5, key=f"{key}_length")
                width = st.number_input(f"Width ({unit_symbol})", min_value=1.0, max_value=200.0,
                                        value=9.0 if units == "Inches" else 23.0,
                                        step=0.5, key=f"{key}_width")
                area = length * width
                description = f"{length:g} × {width:g} {unit_symbol} rectangle"
            return area, description

    original_area, original_desc = dimensions(a, "original", "Original recipe pan", "Round")
    new_area, new_desc = dimensions(b, "target", "Pan you want to use", "Square")
    factor = new_area / original_area
    st.markdown("### Your starting estimate")
    m1, m2, m3 = st.columns(3)
    m1.metric("Original pan area", f"{original_area:,.1f} {unit_symbol}²")
    m2.metric("Target pan area", f"{new_area:,.1f} {unit_symbol}²")
    m3.metric("Recipe multiplier", f"{factor:.2f}×")

    if .9 <= factor <= 1.1:
        st.success("These pans have similar base areas. The original recipe quantity may be a good starting point, provided depth and fill levels are appropriate.")
    elif factor < 1:
        st.info(f"The target pan is smaller. Start with approximately **{factor * 100:.0f}% of the original recipe**, if batter depth can stay comparable.")
    else:
        st.info(f"The target pan is larger. Start with approximately **{factor:.2f} times the original recipe**, if batter depth can stay comparable.")

    st.markdown("#### Optional: scale your ingredient quantities")
    ingredient_amount = st.number_input("One ingredient amount from your original recipe", min_value=0.0,
                                        value=200.0, step=10.0, format="%.1f")
    ingredient_unit = st.selectbox("Ingredient unit", ["grams", "milliliters", "cups", "tablespoons", "teaspoons", "ounces"], index=0)
    st.markdown(f"**Scaled ingredient amount:** {ingredient_amount * factor:,.1f} {ingredient_unit}  ")
    st.caption("For eggs, leavening, very small quantities, or large scaling changes, use recipe-specific judgment instead of mechanical rounding.")

    st.markdown("## Example swaps")
    st.markdown(
        """
| Original pan | Target pan | Approx. area ratio |
|---|---|---:|
| 9-inch round | 8-inch square | 1.01× |
| 9-inch square | 9 × 13-inch rectangle | 1.44× |
| 8-inch round | 9-inch round | 1.27× |
| 9 × 13-inch rectangle | 8-inch square | 0.55× |
"""
    )
    st.caption("Values compare base areas only and are rounded. Pan depth, batter characteristics, and oven conditions still matter.")

    st.markdown("## When a different pan changes the bake")
    st.write(
        "A thicker batter layer often takes longer to cook through; a thinner layer may finish sooner. "
        "Keep an eye on doneness and avoid filling the pan too high. Pans with center tubes, specialty molds, "
        "and delicate recipes such as soufflés or cheesecakes may not respond well to a simple area multiplier."
    )

    st.markdown(
        """
<div class="resource">
  <div class="eyebrow">Related baking resource</div>
  <h3>Need help measuring the ingredients too?</h3>
  <p>Once you've scaled the recipe, you may need to convert individual ingredients between grams and cups. Since flour, sugar, and cocoa have different densities, use an ingredient-specific reference such as this <a href="https://gramstocupsconverter.net/" target="_blank" rel="noopener noreferrer">baking ingredient conversion guide</a>.</p>
  <p class="small">The link opens an independent ingredient measurement resource.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("## Questions bakers ask")
    with st.expander("Can I use an 8-inch square pan instead of a 9-inch round pan?"):
        st.write("Their base areas are nearly identical (64 versus approximately 63.6 square inches). Check pan depth, batter fill, and doneness before treating them as interchangeable.")
    with st.expander("Do I also multiply baking time by the area factor?"):
        st.write("No. The area factor is a starting estimate for ingredient quantity, not baking time. Check your recipe's visual doneness cues and start checking early when changing pan formats.")
    with st.expander("Does this calculator handle Bundt, loaf, or tube pans?"):
        st.write("No. Those pans depend strongly on capacity, geometry, and depth; use a tested recipe or pan-specific volume guidance instead.")
    with st.expander("Can I scale very large or very small batches?"):
        st.write("You can compute a mathematical estimate, but ingredient behavior and baking conditions may change. Test carefully, particularly for leavening, eggs, and specialty batters.")

    st.markdown("## Further reading")
    st.markdown(
        "- [Why the size of your baking pan matters so much — King Arthur Baking](https://www.kingarthurbaking.com/blog/2025/08/18/baking-pan-size)  \n"
        "- [The essential alternative baking pan sizes — King Arthur Baking](https://www.kingarthurbaking.com/blog/2019/04/23/the-essential-alternative-baking-pan-sizes)"
    )
    st.caption("Educational tool. Area-based scaling gives an estimate rather than a guarantee of baking performance.")
