import re
from contextlib import suppress

import libcst as cst
from libcst import matchers as m


class CollectSpiderNames(cst.CSTVisitor):
    def __init__(self, spider_names=None):
        super().__init__()
        self.spider_names = spider_names

    def visit_ClassDef_name(self, node: "ClassDef") -> None:
        class_name = node.name.value
        if 'Parser' not in class_name:
            class_components = node.body.body
            for comp in class_components:
                if m.matches(
                        comp,
                        m.SimpleStatementLine(
                            body=[m.Assign(targets=[m.AssignTarget(target=m.Name("name"))])]
                        )):
                    with suppress(AttributeError):
                        spider_name = comp.body[0].value.value
                    spider_name = re.sub(r'[\'\"]', '', spider_name)
                    self.spider_names.add(spider_name)

