import datetime

import models
from lark import Lark, Transformer

grammar = """
    start: conversation

    conversation  : _HEADER_TOKEN (_BREAK_TOKEN message)* _BREAK_TOKEN

    _HEADER_TOKEN  : "WEBVTT"
    _BREAK_TOKEN   : _NEWLINE _NEWLINE
    _NEWLINE       : (CR? LF)

    message : INDEX _NEWLINE timing _NEWLINE (PERSON ": ")* TEXT

    INDEX         : INT
    PERSON        : (WORD (" " WORD)*)
    TEXT          : /\w+([ \.,&'](\w)*)*/

    timing : START_TIME " --> " END_TIME

    START_TIME : TIMESTAMP
    END_TIME : TIMESTAMP
    TIMESTAMP     : INT ":" INT ":" DECIMAL

    %import common.INT
    %import common.DECIMAL
    %import common.WORD
    %import common.CR
    %import common.LF
"""


class Trans(Transformer):
    def TEXT(self, name):
        return {"text": str(name)}

    def PERSON(self, name):
        return {"sender": models.Person(name=str(name))}

    def START_TIME(self, name):
        return datetime.time.fromisoformat(str(name))

    def END_TIME(self, name):
        return datetime.time.fromisoformat(str(name))

    def message(self, children):
        obj = {}
        for child in [x for x in children if isinstance(x, dict)]:
            obj.update(child)
        return models.Message.parse_obj(obj)

    def timing(self, children):
        return {"start_time": children[0], "end_time": children[1]}

    def conversation(self, children):
        for n, child in enumerate(children):
            try:
                children[n + 1].predecessor = child
            except IndexError:
                pass
        return models.Conversation(messages=children)

    def start(self, children):
        return children[0]


def parser(s: str) -> models.Conversation:
    lark_parser = Lark(grammar, parser="earley")
    tree = lark_parser.parse(s)
    return Trans(visit_tokens=True).transform(tree)
