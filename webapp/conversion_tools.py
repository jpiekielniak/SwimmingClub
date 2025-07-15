import json
import statistics
from pyrg_funkcje import convert2range

# File path to JSON data containing world records
RECORDS_FILE_PATH = "webapp/records.json"

# Stroke name conversions (Polish → formatted style names)
STROKE_CONVERSIONS = {
    "kraul": "dowolnym",
    "grzbietowy": "grzbietowym",
    "klasyczny": "klasycznym",
    "motyl": "motylkowym",
    "zmienny": "zmiennym",
}

# Available race categories
COURSE_CATEGORIES = (
    "Mężczyźni, basen 50 m",
    "Kobiety, basen 50 m",
    "Mężczyźni, basen 25 m",
    "Kobiety, basen 25 m",
)


def get_world_records(distance: str, stroke: str):
    """
    Given a distance and stroke, return a list of four world record times
    corresponding to different gender and pool size categories.
    """
    with open(RECORDS_FILE_PATH, encoding="utf-8") as file:
        records = json.load(file)

    formatted_event = f"{distance[:-1]} m stylem {STROKE_CONVERSIONS[stroke]}"

    return [records[course][formatted_event] for course in COURSE_CATEGORIES]


def parse_time_string(time_str: str) -> int:
    """
    Converts a time string in the format 'M:SS,HH' or 'SS,HH' into hundredths of a second.
    """
    try:
        if ":" in time_str:
            minutes, rest = time_str.split(":")
            seconds, hundredths = rest.split(",")
        else:
            minutes = "0"
            seconds, hundredths = time_str.split(",")
        total_hundredths = (
            int(minutes) * 60 * 100 + int(seconds) * 100 + int(hundredths)
        )
        return total_hundredths
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")


def format_time_from_hundredths(hundredths: float) -> str:
    """
    Converts time in hundredths of a second back to the 'M:SS,HH' string format.
    """
    total_seconds = int(hundredths // 100)
    remaining_hundredths = int(hundredths % 100)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:0>2},{remaining_hundredths:0>2}"


def perform_time_conversions(times: list[str]) -> tuple[str, list[str], list[float]]:
    """
    Given a list of time strings, returns:
    - the average time as a string
    - the reversed list of original times
    - a scaled list of times (0 to 350 range)
    """
    time_in_hundredths = [parse_time_string(t) for t in times]

    average_time = statistics.mean(time_in_hundredths)
    average_time_str = format_time_from_hundredths(average_time)

    reversed_times = list(reversed(times))
    reversed_hundredths = list(reversed(time_in_hundredths))

    max_time = max(reversed_hundredths)
    scaled_times = [convert2range(t, 0, max_time, 0, 350) for t in reversed_hundredths]

    return average_time_str, reversed_times, scaled_times
