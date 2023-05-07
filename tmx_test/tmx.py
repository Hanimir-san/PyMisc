import os
import regex as re

from copy import deepcopy
from pathlib import Path

import numpy

from lxml import etree

class Tmx():

    def __init__(self, path, logger=None):
        self.path = path
        self.tree = self.__parse_tmx()
        self.src_lang = None
        self.src_lang = self.get_tmx_src_lang()
        self.src_lang_base = self.src_lang.split('-')[0] if self.src_lang else None
        self.trg_lang = None
        self.trg_lang = self.get_tmx_trg_lang()
        self.trg_lang_base = self.trg_lang.split('-')[0] if self.trg_lang else None

    def __parse_tmx(self):
        """
        Parses a TMX file to lxml ElementTree object. There are several edge cases such 
        as file validation not covered here, as they are unnecessary for the current task.
        :param path:
        """
        return etree.parse(self.path)
    
    def get_tmx_src_lang(self):
        """
        Gets the source language of a TMX file as ISO-2 language code.
        """
        if self.src_lang:
            return self.src_lang
        tmx_header = self.tree.find('header')
        tmx_src_lang = tmx_header.attrib.get('srclang', None)
        if not tmx_src_lang:
            tmx_src_tuv = self.tree.xpath('body/tu[1]/tuv[1]')
            tmx_src_lang = tmx_src_tuv[0].attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None) if tmx_src_tuv else None
        return tmx_src_lang

    def get_tmx_trg_lang(self):
        """
        Gets the target language of a TMX file as ISO-2 language code.
        """
        if self.trg_lang:
            return self.trg_lang
        tmx_header = self.tree.find('header')
        tmx_trg_lang_prop = tmx_header.xpath('prop[@type="targetlang"]')
        tmx_trg_lang = tmx_trg_lang_prop[0].text if tmx_trg_lang_prop else None
        if not tmx_trg_lang:
            tmx_trg_tuv = self.tree.xpath('body/tu[1]/tuv[last()]')
            tmx_trg_lang = tmx_trg_tuv[0].attrib.get('{http://www.w3.org/XML/1998/namespace}lang', None) if tmx_trg_tuv else None
        return tmx_trg_lang

    def get_tus(self):
        """
        Get translation units from a TMX as lxml ElementTree objects. Tu should normally be
        it's own classe, we are omitting the added layer of complexity at this stage. 
        """
        return self.tree.xpath('body/tu')
    
    def __get_tu_src_el(self, tu):
        """
        Gets the source element of a translation unit.
        """
        return tu.xpath('tuv[1]')[0]
    
    
    def __get_tu_trg_el(self, tu):
        """
        Gets the target element of a translation unit.
        """
        return tu.xpath('tuv[last()]')[0]

    def __get_tuv_text(self, tuv):
        """
        Gets the text of a Tuv element.
        """
        seg_text = etree.tostring(tuv).decode()
        seg_text = re.sub('^<seg>', '', seg_text)
        seg_text = re.sub('<\/seg>', '', seg_text)
        return seg_text
    
    def get_tu_src_text(self, tu):
        tu_src = self.__get_tu_src_el(tu)
        tu_src = self.__get_tuv_text(tu_src)
        return tu_src
    
    def get_tu_trg_text(self, tu):
        tu_trg= self.__get_tu_trg_el(tu)
        tu_trg = self.__get_tuv_text(tu_trg)
        return tu_trg
    
    def multiply_tus(self, target_count):
        tmx_body = self.tree.find('body')
        tmx_tus = self.get_tus()
        tmx_tu_count = len(tmx_tus)
        tmx_tu_copies = tmx_tu_count
        tmx_tu_current = 0
        while tmx_tu_copies < target_count:
            tmx_tu = tmx_tus [tmx_tu_current]
            tmx_body.append(deepcopy(tmx_tu))
            if tmx_tu_current == tmx_tu_count-1:
                tmx_tu_current = 0
            else:
                tmx_tu_current += 1
            tmx_tu_copies += 1

    def save(self, out_dir=None, out_name=None):
        out_dir = out_dir if out_dir else os.path.dirname(self.path)
        out_name = out_name if out_name else os.path.basename(self.path)
        out_name = f'{out_name}.tmx' if not out_name.endswith('tmx') else out_name
        out_path = os.path.join(out_dir, out_name)
        print(out_path)
        self.tree.write(out_path, encoding=self.tree.docinfo.encoding, xml_declaration=True)


    
if __name__ == "__main__":
    path = '/home/admin/Documents/Projects/PyMisc/tmx_test/data/memoq_sample.tmx'
    tmx_obj = Tmx(path)
    tmx_obj.multiply_tus(target_count=100000)
    tmx_obj.save(out_name='memoq_sample_100000_tus.tmx')
