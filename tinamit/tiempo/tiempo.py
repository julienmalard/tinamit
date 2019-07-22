import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

from tinamit.config import _
from tinamit.cositas import _gen_fecha
from tinamit.unids.conv import convertir


class Tiempo(object):
    def __init__(símismo, t, unid_paso):

        símismo.tmñ_paso = t.tmñ_paso
        símismo.n_pasos = t.n_pasos
        símismo.f_inic = t.f_inic
        símismo.guardar_cada = t.guardar_cada

        símismo.unid_paso, símismo.fact_conv = a_unid_tnmt(unid_paso)

        símismo._convs = {}

        símismo.í = 0

    def t_guardar(símismo):
        return not (símismo.í * símismo.tmñ_paso % símismo.guardar_cada)

    def pasos_avanzados(símismo, unid):
        return símismo._obt_fact_conv(unid) * símismo.fact_conv * símismo.tmñ_paso

    def fecha(símismo):
        pass

    def avanzar(símismo):
        if símismo.í < símismo.n_pasos:
            símismo.í += 1
            return símismo.í
        return False

    def eje(símismo):
        return np.arange(
            símismo.n_pasos * símismo.tmñ_paso + 1,
            step=símismo.guardar_cada * símismo.tmñ_paso
        )

    def _obt_fact_conv(símismo, unid):

        # Evitar buscar la misma unidad 2 veces porque la búsqueda puede ser lenta.
        try:
            return símismo._convs[unid]
        except KeyError:
            fact = convertir(de=símismo.unid_paso, a=unid, val=1)
            símismo._convs[unid] = round(fact)
            return fact

    def __len__(símismo):
        return símismo.n_pasos // símismo.guardar_cada + 1


class TiempoCalendario(Tiempo):
    def fecha(símismo):
        unid_ft = a_unid_ft[símismo.unid_paso]
        return símismo.f_inic + relativedelta(**{unid_ft: símismo.í * símismo.fact_conv})

    def delta_relativo(símismo, n_pasos):
        if símismo.unid_paso in ['año', 'mes']:
            return relativedelta(**{a_unid_ft[símismo.unid_paso]: n_pasos * símismo.tmñ_paso * símismo.fact_conv})

        n_días = convertir(símismo.unid_paso, a='día', val=n_pasos * símismo.tmñ_paso * símismo.fact_conv)
        return relativedelta(days=n_días)

    def fecha_próxima(símismo):
        return símismo.fecha() + símismo.delta_relativo(n_pasos=1)

    def eje(símismo):
        paso = símismo.fact_conv * símismo.guardar_cada * símismo.tmñ_paso
        if símismo.unid_paso == 'mes':
            eje = pd.to_datetime([
                símismo.f_inic + relativedelta(months=i)
                for i in range(0, símismo.n_pasos // símismo.guardar_cada + 1, paso)
            ])
            return eje
        return pd.date_range(
            símismo.f_inic, periods=símismo.n_pasos // símismo.guardar_cada + 1,
            freq=str(paso) + _a_unid_pandas[símismo.unid_paso]
        )

    def pasos_avanzados(símismo, unid):
        unid, fact = a_unid_tnmt(unid)
        if símismo.unid_paso == 'año' and unid == 'mes':
            return 12 * símismo.tmñ_paso * símismo.fact_conv / fact

        if símismo.unid_paso in ['año', 'mes']:
            delta = relativedelta(**{a_unid_ft[símismo.unid_paso]: símismo.tmñ_paso * símismo.fact_conv / fact})
            n_días = (símismo.fecha() - (símismo.fecha() - delta)).days
            return int(convertir('día', a=unid, val=n_días))

        return int(convertir(símismo.unid_paso, a=unid, val=símismo.tmñ_paso * símismo.fact_conv / fact))


class EspecTiempo(object):
    def __init__(símismo, n_pasos, f_inic=None, tmñ_paso=1, guardar_cada=1):

        if (int(tmñ_paso) != tmñ_paso) or (tmñ_paso < 1):
            raise ValueError(_('`tmñ_paso` debe ser un número entero superior a 0.'))
        símismo.f_inic = _gen_fecha(f_inic)

        símismo.tmñ_paso = tmñ_paso
        símismo.n_pasos = n_pasos
        símismo.guardar_cada = guardar_cada

    def gen_tiempo(símismo, unid_paso):
        if símismo.f_inic:
            return TiempoCalendario(t=símismo, unid_paso=unid_paso)
        else:
            return Tiempo(t=símismo, unid_paso=unid_paso)


def a_unid_tnmt(unid):
    unid = unid.lower()
    aceptables = [
        'año', 'mes', 'semana', 'día', 'hora', 'minuto',
        'secundo', 'microsecundo', 'millisecundo', 'nanosecundo'
    ]
    for u in aceptables:
        if unid == u:
            return unid, 1
        try:
            factor = convertir(de=unid, a=u)
            if int(factor) == factor:
                return u, factor
        except (ValueError, KeyError):
            pass
    raise ValueError(
        _('La unidad de tiempo "{}" no se pudo convertir a años, meses, días, horas, minutos o secundos.').format(unid))


a_unid_ft = {
    'año': 'years',
    'mes': 'months',
    'semana': 'weeks',
    'día': 'days',
    'hora': 'hours',
    'minuto': 'minutes',
    'secundo': 'seconds',
    'millisecundo': 'milliseconds',
    'microsecundo': 'microseconds',
}

_a_unid_pandas = {
    'año': 'A',
    'mes': 'M',
    'día': 'D',
    'hora': 'H',
    'minuto': 'min',
    'secundo': 'S',
    'millisecundo': 'ms',
    'microsecundo': 'us',
}
