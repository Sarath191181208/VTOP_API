from typing import Dict, List
import pandas as pd

def parse_single_subject_attendance(single_subject_attd_html: str) -> List[Dict[str, str]]:
    return pd.read_html(single_subject_attd_html)[0].drop(columns=["Sl.No"]).to_dict(orient="records") # type: ignore
