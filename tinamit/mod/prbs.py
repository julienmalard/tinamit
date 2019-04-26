import os

import numpy as np
import numpy.testing as npt

from tinamit.cositas import guardar_json, jsonificar, cargar_json


def verificar_leer_ingr(caso, cls):
    info_prb = cls.prb_ingreso()
    if info_prb:
        arch, f_leer = info_prb
        caso.maxDiff = None
        dic = {str(vr): jsonificar(vr.__dict__) for vr in f_leer(arch)}

        dir_, nombre = os.path.split(arch)
        ref = {str(ll): jsonificar(v) for ll, v in _obt_ref(os.path.join(dir_, 'ref', nombre + '.json'), dic).items()}

        caso.assertSetEqual(set(dic), set(ref))
        for vr in ref:
            caso.assertDictEqual(dic[vr], ref[vr], msg=vr)


def verificar_leer_egr(caso, cls):
    info_prb = cls.prb_egreso()
    if info_prb:
        arch, f_leer = info_prb
        dic = {vr: np.array(vl) for vr, vl in f_leer(arch).items()}

        dir_, nombre = os.path.split(arch)
        ref = _obt_ref(os.path.join(dir_, 'ref', nombre + '.json'), dic)
        caso.assertSetEqual(set(dic), set(ref))
        for vr in ref:
            npt.assert_equal(dic[vr], ref[vr], err_msg=vr)


def verificar_simul(caso, cls):
    arch_ingr = cls.prb_simul()
    if arch_ingr and cls.instalado():
        mod = cls(arch_ingr)
        res = mod.simular(2).a_dic()

        dir_, nombre = os.path.split(arch_ingr)

        ref = _obt_ref(os.path.join(dir_, 'ref', nombre + '.simul.json'), res)
        caso.assertDictEqual(res, ref)


def _obt_ref(arch, d_auto):
    if not os.path.isfile(arch):
        guardar_json(jsonificar(d_auto), arch)

    return cargar_json(arch)
