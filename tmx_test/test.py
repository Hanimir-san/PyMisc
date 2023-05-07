import numpy as np

from tmx import Tmx

def test_tu_get_text(path):
        tmx_obj = Tmx(path)
        tmx_tus = tmx_obj.get_tus()
        for tu in tmx_tus:
             tu_src = tmx_obj.get_tu_src_text(tu)
             tu_trg = tmx_obj.get_tu_trg_text(tu)


def test_tu_get_text_range(path):
        tmx_obj = Tmx(path)
        tmx_tus = tmx_obj.get_tus()
        for tu_id in range(len(tmx_tus)):
             tu = tmx_tus[tu_id]
             tu_src = tmx_obj.get_tu_src_text(tu)
             tu_trg = tmx_obj.get_tu_trg_text(tu)


def test_tu_get_text_np_arange(path):
        tmx_obj = Tmx(path)
        tmx_tus = tmx_obj.get_tus()
        for tu_id in np.arange(len(tmx_tus)):
             tu = tmx_tus[tu_id]
             tu_src = tmx_obj.get_tu_src_text(tu)
             tu_trg = tmx_obj.get_tu_trg_text(tu)
