import os
import random
import asyncio
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from app.data import tarot_meaning, templates

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

TAROT_CARD_MEANINGS = tarot_meaning.TAROT_CARD_MEANINGS

class TarotReader:
    def __init__(self):
        self.conversation_state = {
            "is_card_drawn": False,
            "cards": None,
            "topic": None,
            "card_keywords": None,
        }
        
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        # 대화 히스토리 저장
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            input_key="text",
            return_messages=True
        )

        # 템플릿 로드
        self.base_template = templates.base_template
        self.first_reading_prompt = templates.first_reading_prompt
        self.follow_up_prompt = templates.follow_up_prompt

    def create_prompt(self, is_first_reading: bool = False):
        """
        대화 프롬프트를 생성하는 함수
        - 첫 리딩이면 first_reading_prompt 사용
        - 후속 질문이면 follow_up_prompt 사용
        """
        system_template = self.base_template + (self.first_reading_prompt if is_first_reading else self.follow_up_prompt)

        return ChatPromptTemplate(
            input_variables=["text", "chat_history", "cards", "topic", "card_keywords", "prompt_type"],
            messages=[
                SystemMessagePromptTemplate.from_template(system_template),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{text}")
            ]
        )

    def draw_tarot_cards(self):
        """
        22장의 메이저 아르카나 타로 카드 중 3장을 무작위로 뽑기
        """
        cards = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant",
            "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man",
            "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
        ]
        return random.sample(cards, 3)

    def card_keywords(self, cards):
        """
        해당 카드의 의미 데이터 반환
        """
        return {card: TAROT_CARD_MEANINGS[card] for card in cards}

    def process_query(self, text, topic=None):
        """
        사용자의 질문을 처리하고 타로 카드를 해석하여 응답을 반환
        - 첫 리딩이면 카드를 뽑고 카드 키워드 저장
        - 후속 질문이면 기존 카드 정보를 유지하면서 답변 제공
        """
        if not self.conversation_state["is_card_drawn"]:
            # 첫 번째 리딩: 카드 뽑기
            cards = self.draw_tarot_cards()
            self.conversation_state.update({
                "cards": ', '.join(cards),
                "topic": topic,
                "is_card_drawn": True,
                "card_keywords": self.card_keywords(cards),
            })
            
            prompt_template = self.create_prompt(is_first_reading=True)
        else:
            # 후속 질문
            prompt_template = self.create_prompt(is_first_reading=False)

        # 모델 실행
        chain = LLMChain(
            llm=self.model,
            prompt=prompt_template,
            memory=self.memory,
            verbose=False
        )

        response = chain.run(
            text=text,
            topic=topic,
            chat_history=self.memory.chat_memory.messages,
            cards=self.conversation_state["cards"],
            card_keywords=self.conversation_state["card_keywords"]
        )

        return response
