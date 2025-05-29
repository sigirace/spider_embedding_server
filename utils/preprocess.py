import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pymupdf4llm import to_markdown

from utils.file_utils import get_image_path


def get_spliter(
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: list[str] = ["\n\n", "\n", " ", ""],
) -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
    )


# 마크다운 내 이미지 링크 제거 + 추출
def extract_images_and_clean_text(md_text: str) -> tuple[str, list[str]]:
    pattern = r"!\[\]\((.*?)\)"
    image_paths = re.findall(pattern, md_text)
    cleaned_text = re.sub(pattern, "", md_text).replace("#", "").replace("*", "")
    return cleaned_text.strip(), image_paths


# 헤딩 태그 추출
def extract_tags(md_text: str) -> list[str]:
    lines = md_text.splitlines()
    tags = []
    for line in lines:
        match = re.match(r"^#{1,4} (.+)", line)
        if match:
            tags.append(match.group(1).strip().replace("*", ""))
    return tags


def chunking(
    chunk_size: int,
    chunk_overlap: int,
    file_path: str,  # ex) ./data/app_id/1234.pdf
    img_save_path: str,  # ex) app_id/meta_id
) -> list[Document]:

    image_path = get_image_path(img_save_path)  # ./static/data/app_id/document_id

    # 이미지 포함 마크다운 추출
    page_chunks = to_markdown(
        doc=file_path,
        page_chunks=True,
        force_text=True,
        use_glyphs=True,
        write_images=True,
        image_path=image_path,  # 원하는 경로에 저장
        show_progress=True,
    )

    spliter = get_spliter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = []

    for i, chunk in enumerate(page_chunks):
        page_number = i + 1
        raw_md = chunk.get("text", "")

        # 마크다운 이미지 링크 제거 및 경로 추출
        cleaned_text, inline_image_links = extract_images_and_clean_text(raw_md)
        tags = extract_tags(raw_md)

        base_metadata = {
            "source": file_path,
            "page": page_number,
            "tags": tags,
            **chunk.get("metadata", {}),
        }

        base_doc = Document(page_content=cleaned_text, metadata=base_metadata)

        if cleaned_text.strip():
            split_docs = spliter.split_documents([base_doc])
        elif inline_image_links:
            # 텍스트는 없지만 이미지가 있을 경우, 하나의 Document 생성
            split_docs = [base_doc]
        else:
            split_docs = []

        for j, sub_doc in enumerate(split_docs):
            if j == 0 and inline_image_links:
                sub_doc.metadata["images"] = inline_image_links
            documents.append(sub_doc)

    return documents
