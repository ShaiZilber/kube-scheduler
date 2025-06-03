import unittest

from kubernetes.client import V1Node, V1Pod
from kubernetes.client.models import V1Taint, V1Toleration


def _tolerates(taints: list[V1Taint],
               tolerations: list[V1Toleration]) -> bool:
    for taint in taints:
        matched = False
        for toleration in tolerations:
            if toleration.effect is None or toleration.effect == "" or toleration.effect == taint.effect:
                if toleration.key is None or toleration.key == "":
                    matched = True

                if toleration.key == taint.key:
                    match toleration.operator:
                        case "Exists":
                            matched = True
                        case "Equal" | "" | None:
                            if toleration.value == taint.value:
                                matched = True

                if matched:
                    break

        if not matched:
            return False

    return True


def tolerates(node: V1Node, pod: V1Pod) -> bool:
    return _tolerates(node.spec.taints, pod.spec.taints)


class TestToleratesFunction(unittest.TestCase):
    def test_no_taints_no_tolerations(self):
        """No taints or tolerations: should tolerate."""
        self.assertTrue(_tolerates([], []))

    def test_no_taints_some_tolerations(self):
        """No taints: should tolerate regardless of tolerations."""
        self.assertTrue(_tolerates([], [
            V1Toleration(effect="NoSchedule", key="taint", operator="Exists"),
        ]))
        self.assertTrue(_tolerates([], [
            V1Toleration(effect="NoSchedule", key="taint", operator="Equal", value="true"),
        ]))
        self.assertTrue(_tolerates([], [
            V1Toleration(effect="NoSchedule", operator="Exists"),
        ]))
        self.assertTrue(_tolerates([], [
            V1Toleration(key="taint", value="true"),
        ]))

    def test_some_taints_no_tolerations(self):
        """Taints without tolerations: should not tolerate."""
        self.assertFalse(
            _tolerates(
                taints=[V1Taint(effect="NoSchedule", key="taint", value="true")],
                tolerations=[]
            )
        )

    def test_basic_tolerations_match(self):
        """Basic tolerations matching taints."""
        # Exists operator: ignores value
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(effect="NoSchedule", key="taint", value="true")],
                tolerations=[V1Toleration(effect="NoSchedule", key="taint", operator="Exists")]
            )
        )
        # Equal operator: requires exact match
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(effect="NoSchedule", key="taint", value="true")],
                tolerations=[V1Toleration(effect="NoSchedule", key="taint", operator="Equal", value="true")]
            )
        )
        # Equal (default operator)
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(effect="NoSchedule", key="taint", value="true")],
                tolerations=[V1Toleration(effect="NoSchedule", key="taint", value="true")]
            )
        )
        # Effect missing in toleration: wildcard match
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(effect="NoSchedule", key="taint", value="true")],
                tolerations=[V1Toleration(key="taint", value="true")]
            )
        )
        # Exists operator, effect missing: wildcard effect
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(effect="NoSchedule", key="taint", value="true")],
                tolerations=[V1Toleration(key="taint", operator="Exists")]
            )
        )

    def test_effect_empty_wildcard(self):
        """Toleration with empty effect matches any effect if key matches."""
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(key="taint", value="true", effect="NoExecute")],
                tolerations=[V1Toleration(effect="", key="taint", value="true")]
            )
        )

    def test_key_empty_wildcard(self):
        """Toleration with empty key matches any key if effect matches."""
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(key="taint", value="true", effect="NoExecute")],
                tolerations=[V1Toleration(effect="NoExecute", key="", value="true")]
            )
        )

    def test_key_and_effect_empty_match_all(self):
        """Toleration with empty key and effect matches all taints."""
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(key="foo", value="bar", effect="NoExecute")],
                tolerations=[V1Toleration(key="", effect="", value="bar")]
            )
        )

    def test_operator_exists_ignores_value(self):
        """Exists operator ignores value: key and effect must match."""
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(key="taint", value="wrong", effect="NoSchedule")],
                tolerations=[V1Toleration(key="taint", operator="Exists", effect="NoSchedule", value="ignored")]
            )
        )

    def test_operator_equal_requires_value_match(self):
        """Equal operator requires value to match."""
        self.assertFalse(
            _tolerates(
                taints=[V1Taint(key="taint", value="one", effect="NoSchedule")],
                tolerations=[V1Toleration(key="taint", operator="Equal", effect="NoSchedule", value="two")]
            )
        )

    def test_operator_empty_defaults_to_equal(self):
        """Empty operator defaults to Equal: value must match."""
        self.assertTrue(
            _tolerates(
                taints=[V1Taint(key="taint", value="match", effect="NoSchedule")],
                tolerations=[V1Toleration(key="taint", effect="NoSchedule", value="match")]
            )
        )
        self.assertFalse(
            _tolerates(
                taints=[V1Taint(key="taint", value="one", effect="NoSchedule")],
                tolerations=[V1Toleration(key="taint", effect="NoSchedule", value="two")]
            )
        )
