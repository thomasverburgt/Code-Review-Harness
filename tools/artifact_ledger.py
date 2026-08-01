#!/usr/bin/env python3
"""Content-addressed artifact store and append-only execution ledger.

The implementation is intentionally filesystem-backed and zero-dependency. It
is a conformance reference for persistence semantics, not a production database.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import uuid
from pathlib import Path
from typing import Any, Iterable


class LedgerError(Exception):
    """Raised when persistence, integrity, access, or immutability fails."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def content_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def safe_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9._:@-]+", value):
        raise LedgerError(f"unsafe record identifier: {value!r}")
    return value.replace(":", "_")


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, path)
    finally:
        temp = Path(temp_name)
        if temp.exists():
            temp.unlink()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise LedgerError(f"invalid retained JSON at {path}: {exc}") from exc


class ArtifactLedger:
    """Immutable object storage with execution manifests and chained audit."""

    def __init__(self, root: Path, clearance: str = "internal") -> None:
        self.root = root.resolve()
        self.clearance = clearance

    def _object_path(self, object_hash: str) -> Path:
        algorithm, digest = object_hash.split(":", 1)
        if algorithm != "sha256" or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise LedgerError(f"invalid object hash: {object_hash}")
        return self.root / "objects" / algorithm / digest[:2] / f"{digest}.json"

    def put_object(self, value: Any) -> str:
        object_hash = content_hash(value)
        path = self._object_path(object_hash)
        expected = canonical_bytes(value)
        if path.exists():
            if path.read_bytes() != expected:
                raise LedgerError(f"content-address collision or mutation at {path}")
            return object_hash
        atomic_write(path, expected)
        return object_hash

    def get_object(self, object_hash: str) -> Any:
        path = self._object_path(object_hash)
        if not path.is_file():
            raise LedgerError(f"retained object is missing: {object_hash}")
        value = read_json(path)
        if content_hash(value) != object_hash:
            raise LedgerError(f"retained object failed integrity verification: {object_hash}")
        return value

    def put_index(self, family: str, record_id: str, entry: dict[str, Any]) -> None:
        path = self.root / "indexes" / safe_id(family) / f"{safe_id(record_id)}.json"
        encoded = pretty_bytes(entry)
        if path.exists():
            if path.read_bytes() != encoded:
                raise LedgerError(f"immutable index mutation rejected: {family}/{record_id}")
            return
        atomic_write(path, encoded)

    def get_index(self, family: str, record_id: str) -> dict[str, Any]:
        path = self.root / "indexes" / safe_id(family) / f"{safe_id(record_id)}.json"
        if not path.is_file():
            raise LedgerError(f"indexed record not found: {family}/{record_id}")
        return read_json(path)

    def _record_ref(self, logical_path: str, family: str, record_id: str, value: Any,
                    classification: str = "internal", retention_class: str = "architecture-evidence") -> dict[str, Any]:
        if classification != "internal" and self.clearance != classification:
            raise LedgerError(f"access denied for classification {classification!r}")
        object_hash = self.put_object(value)
        ref = {
            "logical_path": logical_path,
            "family": family,
            "record_id": record_id,
            "object_hash": object_hash,
            "classification": classification,
            "retention_class": retention_class,
        }
        self.put_index(family, record_id, ref)
        return ref

    def persist_record(self, logical_path: str, family: str, record_id: str, value: Any,
                       classification: str = "internal", retention_class: str = "architecture-evidence") -> dict[str, Any]:
        """Persist a non-artifact record through the same immutable index boundary."""
        return self._record_ref(logical_path, family, record_id, value, classification, retention_class)

    def persist_artifact(self, value: dict[str, Any], classification: str = "internal") -> dict[str, Any]:
        artifact_id = value.get("artifact", {}).get("artifact_id")
        if not artifact_id:
            raise LedgerError("artifact record is missing artifact.artifact_id")
        retention = value.get("integrity", {}).get("retention_class", "architecture-evidence")
        ref = self._record_ref(f"artifacts/{safe_id(artifact_id)}.json", "artifact", artifact_id, value,
                               classification=classification, retention_class=retention)
        self._index_traceability(value, ref)
        return ref

    def _index_traceability(self, value: dict[str, Any], ref: dict[str, Any]) -> None:
        artifact = value["artifact"]
        links = artifact.get("links", {})
        input_refs = []
        for item in value.get("inputs", []):
            input_refs.append(item.get("artifact_id") or item.get("evidence_id") or item.get("reference"))
        trace = {
            "artifact_id": artifact["artifact_id"],
            "artifact_type": artifact.get("artifact_type"),
            "producer_designation": value.get("identity", {}).get("designation"),
            "lifecycle_state": artifact.get("lifecycle_state"),
            "object_hash": ref["object_hash"],
            "parents": links.get("parents", []),
            "children": links.get("children", []),
            "peers": links.get("peers", []),
            "input_refs": [item for item in input_refs if item],
            "consumers": value.get("consumers", []),
        }
        self.put_index("traceability", artifact["artifact_id"], trace)

    def record_supersession(self, previous_artifact_id: str, successor_artifact_id: str,
                            authority_role: str, decided_at: str, reason: str) -> dict[str, Any]:
        if previous_artifact_id == successor_artifact_id:
            raise LedgerError("an artifact cannot supersede itself")
        previous = self.get_index("artifact", previous_artifact_id)
        successor = self.get_index("artifact", successor_artifact_id)
        supersession_id = str(uuid.uuid5(uuid.UUID("91000000-0000-4000-8000-000000000000"),
                                         "|".join((previous_artifact_id, successor_artifact_id, decided_at))))
        record = {
            "supersession_id": supersession_id,
            "previous_artifact_id": previous_artifact_id,
            "previous_object_hash": previous["object_hash"],
            "successor_artifact_id": successor_artifact_id,
            "successor_object_hash": successor["object_hash"],
            "authority_role": authority_role,
            "decided_at": decided_at,
            "reason": reason,
        }
        ref = self._record_ref(f"supersessions/{supersession_id}.json", "supersession", supersession_id, record)
        return {**record, "record_object_hash": ref["object_hash"]}

    @staticmethod
    def _family_and_id(logical_path: str, value: Any, execution_id: str) -> tuple[str, str]:
        if logical_path.startswith("artifacts/"):
            return "artifact", value["artifact"]["artifact_id"]
        if logical_path.startswith("dispatch/"):
            return "dispatch", value["dispatch_id"]
        if logical_path.startswith("gates/"):
            return "gate", value["gate_result_id"]
        if logical_path == "human-decision-request.json":
            return "decision-request", value["decision_context_id"]
        if logical_path == "schedule.json":
            return "schedule", execution_id
        if logical_path == "routing.json":
            return "routing", execution_id
        if logical_path == "summary.json":
            return "summary", execution_id
        raise LedgerError(f"unrecognized persisted record path: {logical_path}")

    def _build_audit_chain(self, events: list[dict[str, Any]], execution_id: str) -> tuple[list[dict[str, Any]], str]:
        chained: list[dict[str, Any]] = []
        previous = None
        for expected_sequence, event in enumerate(events):
            if event.get("execution_id") != execution_id:
                raise LedgerError("audit event execution_id mismatch")
            if event.get("sequence") != expected_sequence:
                raise LedgerError("audit events are not contiguous and deterministically ordered")
            event_hash = content_hash(event)
            chain_entry = {
                "sequence": expected_sequence,
                "event_id": event["event_id"],
                "event_hash": event_hash,
                "previous_chain_hash": previous,
            }
            chain_hash = content_hash(chain_entry)
            chain_entry["chain_hash"] = chain_hash
            chained.append(chain_entry)
            previous = chain_hash
        return chained, previous or "sha256:" + "0" * 64

    def persist_execution(self, run_dir: Path, source_artifacts: Iterable[Path],
                          workflow_path: Path) -> dict[str, Any]:
        run_dir = run_dir.resolve()
        summary = read_json(run_dir / "summary.json")
        execution_id = summary["execution_id"]
        records: list[dict[str, Any]] = []

        workflow = read_json(workflow_path)
        workflow_record_id = f"{workflow['workflow_id']}@{workflow['workflow_version']}"
        records.append(self._record_ref("workflow.json", "workflow", workflow_record_id, workflow))
        for path in sorted(source_artifacts):
            value = read_json(path)
            retention = value.get("integrity", {}).get("retention_class", "architecture-evidence")
            ref = self._record_ref(f"artifacts/{path.name}", "artifact", value["artifact"]["artifact_id"], value,
                                   retention_class=retention)
            self._index_traceability(value, ref)
            records.append(ref)

        for path in sorted(p for p in run_dir.rglob("*.json") if p.name != "audit-events.json"):
            logical_path = path.relative_to(run_dir).as_posix()
            value = read_json(path)
            family, record_id = self._family_and_id(logical_path, value, execution_id)
            records.append(self._record_ref(logical_path, family, record_id, value))

        events = read_json(run_dir / "audit-events.json")
        if not isinstance(events, list):
            raise LedgerError("audit-events.json must contain an array")
        audit_refs = [self._record_ref(f"audit/{event['sequence']:06d}.json", "audit-event", event["event_id"], event)
                      for event in events]
        chain, chain_head = self._build_audit_chain(events, execution_id)
        audit_ledger = {"execution_id": execution_id, "entries": chain, "chain_head": chain_head}
        audit_ledger_hash = self.put_object(audit_ledger)

        manifest = {
            "manifest_version": "1.0.0",
            "execution_id": execution_id,
            "workflow_id": summary["workflow_id"],
            "scenario": summary["scenario"],
            "records": sorted(records + audit_refs, key=lambda item: item["logical_path"]),
            "audit_ledger_hash": audit_ledger_hash,
            "audit_chain_head": chain_head,
            "attestation": {
                "type": "content-addressed-self-attestation",
                "hash_algorithm": "sha256",
                "attesting_component": "tools/artifact_ledger.py",
            },
        }
        manifest_hash = self.put_object(manifest)
        pointer = {"execution_id": execution_id, "manifest_hash": manifest_hash}
        pointer_path = self.root / "executions" / f"{safe_id(execution_id)}.json"
        encoded = pretty_bytes(pointer)
        if pointer_path.exists() and pointer_path.read_bytes() != encoded:
            raise LedgerError(f"execution mutation rejected: {execution_id}")
        if not pointer_path.exists():
            atomic_write(pointer_path, encoded)
        return {**pointer, "record_count": len(manifest["records"]), "audit_chain_head": chain_head}

    def load_manifest(self, execution_id: str) -> dict[str, Any]:
        pointer_path = self.root / "executions" / f"{safe_id(execution_id)}.json"
        if not pointer_path.is_file():
            raise LedgerError(f"execution not found: {execution_id}")
        pointer = read_json(pointer_path)
        manifest = self.get_object(pointer["manifest_hash"])
        if manifest.get("execution_id") != execution_id:
            raise LedgerError("execution pointer/manifest mismatch")
        return manifest

    def verify_execution(self, execution_id: str) -> dict[str, Any]:
        manifest = self.load_manifest(execution_id)
        for ref in manifest["records"]:
            if ref["classification"] != "internal" and self.clearance != ref["classification"]:
                raise LedgerError(f"access denied for {ref['logical_path']}")
            self.get_object(ref["object_hash"])
        audit_ledger = self.get_object(manifest["audit_ledger_hash"])
        previous = None
        for expected_sequence, entry in enumerate(audit_ledger["entries"]):
            if entry["sequence"] != expected_sequence or entry["previous_chain_hash"] != previous:
                raise LedgerError("audit chain ordering or predecessor mismatch")
            body = {key: entry[key] for key in ("sequence", "event_id", "event_hash", "previous_chain_hash")}
            if content_hash(body) != entry["chain_hash"]:
                raise LedgerError("audit chain hash mismatch")
            self.get_object(entry["event_hash"])
            previous = entry["chain_hash"]
        if (previous or "sha256:" + "0" * 64) != manifest["audit_chain_head"]:
            raise LedgerError("audit chain head mismatch")
        return {"execution_id": execution_id, "records_verified": len(manifest["records"]),
                "audit_events_verified": len(audit_ledger["entries"]), "status": "verified"}

    def replay(self, execution_id: str, output_dir: Path) -> dict[str, Any]:
        manifest = self.load_manifest(execution_id)
        if output_dir.exists() and any(output_dir.iterdir()):
            raise LedgerError(f"replay output directory is not empty: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)
        audit_events: list[tuple[int, Any]] = []
        materialized = 0
        for ref in manifest["records"]:
            value = self.get_object(ref["object_hash"])
            logical_path = ref["logical_path"]
            if logical_path.startswith("audit/"):
                audit_events.append((int(Path(logical_path).stem), value))
                continue
            target = output_dir / Path(logical_path)
            atomic_write(target, pretty_bytes(value))
            materialized += 1
        atomic_write(output_dir / "audit-events.json", pretty_bytes([value for _, value in sorted(audit_events)]))
        return {"execution_id": execution_id, "records_materialized": materialized + 1, "status": "replayed"}
