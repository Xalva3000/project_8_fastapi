from src.producer.schemas import CreateProducer


def create_producer(producer_in: CreateProducer):
    producer = producer_in.model_dump()
    return {'success': True, 'producer': producer}