"""
Genesis Block
{
index: 0,
timestamp: current time,
data: "I am the beginning and the end",
proof: 3,
previous_hash: "0"
} -> hash() -> 139abbb0

{
index: 1,
timestamp: current time,
data: "second is the best",
proof: 43567,
previous_hash: "139abbb0"
} -> hash() -> 897653bbc

{
index: 3,
timestamp: current time,
data: "Why not third",
proof: 7456,
previous_hash: "897653bbc"
} -> hash() -> 8865577gghh


"""

import datetime as _dt
import hashlib as _hashlip
import json as _json

class Blockchain:
    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self.createBlock(data="I am the beginning and the end", proof=1,
                                         previous_hash="0", index=1)
        self.chain.append(genesis_block)
    def mineBlock(self, data: str) -> dict:
        previous_block = self.getPreviousBlock()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(previous_proof, index, data)
        previous_hash = self._hash(block=previous_block)
        block = self.createBlock(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )
        self.chain.append(block)
        return block

    def _hash(self, block: dict) -> str:
        """
        Has a block and return it's cryptographic hash of block
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()
        return _hashlip.sha256(encoded_block).hexdigest()

    def _to_digest(self, new_proof: int, previous_proof: int, index: str, data: str) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data # Simple of your mathematical formular you will keep secret for the miners to mine
        return to_digest.encode()

    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_digest = self._to_digest(new_proof=new_proof,
                                        previous_proof=previous_proof,
                                        index=index, data=data)
            hash_value = _hashlip.sha256(to_digest).hexdigest()

            if hash_value[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def getPreviousBlock(self) -> dict:
        return self.chain[-1]

    def createBlock(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        return block

    # Now let check if the chain is valid.
    def isChainValid(self) -> bool:
        current_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            next_block = self.chain[block_index]

            if next_block["previous_hash"] != self._hash(current_block):
                return False
            current_proof = current_block["proof"]
            next_index, next_data, next_proof = (
                next_block["index"],
                next_block["data"],
                next_block["proof"]
            )
            hash_value = _hashlip.sha256(self._to_digest(new_proof=next_proof,
                                                         previous_proof=current_proof,
                                                         index=next_index, data=next_data,)
                                         ).hexdigest()
            if hash_value[:4] != "0000":
                return False
            current_block = next_block
            block_index += 1
            return True