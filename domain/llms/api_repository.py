from abc import ABC, abstractmethod


class ILlmAPIRepository(ABC):
    """LLM 호출용 추상 인터페이스"""

    @abstractmethod
    async def describe_image(self, image_path: str) -> str:
        pass
