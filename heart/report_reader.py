"""Read a photo of a medical report and pull out the values the form asks for.

Tesseract turns the photo into plain text; the patterns below pick the eleven
clinical values out of that text. A field the report does not mention is left
out of the result, so the form renders it blank -- a guessed cholesterol would
produce a confident but meaningless prediction.

Needs the Tesseract engine installed separately (it is not a pip package):
    https://github.com/UB-Mannheim/tesseract/wiki
Set TESSERACT_CMD in .env if it is not on PATH.
"""
import os
import re

import pytesseract
from PIL import Image, ImageOps, UnidentifiedImageError

if os.environ.get("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]

MAX_IMAGE_BYTES = 5 * 1024 * 1024

# Values outside these ranges are OCR noise, not readings.
LIMITS = {
    "age": (1, 120),
    "resting_bp": (50, 300),
    "cholesterol": (50, 700),
    "max_hr": (40, 250),
    "oldpeak": (0.0, 10.0),
}

# Everything between the label and the number: units, colons, dots from the
# dotted leaders some labs print. Kept short so a number from the next row
# cannot be picked up.
GAP = r"[^0-9\n]{0,30}"


class ReportReadError(Exception):
    """Raised with a message that is safe to show the user."""


def _number(text, label_pattern, cast=int):
    match = re.search(label_pattern + GAP + r"(\d+(?:\.\d+)?)", text, re.I)
    if not match:
        return None
    try:
        return cast(match.group(1))
    except ValueError:
        return None


def _in_range(field, value):
    if value is None:
        return None
    low, high = LIMITS[field]
    return value if low <= value <= high else None


def _age(text):
    # "Age / Sex   58 Years / Male", "Age: 58", "58 Yrs"
    value = _number(text, r"\bage\b")
    if value is None:
        match = re.search(r"(\d{1,3})\s*(?:years?|yrs?)\b", text, re.I)
        value = int(match.group(1)) if match else None
    return _in_range("age", value)


def _sex(text):
    if re.search(r"\bfemale\b|\bsex\b[^a-z\n]{0,12}\bF\b", text, re.I):
        return "F"
    if re.search(r"\bmale\b|\bsex\b[^a-z\n]{0,12}\bM\b", text, re.I):
        return "M"
    return None


def _resting_bp(text):
    # "Blood Pressure (resting)  150 / 90 mmHg" -- the systolic number only.
    match = re.search(r"(?:blood\s*pressure|\bBP\b)" + GAP + r"(\d{2,3})\s*/\s*\d{2,3}", text, re.I)
    if match:
        return _in_range("resting_bp", int(match.group(1)))
    return _in_range("resting_bp", _number(text, r"systolic"))


def _cholesterol(text):
    # Total cholesterol only -- never HDL, LDL or triglycerides.
    for pattern in (r"total\s*cholesterol", r"cholesterol\s*[-,]?\s*total", r"\bT\.?C\.?\b"):
        value = _number(text, pattern)
        if value is not None:
            return _in_range("cholesterol", value)
    # A bare "Cholesterol" line, as long as it is not the HDL/LDL row.
    match = re.search(r"(?<![a-z])(?<!hdl )(?<!ldl )cholesterol" + GAP + r"(\d{2,3})", text, re.I)
    return _in_range("cholesterol", int(match.group(1))) if match else None


def _fasting_bs(text):
    # The form wants a flag, not the reading: 1 when fasting glucose is over 120.
    value = _number(
        text,
        r"(?:fasting\s*(?:blood\s*)?(?:sugar|glucose)|\bFBS\b|\bFBG\b)",
        float,
    )
    if value is not None and 20 <= value <= 600:
        return 1 if value > 120 else 0
    if re.search(r"\bdiabet(?:es|ic)\b", text, re.I):
        return 1
    return None


def _resting_ecg(text):
    if re.search(r"ST[\s-]*T\s*wave|ST[\s-]*T\s*change|\bST\s*abnormal", text, re.I):
        return "ST"
    if re.search(r"\bLVH\b|left\s*ventricular\s*hypertrophy", text, re.I):
        return "LVH"
    if re.search(r"(?:ECG|EKG)[^.\n]{0,40}\bnormal\b|\bnormal\b[^.\n]{0,20}(?:ECG|EKG)", text, re.I):
        return "Normal"
    return None


def _max_hr(text):
    for pattern in (r"max(?:imum)?\s*(?:heart\s*rate|HR)", r"peak\s*(?:heart\s*rate|HR)"):
        value = _number(text, pattern)
        if value is not None:
            return _in_range("max_hr", value)
    return None


def _exercise_angina(text):
    if re.search(r"\bno\b[^.\n]{0,30}(?:chest\s*pain|angina)|angina[^.\n]{0,15}\babsent\b", text, re.I):
        return "N"
    if re.search(
        r"(?:chest\s*(?:pain|tightness|discomfort)|angina)[^.\n]{0,40}"
        r"(?:exertion|exercise|effort|walking|stairs)"
        r"|exercise[\s-]*induced\s*angina"
        r"|(?:exertion|exercise)[^.\n]{0,40}(?:chest\s*(?:pain|tightness)|angina)",
        text, re.I,
    ):
        return "Y"
    return None


def _oldpeak(text):
    for pattern in (r"old\s*peak", r"ST\s*depression", r"ST\s*segment\s*depression"):
        value = _number(text, pattern, float)
        if value is not None:
            return _in_range("oldpeak", value)
    return None


SLOPE_WORDS = (
    ("Down", r"down\s*slop\w*|\bdownward\b|\bdown\b"),
    ("Up", r"up\s*slop\w*|\bupward\b|\brising\b|\bup\b"),
    ("Flat", r"\bflat\b|horizontal"),
)


def _st_slope(text):
    # Read only the line that talks about the slope, so "ST depression" above it
    # cannot be mistaken for it. That line often carries the reference value too
    # ("Downsloping ... Upsloping"), and labs print the result first, so take
    # whichever word appears earliest rather than a fixed Down/Up/Flat order.
    for line in text.splitlines():
        if not re.search(r"slope|ST\s*segment", line, re.I):
            continue
        hits = []
        for value, pattern in SLOPE_WORDS:
            match = re.search(pattern, line, re.I)
            if match:
                hits.append((match.start(), value))
        if hits:
            return min(hits)[1]
    return None


def _chest_pain_type(text):
    # Atypical must be tested before typical: one contains the other.
    if re.search(r"a[\s-]*typical\s*angina", text, re.I):
        return "ATA"
    if re.search(r"non[\s-]*anginal", text, re.I):
        return "NAP"
    if re.search(r"asymptomatic", text, re.I):
        return "ASY"
    if re.search(r"typical\s*angina", text, re.I):
        return "TA"
    return None


EXTRACTORS = {
    "age": _age,
    "sex": _sex,
    "chest_pain_type": _chest_pain_type,
    "resting_bp": _resting_bp,
    "cholesterol": _cholesterol,
    "fasting_bs": _fasting_bs,
    "resting_ecg": _resting_ecg,
    "max_hr": _max_hr,
    "exercise_angina": _exercise_angina,
    "oldpeak": _oldpeak,
    "st_slope": _st_slope,
}


def extract_fields(text):
    """Pick the form values out of already-OCR'd report text."""
    found = {}
    for name, extractor in EXTRACTORS.items():
        value = extractor(text)
        if value is not None:
            found[name] = value
    return found


def image_to_text(uploaded_file):
    """OCR the upload and return the plain text Tesseract read."""
    if uploaded_file.size > MAX_IMAGE_BYTES:
        raise ReportReadError("That image is larger than 5 MB. Please upload a smaller photo.")

    try:
        image = Image.open(uploaded_file)
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise ReportReadError(
            "That file is not a readable image. Please upload a JPG or PNG photo of your report."
        ) from exc

    # Grey, upright and reasonably large reads far better than a raw phone photo.
    image = ImageOps.exif_transpose(image).convert("L")
    if image.width < 1400:
        scale = 1400 / image.width
        image = image.resize((1400, int(image.height * scale)), Image.LANCZOS)

    try:
        return pytesseract.image_to_string(image)
    except pytesseract.TesseractNotFoundError as exc:
        raise ReportReadError(
            "The text reader (Tesseract) is not installed on this server, so report "
            "scanning is off. Please fill the form in by hand."
        ) from exc
    except pytesseract.TesseractError as exc:
        raise ReportReadError(
            "Could not read that image. Please try a clearer, straighter photo."
        ) from exc


def read_report(uploaded_file):
    """Return {form_field: value} for every value found on the report photo.

    Fields the report does not mention are left out, so the form renders them
    blank rather than carrying a guess into the model.
    """
    return extract_fields(image_to_text(uploaded_file))
