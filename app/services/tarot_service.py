import os
import random
import time
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableSequence  
from langchain.schema import StrOutputParser 
from app.data import tarot_meaning, templates, tarot_card_images


# 환경변수 로드
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
# 타로 의미 데이터 로드
TAROT_CARD_MEANINGS = tarot_meaning.TAROT_CARD_MEANINGS
# 타로 카드 이미지 URL
TAROT_CARD_IMAGES = tarot_card_images.TAROT_CARD_IMAGES


class TarotReader:
    """
    ✅ 타로 점을 제공하는 클래스
    
    - 사용자가 질문하면 타로 카드를 뽑고 해석하여 응답을 반환
    - 첫 질문(topic 필요)에서는 카드를 3장 뽑아 해석하고, 이후 질문에는 기존 카드의 해석으로 대답
    """

    def __init__(self):
        """
        ✅ TarotReader 클래스 초기화

        - conversation_state : 대화에 필요한 변수 관리
        - model : Langchain의 OpenAI 사용
        - ConversationBufferMemory : 대화 기록 저장
        - 타로 해석을 위한 프롬프트 템플릿 로드.
        """

        # 대화 상태 
        self.conversation_state = {
            "is_card_drawn": False, # 카드를 뽑았는지 bool
            "is_first_reading": True,
            "cards": None,          # 뽑힌 카드 list
            "topic": None,          # 사용자가 선택한 주제 string
            "card_keywords": None,  # 뽑힌 카드의 의미 dict
        }
        
        # 모델 정의 : gpt-4o-mini
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
        ✅ 대화 프롬프트 생성 함수

        - 첫 리딩이면 first_reading_prompt 사용
        - 후속 질문이면 follow_up_prompt 사용
        - str + str으로 templates 생성

        Args : is_first_reading (bool) 카드 뽑음 여부
        Returns : ChatPromptTemplate(프롬프트 템플릿 객체)
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

    
    def topic_update(self, topic):
        """
        ✅ 토픽 저장
        """
        self.conversation_state["topic"] = topic

        return self.conversation_state["topic"]

    def draw_tarot_cards(self):
        """
        ✅ 22장의 메이저 아르카나 타로 카드 중 3장 무작위 뽑기
        """
        tarot_cards = [
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant",
            "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man",
            "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
        ]
        # 카드 정보 업데이트
        self.conversation_state["cards"] = random.sample(tarot_cards, 3)
        # 카드 뽑음 여부 True
        # self.conversation_state["is_card_drawn"] = True

        return self.conversation_state["cards"]  # ["카드이름"]


    def card_images_url(self, cards):
        """
        ✅ self.conversation_state["cards"]에 든 카드 3장의 이미지 URL을 반환
        """
        
        return {card: TAROT_CARD_IMAGES.get(card, "https://i.namu.wiki/i/BldqgVbeK4tGO4_VXDjy-3cMuC_Zw7WDqDUDUsApMzkry4X4SamqFtv6FmL872EJq8uQTelygkk8uG34o1H-4Q.webp") for card in cards}
        

    def card_keywords(self, cards):
        """
        ✅ 뽑은 카드의 의미를 담는 함수
        - process_query()에서 사용

        Args : cards (list) 뽑힌 카드 리스트
        Return : dict
        """
        # 카드 키워드 업데이트
        self.conversation_state["card_keywords"] = {card: TAROT_CARD_MEANINGS[card] for card in cards}

        return self.conversation_state


    def process_query(self, text):
        """
        ✅ 사용자의 질문을 처리하고 대화 응답을 chunk단위로 반환하는 함수

        - 첫 리딩이면 뽑은 카드로 카드 키워드 저장장
        - 후속 질문이면 기존 카드 정보를 유지하면서 답변 제공

        Args : 
            text (str) : 사용자 질문
            topic (str) : 사용자가 선택한 주제
        Yields:
            str : 모델이 생성한 타로 해석 (stream)
        """

        # 1. 사용자 질문 저장
        self.memory.chat_memory.add_user_message(text)

        # 2-1. 첫 리딩이면 : 고른 토픽과 뽑은 카드가 이미 저장된 상태
        if self.conversation_state["is_first_reading"]:
            # 카드 키워드 저장
            self.card_keywords(self.conversation_state["cards"])
            # 첫 리딩 판별 변수 업데이트
            self.conversation_state["is_first_reading"] = False
            # 프롬프트 생성
            prompt_template = self.create_prompt(is_first_reading=True)
        # 2-2. 후속 리딩이면
        else:
            prompt_template = self.create_prompt(is_first_reading=False)

        # 3. 모델 실행
        chain = RunnableSequence(
            prompt_template, 
            self.model,      
            StrOutputParser()  
        )

        # 4. 응답 streaming
        full_response = ""
        for chunk in chain.stream(input={
            "text": text,
            "topic": self.conversation_state["topic"],
            "cards": self.conversation_state["cards"],
            "card_keywords": self.conversation_state["card_keywords"],
            "chat_history": self.memory.chat_memory.messages,
        }):
            yield chunk   
            time.sleep(0.1)
            full_response += chunk

        # 챗봇 응답 저장
        self.memory.chat_memory.add_ai_message(full_response)