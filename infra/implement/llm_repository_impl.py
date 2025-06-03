from fastapi import HTTPException
from infra.api.haiqv_ollama import HaiqvOllamaLLM
from domain.llms.repository import ILlmRepository
import re


_PROMPT_TEMPLATE = """
이 이미지를 문서화된 설명으로 변환해 주세요. 
이미지에 나오는 장면, 사물, 배경, 글자, 구조 등을 최대한 객관적이고 구체적으로 서술해 주세요.
이 설명은 다른 문서와 함께 벡터 임베딩되어 검색될 예정입니다. 
주관적인 추측이나 감정 표현은 배제하고, 정보 중심의 설명으로 작성해 주세요.
결과는 markdown 형식이 아닌 텍스트 형식으로 작성해 주세요.
"""


class LlmRepositoryImpl(ILlmRepository):
    """HaiQV Ollama 연동 구현"""

    def __init__(self, llm: HaiqvOllamaLLM):
        self.llm = llm

    async def describe_image(
        self,
        image_path: str,
    ) -> str:

        try:
            bound_llm = self.llm.bind(images=[image_path])
            response = await bound_llm.ainvoke(_PROMPT_TEMPLATE)

            return re.sub(r"[\*\n\\]", "", response)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
