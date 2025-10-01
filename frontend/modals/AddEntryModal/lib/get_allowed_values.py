from backend.utils.logger import logging

logger = logging.getLogger("frontend")

# QwQ мощно конечно, но..
def get_allowed_values(table: str, name: str) -> list[str]:
    if table == "sensors":
        if name == "type":
            return ["temperature", "vibration", "pressure", "noise"]
    if table == "equipment":
        if name == "status":
            return ["working", "maintenance", "broken"]
        if name == "unit":
            return []
    if table == "failure_predictions":
        if name == "risk_level":
            return ["low", "medium", "high"]
    if table == "maintenance_logs":
        if name == "type":
            return ["planned", "emergency", "predictive"]
    logger.error(
        f"Couldn't match input type with its allowed values list. Defaulting to empty list. (name: '{name}', table: '{table}')"
    )
    return []
