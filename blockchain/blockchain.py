from datetime import datetime
from .block import Block

class Blockchain:
    """
    Blockchain simplifiée
    """
    def __init__(self):
        self.chain = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = Block(
            index=0,
            timestamp=str(datetime.now()),
            transactions="Bloc Genesis",
            previous_hash="0"
        )
        self.chain.append(genesis)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        new_block = Block(
            index=len(self.chain),
            timestamp=str(datetime.now()),
            transactions=transactions,
            previous_hash=self.get_latest_block().hash
        )
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True
