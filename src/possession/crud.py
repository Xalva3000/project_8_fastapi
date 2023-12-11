from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Possession
from sqlalchemy.engine import Result
from sqlalchemy import select
from src.possession.schemas import PossessionCreate, PossessionUpdate, PossessionUpdatePartial


async def insert_possession(session: AsyncSession, possession_in: PossessionCreate) -> Possession:
    possession = Possession(**possession_in.dict())
    session.add(possession)
    await session.commit()
    await session.refresh(possession)
    return possession


async def select_all_possessions(session: AsyncSession) -> list[Possession]:
    stmt = select(Possession).order_by(Possession.product_id)
    result: Result = await session.execute(stmt)
    possessions = result.scalars().all()
    return possessions


async def select_no_zero_possession(session: AsyncSession) -> list[Possession]:
    stmt = select(Possession).where(Possession.quantity != 0).order_by(Possession.product_id)
    result: Result = await session.execute(stmt)
    possessions = result.scalars().all()
    return possessions


async def select_possession_by_id(session: AsyncSession, product_id: int) -> Possession | None:
    return await session.get(Possession, product_id)


async def delete_possession(session: AsyncSession, possession: Possession):
    await session.delete(possession)
    await session.commit()


async def update_possession(
        session: AsyncSession,
        possession: Possession,
        possession_update: PossessionUpdate | PossessionUpdatePartial,
        partial: bool = False
):
    for k, v in possession_update.model_dump(exclude_unset=partial).items():
        setattr(possession, k, v)
    await session.commit()
    return possession
