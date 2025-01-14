from langchain.tools import Tool


def get_current_datetime():
    """
    Returns the current date and time in a standardized format (YYYY-MM-DD).
    """
    return datetime.now().strftime("%Y-%m-%d")
datetime_tool = Tool(
    name="Current DateTime Fetcher",
    func=lambda _: get_current_datetime(),
    description="Fetches the current date in 'YYYY-MM-DD' format. Useful for resolving relative terms like 'next week' or 'tomorrow'."
)