import os

def get_images_url(cards):
    """
    ✅ 타로 카드 이미지 URL을 생성하는 함수
    """
    base_url = "/static/imgs/tarot_front_images/"
    static_folder = os.path.join(os.getcwd(), "app", "static", "imgs", "tarot_front_images") 
    default_img = "/static/imgs/tarot_front_images/default.png"

    return {
        card: f"{base_url}{card}.png"
        if os.path.exists(os.path.join(static_folder, f"{card}.png"))
        else default_img
        for card in cards
    }