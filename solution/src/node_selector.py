import unittest

from kubernetes.client import V1Node, V1Pod


def is_fit_node(node_labels: dict, pod_node_selector_labels: dict):
    """
    checks if all the pod's node selector labels exists on the given node
    :param node_labels: the labels of the node (node.metadata.labels)
    :param pod_node_selector_labels: the labels of the node selector (pod.spec.node_selector)
    :return: boolean - True if "fit" node, otherwise False
    """

    # if the node selector is None or empty all the nodes fit
    if pod_node_selector_labels is None or not pod_node_selector_labels:
        return True

    # if the node selector field exists and there are no node labels, the node doesn't fit
    if node_labels is None or not node_labels:
        return False

    # if both node selector and node labels exist, node is fit if all the node selector labels exists in node labels.
    return all(
        key in node_labels.keys() and node_labels[key] == value
        for key, value in pod_node_selector_labels.items()
    )


def node_selector_filter(node: V1Node, pod: V1Pod):
    print(
        f"pod name: {pod.metadata.name}, selector: {pod.spec.node_selector}, node: {node.metadata.name}, node labels: {node.metadata.labels}"
    )
    return is_fit_node(node.metadata.labels, pod.spec.node_selector)


class TestNodeSelectorFunction(unittest.TestCase):
    def test_no_node_selector(self):
        """No node selector: should fit no matter of node's labels."""
        self.assertTrue(
            is_fit_node(
                {"node_label1": "value1"},
                {},
            )
        )

        self.assertTrue(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {},
            )
        )
        self.assertTrue(
            is_fit_node(
                {
                    "node_label1": "value1",
                    "node_label2": "value2",
                    "node_label3": "value3",
                    "node_label4": "value4",
                    "node_label5": "value5",
                    "node_label6": "value6",
                },
                {},
            )
        )
        self.assertTrue(
            is_fit_node(
                None,
                None,
            )
        )
        self.assertTrue(
            is_fit_node(
                {"node_label1": "value1"},
                None,
            )
        )

        self.assertTrue(
            is_fit_node(
                {},
                None,
            )
        )
        self.assertTrue(
            is_fit_node(
                {},
                {},
            )
        )

    def test_no_node_labels_with_node_selector(self):
        """no node labels with node selector: should not fit."""
        self.assertFalse(
            is_fit_node(
                node_labels={},
                pod_node_selector_labels={
                    "labelDoesntExist1": "value1",
                    "labelDoesntExist2": "value2",
                },
            )
        )
        self.assertFalse(
            is_fit_node(
                None,
                {"node_label1": "value1"},
            )
        )
        self.assertFalse(
            is_fit_node(
                node_labels={},
                pod_node_selector_labels={"labelDoesntExist1": "value1"},
            )
        )
        self.assertFalse(
            is_fit_node(
                node_labels={},
                pod_node_selector_labels={
                    "node_label1": "value1",
                    "node_label2": "value2",
                    "node_label3": "value3",
                    "node_label4": "value4",
                    "node_label5": "value5",
                    "node_label6": "value6",
                },
            )
        )

    def test_node_selector_doesnt_match_all_node_labels(self):
        """node labels don't match all the node selector: should not fit."""
        # keys dont match
        self.assertFalse(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {"labelDoesntExist1": "value1", "labelDoesntExist2": "value2"},
            )
        )

        # keys dont match
        self.assertFalse(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {"labelDoesntExist1": "value1"},
            )
        )
        # values dont match
        self.assertFalse(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {"node_label1": "badValue1", "node_label2": "badValue2"},
            )
        )

    def test_node_selector_doesnt_match_some_node_labels(self):
        """node labels don't match some of the node selector: should not fit."""
        # node label missing
        self.assertFalse(
            is_fit_node(
                {"node_label1": "value1"},
                {"node_label1": "value1", "node_label2": "value2"},
            )
        )

        # one label not matching
        self.assertFalse(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {"node_label1": "value1", "node_label2": "badValue2"},
            )
        )

    def test_node_selector_match_node_labels(self):
        """all node labels match all node selector: should fit."""
        # all node match all selector
        self.assertTrue(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {"node_label1": "value1", "node_label2": "value2"},
            )
        )

        # one node label match all selector
        self.assertTrue(
            is_fit_node(
                {"node_label1": "value1", "node_label2": "value2"},
                {"node_label1": "value1"},
            )
        )
