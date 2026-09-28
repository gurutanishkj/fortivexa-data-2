"""
FORTIVEXA - Tamper-Evident SHA-256 Cryptographic Audit Ledger
Problem Statement SIH26184 - Ministry of Home Affairs

Implements a local blockchain-style SHA-256 hash-chain logging every investigator interaction:
- CASE_INGESTION
- PREDICTION_RUN
- DOSSIER_DISPATCH
- GRAPH_INSPECTION

Every block contains: Index, Previous_Hash, Timestamp, Officer_ID, Action, Details, Current_Hash.
Includes full verification methods to ensure non-repudiation and court-admissible audit trails.
"""

import os
import sys
import json
import hashlib
import datetime
from typing import Dict, List, Any, Tuple, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

LEDGER_FILE = os.path.join(BASE_DIR, "data", "audit_ledger.json")

class AuditBlock:
    def __init__(
        self,
        index: int,
        timestamp: str,
        officer_id: str,
        action: str,
        details: Dict[str, Any],
        previous_hash: str,
        current_hash: Optional[str] = None
    ):
        self.index = index
        self.timestamp = timestamp
        self.officer_id = officer_id
        self.action = action
        self.details = details
        self.previous_hash = previous_hash
        self.current_hash = current_hash or self.compute_hash()

    def compute_hash(self) -> str:
        """Computes deterministic SHA-256 hash of the block contents."""
        block_string = (
            f"{self.index}|{self.timestamp}|{self.officer_id}|{self.action}|"
            f"{json.dumps(self.details, sort_keys=True)}|{self.previous_hash}"
        )
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "officer_id": self.officer_id,
            "action": self.action,
            "details": self.details,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditBlock":
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            officer_id=data["officer_id"],
            action=data["action"],
            details=data.get("details", {}),
            previous_hash=data["previous_hash"],
            current_hash=data["current_hash"]
        )

class TamperEvidentAuditLedger:
    def __init__(self, ledger_path: str = LEDGER_FILE):
        self.ledger_path = ledger_path
        self.chain: List[AuditBlock] = []
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        self._load_or_initialize_ledger()

    def _create_genesis_block(self) -> AuditBlock:
        """Initializes the immutable Genesis Block."""
        now = "2026-01-01T00:00:00Z"
        genesis = AuditBlock(
            index=0,
            timestamp=now,
            officer_id="SYSTEM_ROOT_MHA",
            action="GENESIS_INITIALIZATION",
            details={
                "system": "FORTIVEXA Cybercrime Intelligence Platform",
                "authority": "Ministry of Home Affairs - Indian Cyber Crime Coordination Centre (I4C)",
                "problem_statement": "SIH26184",
                "hashing_algorithm": "SHA-256 Merkle-Linked Hash-Chain"
            },
            previous_hash="0" * 64
        )
        return genesis

    def _load_or_initialize_ledger(self):
        """Loads existing ledger from disk or creates genesis block."""
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.chain = [AuditBlock.from_dict(b) for b in data]
                # If corrupted or empty
                if not self.chain:
                    self.chain = [self._create_genesis_block()]
                    self._persist()
            except Exception as e:
                print(f"[FORTIVEXA AuditLedger] Error reading {self.ledger_path}: {e}. Creating new Genesis.")
                self.chain = [self._create_genesis_block()]
                self._persist()
        else:
            self.chain = [self._create_genesis_block()]
            self._persist()

    def _persist(self):
        """Atomically persists the ledger to disk."""
        data = [b.to_dict() for b in self.chain]
        temp_file = f"{self.ledger_path}.tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(temp_file, self.ledger_path)

    @property
    def latest_block(self) -> AuditBlock:
        return self.chain[-1]

    def log_action(
        self,
        officer_id: str,
        action: str,
        details: Dict[str, Any]
    ) -> AuditBlock:
        """
        Appends an immutable action entry to the SHA-256 hash-chain.
        Actions include:
        - CASE_INGESTION
        - PREDICTION_RUN
        - DOSSIER_DISPATCH
        - GRAPH_INSPECTION
        """
        now = datetime.datetime.utcnow().isoformat() + "Z"
        prev_hash = self.latest_block.current_hash
        new_index = len(self.chain)

        new_block = AuditBlock(
            index=new_index,
            timestamp=now,
            officer_id=officer_id or "OFFICER-DEFAULT",
            action=action,
            details=details,
            previous_hash=prev_hash
        )
        
        self.chain.append(new_block)
        self._persist()
        return new_block

    def verify_chain(self) -> Tuple[bool, Optional[int], str]:
        """
        Verifies the cryptographic integrity of the entire ledger.
        Returns:
            (is_valid: bool, compromised_index: Optional[int], status_message: str)
        """
        if not self.chain:
            return False, 0, "Audit ledger is completely empty."

        # Verify Genesis
        genesis = self.chain[0]
        if genesis.index != 0 or genesis.previous_hash != "0" * 64:
            return False, 0, "Genesis block is corrupted or modified."

        if genesis.current_hash != genesis.compute_hash():
            return False, 0, f"Genesis block hash mismatch (computed: {genesis.compute_hash()[:12]}... stored: {genesis.current_hash[:12]}...)"

        # Verify remaining blocks
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            # 1. Previous hash link check
            if current.previous_hash != prev.current_hash:
                return (
                    False,
                    i,
                    f"Cryptographic link broken at Block #{i}! Previous hash ({current.previous_hash[:12]}...) does not match Block #{i-1} hash ({prev.current_hash[:12]}...)"
                )

            # 2. Content integrity check
            recalculated = current.compute_hash()
            if current.current_hash != recalculated:
                return (
                    False,
                    i,
                    f"Block #{i} content has been tampered with! Recomputed: {recalculated[:12]}..., Recorded: {current.current_hash[:12]}..."
                )

        return True, None, f"Audit trail verified: All {len(self.chain)} blocks are cryptographically valid and untampered."

    def get_recent_logs(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Returns the most recent audit blocks in reverse chronological order."""
        return [b.to_dict() for b in reversed(self.chain[-limit:])]

# Singleton instance
_audit_ledger_instance = None

def get_audit_ledger() -> TamperEvidentAuditLedger:
    global _audit_ledger_instance
    if _audit_ledger_instance is None:
        _audit_ledger_instance = TamperEvidentAuditLedger()
    return _audit_ledger_instance

if __name__ == "__main__":
    print("[Testing TamperEvidentAuditLedger]...")
    ledger = get_audit_ledger()
    print(f"Current Ledger Length: {len(ledger.chain)}")
    
    # Log test actions
    b1 = ledger.log_action("OFFICER_DL_4091", "CASE_INGESTION", {"complaint_id": "CMP-2026-00001", "amount": 1500000})
    b2 = ledger.log_action("OFFICER_DL_4091", "PREDICTION_RUN", {"complaint_id": "CMP-2026-00001", "predicted_atm": "ATM_NCR_0042", "confidence": 98.5})
    b3 = ledger.log_action("SUPERVISOR_SP_01", "DOSSIER_DISPATCH", {"dossier_id": "DOS-2026-0091", "status": "APPROVED"})
    
    valid, bad_idx, msg = ledger.verify_chain()
    print(f"Chain Verification: {valid} - {msg}")
    print(f"Latest Block Hash: {ledger.latest_block.current_hash}")
