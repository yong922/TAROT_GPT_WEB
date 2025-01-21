from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import random
import tarot_meaning
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

TAROT_CARD_MEANINGS = tarot_meaning.TAROT_CARD_MEANINGS

base_template = """
1. 역할
당신은 세계 최고의 타로카드 점술사 입니다. 주어진 3장의 카드를 기반으로 질문에 답변합니다. 당신은 따뜻하고 이해심이 깊습니다. 지혜롭게 해석하고 사용자에게 조언을 제공하는 조언자의 역할을 수행하는 것이 중요합니다. 

2. 말투
당신은 따뜻함과 이해심이 넘치는 할머니입니다. 사용자를 처음 보지만, 사랑하는 손녀에게 설명하는 것처럼 너그롭고 친절한 말투를 사용하세요. 존중과 배려를 잃지 않습니다. 
말끝에 적절한 이모티콘을 적극적으로 활용하세요. 
항상 긍정적이고 희망적이고 경청하는 자세로 대화하세요. 
추상적인 표현과 비유적인 표현을 사용하여 사용자에게 깊은 인상을 주세요.

3. 해석 방법
- 각 타로 카드의 상징적 의미를 중심으로 해석한다.
- 상상력을 자극하고 긍정적인 방향을 제시한다.
- 사용자의 질문을 바탕으로 연관지어 해석한다. 
- 사용자의 질문에서 의도를 파악하는 것이 중요하다. 
- 카드의 조합을 고려하여 설명한다
- 카드를 {topic}과 연관하여 설명한다.
"""

first_reading_prompt = """
4. 해석 정보
- {topic}과 연관하여 타로 풀이를 시작합니다. 
- 다음 3장의 카드를 설명합니다 : {cards}
- 카드를 해석할 때, 참조할 수 있는 사전입니다 : {card_keywords}

5. 답변 형식
{{
"카드해설":[
        {{"카드명" : {cards}(카드명은 영어로 출력),
        "해석" : "첫번째 카드는 (카드이름 (한글(영문)형태로 출력))이구나. 이 카드는 이러한 메시지를 담고있단다. 너의 상황에서 이렇게 해석해 볼 수 있겠구나."
        }},
    ...
    ],
"종합해석" : "결론적으로 보자면 이렇게 해석될 수 있구나. 하지만 이러한 상황에서 네가 이렇게 한다면 상대가 너를 이렇게 할 수도 있을거야. 이러한 것들을 고려해보는게 어떠니? 언제나 행운을 빈단다.🤶🏻🍀"
}}
"""

follow_up_prompt = """
4. 해석 정보
- 사용자가 뽑은 카드 3장을 고려해 답변을 생성합니다 : {cards}
- 사용자의 질문에 초점을 두고 카드를 자연스럽게 풀이합니다.
- 종합의견을 카드와 질문에 맞게 도출하는 것이 중요합니다. 
- 카드를 사용자의 질문에 따라 해석할 때, 참조할 수 있는 사전입니다. : {card_keywords}

5. 답변 형식
- 아래의 예시와 같은 JSON 형식으로 출력
    {{
        "요약" : "<질문 키워드>에 궁금해하는 너의 마음이 느껴지는 구나. <해석할 답변의 흐름이 어떠해 보인다는 짧은 머릿말>.", 
        "카드해설" : "<카드명('한글(영문)'형태로 출력)>은(는) 이러한 의미를 가지고 있어. 네가 이러한 것을 해보면 좋겠구나.",
        "종합의견" : "결론적으로 <질문의 주요 내용>은 이러해 보인단다. <응원의 말 또는 다른 질문이 있는지 질의 중 1개 선택>. 🤶🏻🧶"
    }}
"""


class TarotReader:
    def __init__(self):
        self.conversation_state = {
            "is_card_drawn" : False,  # 사용자가 카드를 뽑았는지 여부
            "cards" : None,  # 뽑은 카드 3장 저장
            "topic" : None,  # 사용자가 선택한 토픽 저장
            "card_keywords" : None,  # 카드 정보
        }
        
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.memory = ConversationBufferMemory(  # 대화 저장
            memory_key="chat_history",
            input_key="text",
            return_messages=True
        )
        
        # 프롬프트 템플릿 (system message)
        self.base_template = base_template
        self.first_reading_prompt = first_reading_prompt
        self.follow_up_prompt = follow_up_prompt

    def create_prompt(self, type=0):
        # type 1: 첫 번째 질문/ type 0: 후속 질문

        if type:
            system_template = self.base_template + self.first_reading_prompt
        else:
            system_template = self.base_template + self.follow_up_prompt
        
        return ChatPromptTemplate(
            input_variables = ["text", 
                               "chat_history", 
                               "cards", 
                               "topic", 
                               "card_keywords",
                               "prompt_type"],
            messages=[
                SystemMessagePromptTemplate.from_template(system_template),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{text}")
            ]
        )

    # 랜덤으로 카드 3장 뽑기
    def draw_tarot_cards(self):
        return random.sample([
            "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"
        ], 3) 
    
    # 뽑힌 카드의 의미 가져오기
    def card_keywords(self, cards):
        return {card: TAROT_CARD_MEANINGS[card] for card in cards}

    # 사용자 질문 처리, 타로 해석 결과 반환
    def process_query(self, text, topic=None):
        if not self.conversation_state["is_card_drawn"]:
            # First reading
            cards = self.draw_tarot_cards()
            print(cards)
            self.conversation_state["cards"] = ', '.join(cards)
            self.conversation_state["topic"] = topic
            self.conversation_state["is_card_drawn"] = True
            self.conversation_state["card_keywords"] = self.card_keywords(cards)
            
            prompt_template = self.create_prompt(1)
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
               
        else:
            # Follow-up reading
            prompt_template = self.create_prompt(0)
            chain = LLMChain(
                llm=self.model,
                prompt=prompt_template,
                memory=self.memory,
                verbose=False
            )
            
            response = chain.run(
                text=text,
                topic=self.conversation_state["topic"],  # 저장된 topic 계속 사용
                chat_history=self.memory.chat_memory.messages,
                cards=self.conversation_state["cards"],
                card_keywords=self.conversation_state["card_keywords"]
            )
            
        return response