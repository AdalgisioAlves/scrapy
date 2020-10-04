
from bs4 import BeautifulSoup

def _remove_attrs(soup):
    tag_list = soup.findAll(lambda tag: len(tag.attrs) > 0)
    for t in tag_list:
        for attr, val in t.attrs:
            del t[attr]
    return soup


def example():
    doc = '<html><head><title>test</title></head><body id="foo"><p class="wahtever">junk</p><div style="background: yellow;">blah</div></body></html>'
    print ('Before:\n%s' % doc)
    soup = BeautifulSoup(doc)
    clean_soup = _remove_attrs(soup)
    print ('After:\n%s' % clean_soup)
example()