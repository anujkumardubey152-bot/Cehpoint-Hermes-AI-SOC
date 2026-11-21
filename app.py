import json
import sys
from pathlib import Path
from datetime import datetime

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from soc.investigation.engine import run_investigation
from soc.reporting.generator import generate_reports


st.set_page_config(
    page_title="Cehpoint AI SOC",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -1px;
}
.subtitle {
    color: #9299a6;
    font-size: 0.95rem;
}
div[data-testid="stMetric"] {
    background: rgba(128,128,128,0.08);
    border: 1px solid rgba(128,128,128,0.18);
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🛡️ Cehpoint AI Security Operations Centre</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Evidence-driven Security Investigation Platform</div>',
    unsafe_allow_html=True
)
st.divider()

st.warning(
    "Demonstration prototype. Uses synthetic laboratory logs "
    "and local mock threat intelligence. No production response "
    "actions are executed."
)

REQUIRED_FIELDS = [
    "alert_id", "alert_type", "timestamp", "account",
    "source_ip", "asset", "failed_login_count",
    "successful_login", "source"
]


def validate_alert(alert):
    if not isinstance(alert, dict):
        raise ValueError("Alert must be a JSON object.")

    missing = [field for field in REQUIRED_FIELDS if field not in alert]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))

    string_fields = [
        "alert_id", "alert_type", "timestamp", "account",
        "source_ip", "asset", "source"
    ]
    for field in string_fields:
        if not isinstance(alert[field], str) or not alert[field].strip():
            raise ValueError(f"{field} must be a non-empty string.")

    if alert["alert_type"] != "possible_account_compromise":
        raise ValueError("Unsupported alert type.")

    if type(alert["failed_login_count"]) is not int or alert["failed_login_count"] < 0:
        raise ValueError("failed_login_count must be a non-negative integer.")

    if type(alert["successful_login"]) is not bool:
        raise ValueError("successful_login must be true or false.")

    try:
        datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Invalid ISO timestamp.")

    return alert


st.sidebar.title("Investigation Console")
input_method = st.sidebar.radio(
    "Select alert input",
    ["Sample alert", "Upload JSON alert"]
)

alert = None

if input_method == "Sample alert":
    sample_path = ROOT / "data" / "alerts" / "account_compromise.json"
    if sample_path.exists():
        with sample_path.open("r", encoding="utf-8") as file:
            alert = json.load(file)
    else:
        st.error("Sample alert file not found.")
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload security alert",
        type=["json"]
    )
    if uploaded_file:
        try:
            alert = json.loads(uploaded_file.getvalue().decode("utf-8"))
        except Exception as error:
            st.sidebar.error(f"Invalid JSON: {error}")


if alert is not None:
    try:
        validate_alert(alert)

        st.subheader("Security Alert")
        col1, col2, col3 = st.columns(3)
        col1.metric("Alert ID", alert["alert_id"])
        col2.metric("Failed Logins", alert["failed_login_count"])
        col3.metric(
            "Successful Login",
            "Yes" if alert["successful_login"] else "No"
        )

        with st.expander("View Alert JSON"):
            st.json(alert)

        if st.button(
            "Run Security Investigation",
            type="primary",
            use_container_width=True
        ):
            with st.spinner("Investigating alert using approved SOC tools..."):
                investigation = run_investigation(alert)
                report_paths = generate_reports(investigation)
                st.session_state["investigation"] = investigation
                st.session_state["report_paths"] = report_paths

            st.success("Investigation completed successfully.")

    except Exception as error:
        st.error(f"Alert processing error: {error}")


investigation = st.session_state.get("investigation")

if investigation:
    assessment = investigation.get("assessment", {})

    st.divider()
    st.header("Investigation Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Severity", assessment.get("severity", "Unknown"))
    col2.metric("Confidence", assessment.get("confidence", "Unknown"))
    col3.metric("Status", investigation.get("status", "Unknown"))

    st.caption("Incident ID: " + investigation.get("incident_id", "Unknown"))

    st.subheader("Affected Entities")
    entities = investigation.get("affected_entities", {})
    col1, col2, col3 = st.columns(3)
    col1.write("**Account**")
    col1.write(entities.get("account", "Unknown"))
    col2.write("**Asset**")
    col2.write(entities.get("asset", "Unknown"))
    col3.write("**Source IP**")
    col3.write(entities.get("source_ip", "Unknown"))

    st.subheader("Severity Assessment")
    st.write(assessment.get("severity_reason", "Not available."))

    st.subheader("Confidence Assessment")
    st.write(assessment.get("confidence_reason", "Not available."))

    st.subheader("Analyst Conclusion")
    st.info(assessment.get("conclusion", "No conclusion available."))

    st.subheader("Investigation Timeline")
    timeline = investigation.get("timeline", [])
    if timeline:
        st.dataframe(timeline, use_container_width=True, hide_index=True)
    else:
        st.info("No timeline events available.")

    st.subheader("Evidence Gaps")
    gaps = investigation.get("evidence_gaps", [])
    if gaps:
        for gap in gaps:
            st.warning(gap)
    else:
        st.success("No evidence gaps recorded.")

    st.subheader("Approved SOC Tool Results")
    for tool_name, result in investigation.get("tool_results", {}).items():
        with st.expander(tool_name):
            st.json(result)

    st.subheader("Recommended Analyst Actions")
    for recommendation in investigation.get("recommendations", []):
        st.markdown(
            f"**Priority {recommendation.get('priority', 'N/A')}** — "
            f"{recommendation.get('action', 'Unspecified')}"
        )
        st.write(
            "Expected impact:",
            recommendation.get("expected_impact", "Not specified")
        )
        st.write(
            "Human approval required:",
            "Yes" if recommendation.get("approval_required") else "No"
        )
        st.divider()

    st.subheader("Incident Reports")
    report_paths = st.session_state.get("report_paths", {})
    json_path = Path(report_paths.get("json_report", ""))
    md_path = Path(report_paths.get("markdown_report", ""))

    col1, col2 = st.columns(2)
    if json_path.is_file():
        col1.download_button(
            "Download JSON Report",
            data=json_path.read_bytes(),
            file_name="incident_report.json",
            mime="application/json",
            use_container_width=True
        )
    if md_path.is_file():
        col2.download_button(
            "Download Markdown Report",
            data=md_path.read_bytes(),
            file_name="incident_report.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.divider()
    st.subheader("Human Approval & Safety")
    st.success(
        "No production response action was executed. "
        "Disruptive actions require human approval."
    )
    st.caption(
        "This dashboard does not execute account blocking, host isolation, "
        "session revocation or deletion."
    )
    st.caption(
        "Hermes runtime integration remains provisional and is not "
        "represented as connected."
    )
else:
    st.info(
        "Select a sample alert or upload a JSON alert, "
        "then click Run Security Investigation."
    )

st.divider()
st.caption(
    "Cehpoint AI SOC | Synthetic Dataset | Local Mock Intelligence | "
    "Human-in-the-Loop Safety"
)
