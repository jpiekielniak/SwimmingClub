import json
import statistics
from pathlib import Path

import pyrg_funkcje


DATA_FOLDER = "datatrainings/"
CHARTS_FOLDER = "charts/"
RECORDS_FILE = "records.json"

STROKE_CONVERSIONS = {
    "kraul": "dowolnym",
    "grzbietowy": "grzbietowym",
    "klasyczny": "klasycznym",
    "motyl": "motylkowym",
    "zmienny": "zmiennym",
}

COURSES = (
    "Mężczyźni, basen 50 m",
    "Kobiety, basen 50 m",
    "Mężczyźni, basen 25 m",
    "Kobiety, basen 25 m",
)


def event_key_from_filename(filename: str) -> str:
    """
    Convert swimmer file name into the dictionary key used in world record JSON.
    Example: "jan-13-100m-kraul.txt" → "100 m stylem dowolnym"
    """
    *_, distance, stroke = filename.removesuffix(".txt").split("-")
    return f"{distance[:-1]} m stylem {STROKE_CONVERSIONS[stroke]}"


def read_swim_file(filename: str):
    """
    Parses swimmer training file and returns swimmer info, raw times,
    converted times (in hundredths of seconds), and average time string.
    """
    swimmer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    with open(Path(DATA_FOLDER) / filename, encoding="utf-8") as file:
        line = file.readline().strip()
        times = line.split(";")

    converted_times = []
    for time_str in times:
        if ":" in time_str:
            minutes, rest = time_str.split(":")
            seconds, hundredths = rest.split(",")
        else:
            minutes = 0
            seconds, hundredths = time_str.split(",")
        total_hundredths = (
            int(minutes) * 60 * 100 + int(seconds) * 100 + int(hundredths)
        )
        converted_times.append(total_hundredths)

    avg_hundredths = statistics.mean(converted_times)
    minutes = int(avg_hundredths // 6000)
    seconds = int((avg_hundredths % 6000) // 100)
    hundredths = int(avg_hundredths % 100)
    avg_time_str = f"{minutes}:{seconds:0>2},{hundredths:0>2}"

    return swimmer, age, distance, stroke, times, avg_time_str, converted_times


def load_world_record_times(event_key: str) -> list[str]:
    """
    Returns the list of 4 world record times for a given event key.
    """
    with open(RECORDS_FILE, encoding="utf-8") as file:
        records = json.load(file)

    return [records[course][event_key] for course in COURSES]


def generate_bar_chart_html(
    swimmer: str,
    age: str,
    distance: str,
    stroke: str,
    times: list[str],
    average_time: str,
    converted_times: list[int],
    world_records: list[str],
) -> str:
    """
    Generates the full HTML content for the swimmer's bar chart.
    """
    reversed_times = list(reversed(times))
    reversed_converted = list(reversed(converted_times))
    max_time = max(reversed_converted)

    title = f"{swimmer} (under {age} y/o), {distance}, stroke: {stroke}"
    chart_bars = "\n".join(
        f"""
        <svg height="30" width="400">
            <rect height="30" width="{pyrg_funkcje.convert2range(value, 0, max_time, 0, 350)}"
                  style="fill:rgb(0,0,255);" />
        </svg>{time}<br />
        """
        for value, time in zip(reversed_converted, reversed_times)
    )

    record_display = (
        f"M: {world_records[0]} ({world_records[2]})<br />"
        f"K: {world_records[1]} ({world_records[3]})"
    )

    return f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="/static/webapp.css"/>
</head>
<body>
    <h2>{title}</h2>
    {chart_bars}
    <p>Average time: {average_time}</p>
    <p>{record_display}</p>
</body>
</html>"""


def produce_bar_chart(filename: str, output_folder: str = CHARTS_FOLDER) -> str:
    """
    Main interface: generates an HTML bar chart from swimmer file.
    Saves the HTML chart and returns the path to the saved file.
    """
    (swimmer, age, distance, stroke, times, average_time, converted_times) = (
        read_swim_file(filename)
    )

    event_key = event_key_from_filename(filename)
    world_records = load_world_record_times(event_key)

    html_content = generate_bar_chart_html(
        swimmer,
        age,
        distance,
        stroke,
        times,
        average_time,
        converted_times,
        world_records,
    )

    output_path = Path(output_folder) / f"{filename.removesuffix('.txt')}.html"
    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(html_content)

    return str(output_path)
