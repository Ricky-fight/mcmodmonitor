class Block:
    text: [str]
    indentsCount: int
    INDENT = '\t'

    def __init__(self):
        self.text = []
        self.indentsCount = 0

    def indent(self, add: int = 0):
        self.indentsCount += add
        return self.INDENT * self.indentsCount

    def addLine(self, line=""):
        self.text.append(self.indent() + line)

    def addBlock(self, block):
        if isinstance(block, Block):
            block = block.text
        for i in range(len(block)):
            block[i] = self.indent() + block[i]
        self.text.extend(block)

    def addTitle(self, line, level=1):
        self.indentsCount = 0
        self.addLine(f"{'#' * level} {line}")
        self.indentsCount += 1

    def addFoldBlock(self, summary, block):
        self.indentsCount = 0
        self.addLine(f"<details><summary>{summary}</summary>")
        self.addLine()
        self.addBlock(block)
        self.addLine("</details>")

    def addUl(self, line):
        self.addLine(f"- {line}")


class Report(Block):

    def __init__(self):
        super().__init__()

    def dumps(self):
        ret = ""
        for line in self.text:
            ret += line + '\n'
        return ret


def buildLink(text, link):
    return f"[{text}]({link})"
