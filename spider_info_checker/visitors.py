from contextlib import suppress

import libcst as cst
from libcst import matchers as m


class CollectSpiderNames(cst.CSTVisitor):
    def __init__(self, spider_names=None):
        super().__init__()
        self.spider_names = spider_names

    def visit_SimpleStatementLine(self, node: "SimpleStatementLine") -> None:
        if m.matches(
            node,
            m.SimpleStatementLine(
                body=[m.Assign(targets=[m.AssignTarget(target=m.Name("name"))])]
            ),
        ):
            with suppress(AttributeError):
                self.spider_names.add(node.body[0].value.value.replace('"', '').replace("'", ""))
