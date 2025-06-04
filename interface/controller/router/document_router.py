from typing import List
from fastapi import APIRouter, Depends, File, UploadFile

from application.documents.create_document import CreateDocument
from application.documents.delete_document import DeleteDocument
from application.documents.get_document import GetDocument
from application.documents.get_document_list import GetDocumentList
from application.documents.update_document import UpdateDocument
from common.log_wrapper import log_request
from containers import Container
from domain.users.models import User
from interface.controller.dependency.auth import get_current_user
from interface.dto.document_dto import (
    DocumentRepsonse,
    DocumentUpdateRequest,
    DocumentUploadResponse,
)
from dependency_injector.wiring import Provide, inject

from interface.mapper.document_mapper import DocumentMapper

router = APIRouter(prefix="/document")


@router.post("/{app_id}", response_model=DocumentUploadResponse)
@log_request()
@inject
async def create_document(
    app_id: str,
    file_list: List[UploadFile] = File(...),
    user: User = Depends(get_current_user),
    create_document: CreateDocument = Depends(Provide[Container.create_document]),
):
    success_list, error_list = await create_document(
        app_id=app_id,
        file_list=file_list,
        user_id=user.user_id,
    )

    return DocumentMapper.to_upload_response(success_list, error_list)


@router.get("/{document_id}", response_model=DocumentRepsonse)
@log_request()
@inject
async def get_document(
    document_id: str,
    user: User = Depends(get_current_user),
    get_document: GetDocument = Depends(Provide[Container.get_document]),
):
    document = await get_document(document_id=document_id, user_id=user.user_id)
    return DocumentMapper.to_response(document)


@router.get("/{app_id}/list", response_model=List[DocumentRepsonse])
@log_request()
@inject
async def get_document_list(
    app_id: str,
    user: User = Depends(get_current_user),
    get_document_list: GetDocumentList = Depends(Provide[Container.get_document_list]),
):
    documents = await get_document_list(app_id=app_id, user_id=user.user_id)
    return [DocumentMapper.to_response(doc) for doc in documents]


@router.put("/{document_id}", response_model=DocumentRepsonse)
@log_request()
@inject
async def update_document(
    document_id: str,
    update_document_req: DocumentUpdateRequest,
    user: User = Depends(get_current_user),
    update_document: UpdateDocument = Depends(Provide[Container.update_document]),
):

    document = await update_document(
        document_id=document_id,
        update_document=DocumentMapper.to_update(update_document_req),
        user_id=user.user_id,
    )

    return DocumentMapper.to_response(document)


@router.delete("/{document_id}")
@log_request()
@inject
async def delete_document(
    document_id: str,
    user: User = Depends(get_current_user),
    delete_document: DeleteDocument = Depends(Provide[Container.delete_document]),
):
    await delete_document(document_id, user.user_id)

    return {"message": f"{document_id} Document Deleted"}
