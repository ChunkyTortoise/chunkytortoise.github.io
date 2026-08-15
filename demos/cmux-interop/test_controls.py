from __future__ import annotations

import unittest

from controls import (
    ControlViolation, RoleContract, SurfaceObservation, context_binding,
    executable_matches, mint_successor, mission_sha256, resolve_by_surface_uuid,
    seal_targets, select_independent_verifier, transition_state, validate_result,
    verify_surface, verify_target_seal,
)


class InteropThreatModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = RoleContract("Verifier", "agent.exe", "/workspace", "verifier-a")
        self.surface = SurfaceObservation(
            "surface-fixture-1", "Verifier", "agent.exe", "/workspace", "verifier-a"
        )

    def test_01_exact_title_and_executable_reject_prefix_spoof(self) -> None:
        self.assertTrue(executable_matches("agent.exe", "/bin/agent.exe"))
        self.assertFalse(executable_matches("agent.exe", "/bin/agent.exe-helper"))
        with self.assertRaisesRegex(ControlViolation, "canonical title"):
            verify_surface(self.contract, SurfaceObservation(
                "surface-fixture-1", "Verifier Copy", "agent.exe", "/workspace", "verifier-a"
            ))

    def test_02_cwd_and_actor_mismatch_fail_closed(self) -> None:
        with self.assertRaisesRegex(ControlViolation, "working directory, actor identity"):
            verify_surface(self.contract, SurfaceObservation(
                "surface-fixture-1", "Verifier", "agent.exe", "/other", "shared-actor"
            ))

    def test_03_nonce_and_context_binding_reject_stale_result(self) -> None:
        mission_hash = mission_sha256(b"read-only fixture")
        binding = context_binding("run-1", "verifier", "nonce-1", mission_hash, self.surface.uuid)
        valid = f"CMUX_RUN_NONCE=nonce-1\nCMUX_CONTEXT_BINDING={binding}\nOK\n"
        validate_result(valid, "nonce-1", binding)
        with self.assertRaisesRegex(ControlViolation, "stale"):
            validate_result(valid, "nonce-old", binding)

    def test_04_sealed_target_mutation_is_rejected(self) -> None:
        targets = [{"role": "verifier", "mission_sha256": "abc"}]
        sealed = seal_targets(targets)
        with self.assertRaisesRegex(ControlViolation, "mutation"):
            verify_target_seal([{"role": "verifier", "mission_sha256": "changed"}], sealed)

    def test_05_partial_dispatch_is_monotonic_and_terminal(self) -> None:
        with self.assertRaisesRegex(ControlViolation, "terminal"):
            transition_state("partial-dispatch", "collecting")
        with self.assertRaisesRegex(ControlViolation, "regression"):
            transition_state("gated", "running")

    def test_06_zero_process_telemetry_uses_exact_uuid_and_full_identity(self) -> None:
        observed = resolve_by_surface_uuid(
            self.contract, self.surface.uuid, {self.surface.uuid: self.surface}
        )
        self.assertEqual(observed, self.surface)
        with self.assertRaisesRegex(ControlViolation, "not observable"):
            resolve_by_surface_uuid(self.contract, "nearby-surface", {})

    def test_07_verifier_selection_is_available_and_independent(self) -> None:
        selected = select_independent_verifier(
            "conductor", ["preferred", "fallback", "conductor"],
            {"preferred": False, "fallback": True, "conductor": True},
        )
        self.assertEqual(selected, "fallback")
        with self.assertRaisesRegex(ControlViolation, "no independent"):
            select_independent_verifier("conductor", ["conductor"], {"conductor": True})

    def test_08_terminal_failure_requires_immutable_successor(self) -> None:
        successor = mint_successor("run-1", "partial-dispatch", {"run-1-successor-01"})
        self.assertEqual(successor, "run-1-successor-02")
        with self.assertRaisesRegex(ControlViolation, "terminal predecessor"):
            mint_successor("run-live", "running", set())


if __name__ == "__main__":
    unittest.main()
