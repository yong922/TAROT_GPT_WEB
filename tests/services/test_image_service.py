import os
import pytest
from app.services.image_service import get_images_url

# 진짜 타로 카드 이미지 폴더 경로
STATIC_FOLDER = os.path.join(os.getcwd(), "app", "static", "imgs", "tarot_front_images")

def test_all_tarot_images_exist():
    """💚 모든 타로 카드 이미지와 default.png가 존재하는지 확인"""

    # 22장 메이저 아르카나 카드 리스트
    all_cards = [
        "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
        "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
        "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
        "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
        "Judgement", "The World"
    ]

    # 카드 이미지 존재 검사
    for card in all_cards:
        file_path = os.path.join(STATIC_FOLDER, f"{card}.png")
        assert os.path.exists(file_path), f"❌ 카드 이미지 {card}.png 가 존재하지 않습니다."

    # default 이미지 존재 검사
    default_path = os.path.join(STATIC_FOLDER, "default.png")
    assert os.path.exists(default_path), "❌ 기본 이미지 default.png 가 존재하지 않습니다."


def test_get_images_url_success():
    """💚 1. 카드 이미지가 전부 존재하는 경우"""
    cards = ["The Fool", "The Magician", "The High Priestess"]

    # 카드 이미지 파일이 실제로 존재하는지 확인 (안 존재하면 테스트 실패)
    for card in cards:
        file_path = os.path.join(STATIC_FOLDER, f"{card}.png")
        assert os.path.exists(file_path), f"테스트용 카드 이미지 {file_path}가 존재하지 않습니다."

    urls = get_images_url(cards)

    for card in cards:
        assert urls[card] == f"/static/imgs/tarot_front_images/{card}.png"


def test_get_images_url_failure():
    """💚 2. 카드 이미지가 전부 존재하지 않는 경우"""
    cards = ["NonExistentCard1", "NonExistentCard2", "NonExistentCard3"]

    urls = get_images_url(cards)

    for card in cards:
        assert urls[card] == "/static/imgs/tarot_front_images/default.png"


def test_get_images_url_mixed():
    """💚 3. 일부 카드는 존재하고 일부 카드는 존재하지 않는 경우"""
    cards = ["The Fool", "NonExistentCard1", "NonExistentCard2"]

    # "The Fool" 이미지는 실제로 존재하는지 검증
    file_path = os.path.join(STATIC_FOLDER, "The Fool.png")
    assert os.path.exists(file_path), f"테스트용 카드 이미지 {file_path}가 존재하지 않습니다."

    urls = get_images_url(cards)

    assert urls["The Fool"] == "/static/imgs/tarot_front_images/The Fool.png"
    assert urls["NonExistentCard1"] == "/static/imgs/tarot_front_images/default.png"
    assert urls["NonExistentCard2"] == "/static/imgs/tarot_front_images/default.png"
