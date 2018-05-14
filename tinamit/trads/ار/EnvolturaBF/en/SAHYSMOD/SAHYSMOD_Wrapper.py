from tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper import read_output_file
from tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper import SAHYSMOD_output_vars
from tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper import SAHYSMOD_input_vars
from tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper import codes_to_vars
from tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper import vars_SAHYSMOD
from tinamit.EnvolturaBF.en.SAHYSMOD.SAHYSMOD_Wrapper import ModeloSAHYSMOD


class ModeloSAHYSMOD(ModeloSAHYSMOD):

    def iniciar_modelo(خود, tiempo_final, nombre_corrida):
        return super().iniciar_modelo(tiempo_final=tiempo_final, nombre_corrida=nombre_corrida)

    def avanzar_modelo(خود):
        return super().avanzar_modelo()

    def cerrar_modelo(خود):
        return super().cerrar_modelo()

    def escribir_archivo_ingr(خود, n_años_simul, dic_ingr):
        return super().escribir_archivo_ingr(n_años_simul=n_años_simul, dic_ingr=dic_ingr)

    def leer_archivo_egr(خود, n_años_egr):
        return super().leer_archivo_egr(n_años_egr=n_años_egr)

    def leer_archivo_vals_inic(خود):
        return super().leer_archivo_vals_inic()

    def paralelizable(símismo):
        return super().paralelizable()

vars_SAHYSMOD = vars_SAHYSMOD

codes_to_vars = codes_to_vars

SAHYSMOD_input_vars = SAHYSMOD_input_vars

SAHYSMOD_output_vars = SAHYSMOD_output_vars
