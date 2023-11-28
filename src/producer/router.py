from typing import Annotated

from fastapi import APIRouter, Path
from src.producer.schemas import CreateProducer
from src.producer.crud import create_producer

router = APIRouter(prefix='/producer', tags=['producer'])


@router.get("/")
def get_item():
    return ['producer1', 'producer2', 'producer3']

@router.post('/')
async def create_producer(producer: CreateProducer):
    return create_producer(producer=producer)

@router.get("/{item_id}/")
def get_item(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {'status': '200', 'item': item_id}

