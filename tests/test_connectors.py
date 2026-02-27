import pytest

from backend.app.connectors import (
    ottoneu_connector,
    statcast_connector,
    projections_connector,
    news_connector,
)


def test_parse_csv() -> None:
    csv_text = """player_name,position,salary,mlbam_id\nMike Trout,OF,45,545361\nShohei Ohtani,UT,60,673548"""
    parsed = ottoneu_connector.parse_csv(csv_text)
    assert parsed["player_name"] == ["Mike Trout", "Shohei Ohtani"]
    assert parsed["position"] == ["OF", "UT"]
    assert parsed["salary"] == ["45", "60"]


def test_statcast_connector_stub() -> None:
    data = statcast_connector.fetch_statcast_leaderboard()
    assert isinstance(data, list)
    assert data
    sample = data[0]
    assert "mlbam_id" in sample
    assert "barrel_rate" in sample


def test_projections_connector_stub() -> None:
    data = projections_connector.fetch_ros_projections()
    assert isinstance(data, list)
    assert data[0].get("mlbam_id") is not None
    assert data[0].get("proj_points") is not None


def test_news_connector_stub() -> None:
    items = news_connector.fetch_player_news()
    assert isinstance(items, list)
    sample = items[0]
    assert "mlbam_id" in sample
    assert "headline" in sample
    assert "timestamp" in sample