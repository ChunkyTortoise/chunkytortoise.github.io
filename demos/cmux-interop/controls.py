"""Dependency-free model of eight fail-closed dispatch controls."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import PurePath
from typing import Iterable, Mapping


class ControlViolation(ValueError):
    """Raised when a dispatch or collection invariant does not hold."""


@dataclass(frozen=True)
class RoleContract:
    title: str
    executable: str
    cwd: str
    actor: str


@dataclass(frozen=True)
class SurfaceObservation:
    uuid: str
    title: str
    executable: str
    cwd: str
    actor: str
    ready: bool = True


def executable_matches(expected: str, observed: str) -> bool:
    return PurePath(observed).name == expected


def verify_surface(contract: RoleContract, observed: SurfaceObservation) -> None:
    checks = {
        "canonical title": observed.title == contract.title,
        "exact executable": executable_matches(contract.executable, observed.executable),
        "working directory": observed.cwd == contract.cwd,
        "actor identity": observed.actor == contract.actor,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise ControlViolation("surface rejected: " + ", ".join(failed))


def resolve_by_surface_uuid(
    contract: RoleContract,
    surface_uuid: str,
    observations: Mapping[str, SurfaceObservation],
) -> SurfaceObservation:
    try:
        observed = observations[surface_uuid]
    except KeyError as exc:
        raise ControlViolation("surface UUID is not observable") from exc
    verify_surface(contract, observed)
    return observed


def mission_sha256(mission: bytes) -> str:
    return sha256(mission).hexdigest()


def context_binding(
    run_id: str,
    role: str,
    nonce: str,
    mission_hash: str,
    surface_uuid: str,
) -> str:
    payload = "\n".join((run_id, role, nonce, mission_hash, surface_uuid)) + "\n"
    return sha256(payload.encode()).hexdigest()


def validate_result(result: str, nonce: str, binding: str) -> None:
    lines = [line for line in result.splitlines() if line.strip()]
    required = [f"CMUX_RUN_NONCE={nonce}", f"CMUX_CONTEXT_BINDING={binding}"]
    if lines[:2] != required:
        raise ControlViolation("stale or cross-mission result")


def seal_targets(targets: Iterable[Mapping[str, str]]) -> str:
    canonical = json.dumps(list(targets), sort_keys=True, separators=(",", ":"))
    return sha256(canonical.encode()).hexdigest()


def verify_target_seal(targets: Iterable[Mapping[str, str]], sealed_hash: str) -> None:
    if seal_targets(targets) != sealed_hash:
        raise ControlViolation("sealed target or mission mutation")


STATE_RANK = {
    "draft": 0,
    "sealed": 1,
    "dispatching": 2,
    "running": 3,
    "collecting": 5,
    "gated": 6,
    "blocked": 7,
    "partial-dispatch": 10,
}


def transition_state(current: str, requested: str) -> str:
    if current == "partial-dispatch":
        raise ControlViolation("partial-dispatch is terminal")
    if current not in STATE_RANK or requested not in STATE_RANK:
        raise ControlViolation("unknown run state")
    if STATE_RANK[requested] < STATE_RANK[current]:
        raise ControlViolation("run state regression")
    return requested


def select_independent_verifier(
    conductor: str,
    preferred_order: Iterable[str],
    availability: Mapping[str, bool],
) -> str:
    for role in preferred_order:
        if role != conductor and availability.get(role, False):
            return role
    raise ControlViolation("no independent verifier is ready")


def mint_successor(run_id: str, state: str, existing: Iterable[str]) -> str:
    if state not in {"partial-dispatch", "blocked", "timed-out", "rejected", "cancelled"}:
        raise ControlViolation("successor requires an explicit terminal predecessor")
    used = set(existing)
    index = 1
    while True:
        candidate = f"{run_id}-successor-{index:02d}"
        if candidate not in used:
            return candidate
        index += 1
