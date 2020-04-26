#-*- coding:utf-8 -*-
import os
import re

from bs4 import Tag

from ..base import *

multitran_url_base = u'https://www.multitran.com/m.exe?l1=1&l2=2'
multitran_url_example = u'https://www.multitran.com/m.exe?a=3&sc=0&l1=1&l2=2'
multitran_download_mp3 = True
multitran_download_img = True

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"

@register(u'Multitran')
class Multitran(WebService):
    def __init__(self):
        super().__init__()

    def _get_url(self):
        return multitran_url_base

    def _get_example_url(self):
        return multitran_url_example

    def _get_from_api(self, lang='en'):
        result = {
            'pronunciation': '',
            'image': '',
            'thumb': '',
            'def': '',
            'def_list': [],
            'example': ''
        }

        # Def

        data = self.get_response(u'{0}&s={1}'.format(self._get_url(), self.quote_word))
        soup = parse_html(data)

        table = soup.find( "table", {"width":"100%"} )
        result['def'] = str(table)

        # Example

        data = self.get_response(u'{0}&s={1}'.format(self._get_example_url(), self.word))
        soup = parse_html(data)

        # table = soup.find( "table", {"id":"phrasetable"} )
        table = soup.new_tag('table') 
        tds = soup.findAll( "td", {"class":["phraselist1", "phraselist2"]} )

        for x in range(0, len(tds), 2):
            tr = soup.new_tag("tr")
            tr.append(tds[x])
            tr.append(tds[x + 1])
            table.append(tr)

        result['example'] = str(table)

        return self.cache_this(result)

    @with_styles(need_wrap_css=True, cssfile='_multitran.css')
    def _css(self, val):
        return val

    @export('DEF')
    def fld_definition(self):
        try:
            val = self._get_field('def')
            return self._css(val)
        except:
            return ''

    @export('PRON')
    def fld_pron(self):
       return ''

    @export('PHON')
    def fld_phon(self):
       return ''

    @export('EXAMPLE')
    def fld_example(self):
        try:
            val = self._get_field('example')
            return self._css(val)
        except:
            return ''

    @export([u'派生词', u'Derivatives'])
    def fld_deriv(self):
       return ''

    @export([u'词性', u'POS'])
    def fld_pos(self):
       return ''
