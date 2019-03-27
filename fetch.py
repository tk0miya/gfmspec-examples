"""
    conftest
    ~~~~~~~~

    :copyright: Copyright 2019 by Takeshi KOMIYA
    :license: Apache License 2.0, see LICENSE for details.
"""

from urllib.request import urlopen
from xml.etree import ElementTree

import html5lib


def fetch_gfmspec():
    def elem2code(elem):
        code = ElementTree.tostring(elem, encoding="utf-8", method="text").decode('utf-8')
        code = code.rstrip("\n")
        code = code.replace("→", "\t")
        return code

    with urlopen("https://github.github.com/gfm/") as f:
        document = html5lib.parse(f, transport_encoding=f.info().get_content_charset(),  # type: ignore
                                  namespaceHTMLElements=False)

    for example in document.findall('.//div[@class="example"]'):
        example_id = example.attrib['id']
        source = example.find('.//pre/code[@class="language-markdown"]')

        yield example_id, elem2code(source)


def main():
    for example_id, source in fetch_gfmspec():
        with open(example_id + '.md', 'wt') as f:
            f.write(source)


if __name__ == '__main__':
    main()
