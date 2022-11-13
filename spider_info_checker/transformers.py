import libcst as cst
from libcst import CSTTransformer
from libcst import matchers as m

from spider_info_checker.misc import get_cst_from_file
from spider_info_checker.templates import SUPER_COMMA, get_dict_from_spider_name
from .templates import SpiderInfoTemplates

Sinfo = SpiderInfoTemplates()


def update_spiders_info(spiders_info: dict | None, missed_spiders_names: set, const_file: str):
    const_cst = get_cst_from_file(const_file)
    if not spiders_info:
        body = const_cst.body
        body.append(Sinfo.assign)
        const_cst = const_cst.with_changes(body=body)
    new_file = const_cst.visit(SpidersInfoTransformer(missed_spiders_names))
    with open(const_file, "w") as file:
        file.write(new_file.code)





class SpidersInfoTransformer(CSTTransformer):
    def __init__(self, missed_names: set):
        self.missed_names = sorted(missed_names)

    def update_braces(self, template_dict: cst.Dict):
        updated_dict = template_dict
        whitespace_block = cst.ParenthesizedWhitespace(
            first_line=cst.TrailingWhitespace(),
            indent=True,
            last_line=cst.SimpleWhitespace(value='    ')
        )
        lbrace = cst.LeftCurlyBrace(whitespace_after=whitespace_block)
        rbrace = cst.RightCurlyBrace(whitespace_before=whitespace_block)
        updated_dict = updated_dict.with_changes(lbrace=lbrace, rbrace=rbrace)
        return updated_dict

    def get_new_elements_from_missed_names(self):
        new_elems = []
        for missed in self.missed_names:
            sinfo_dict = get_dict_from_spider_name(missed)
            sinfo_dict = self.update_braces(sinfo_dict)
            new_elems.append(cst.DictElement(key=cst.SimpleString(value=f'"{missed}"'),
                                             value=sinfo_dict,
                                             comma=SUPER_COMMA))
        return new_elems

    def leave_SimpleStatementLine(
            self, original_node: cst.SimpleStatementLine, updated_node: cst.SimpleStatementLine
    ) -> cst.SimpleStatementLine:
        if m.matches(original_node,
                     m.SimpleStatementLine(body=[m.Assign(targets=(m.AssignTarget(target=m.Name('_SPIDERS_INFO')),))])):
            prev_dicts = original_node.body[0].value.elements
            new_dicts = self.get_new_elements_from_missed_names()
            if new_dicts:
                if prev_dicts:
                    prev_dicts = list(prev_dicts)
                    last = prev_dicts.pop()
                    last = last.with_changes(comma=SUPER_COMMA)
                    prev_dicts.append(last)
                assign = updated_node.body[0]
                assign_value = assign.value
                new_elems = tuple([*prev_dicts, *new_dicts])
                new_ass_value = assign_value.with_changes(elements=new_elems)
                new_ass = assign.with_changes(value=new_ass_value)
                updated_node = updated_node.with_changes(body=[new_ass])
        return updated_node
