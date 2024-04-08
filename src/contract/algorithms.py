from src.database.models import Contract


def contract_rpe_map(contract: Contract):
    return ''.join(map(lambda b: str(int(b)), [contract.reserved, contract.payment, contract.executed]))
