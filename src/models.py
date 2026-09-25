from mongoengine import *
from datetime import datetime
import re
import math
from models.localidades import Localidades

class Acao:
    NOVA_OLT = "NOVA_OLT"
    AMPLIACAO = "AMPLIACAO"
    AMP_NOVA = "AMP+NOVA"
    FIBRA_ATIVA = "FIBRA_ATIVA"
    JUMPER = "JUMPER"
    PENDENTE = "PENDENTE"

class Tecnologia:
    GPON = "GPON"
    XGS = "XGS"

class Etapa:
    ENGENHARIA = "ENGENHARIA"
    IMPLANTACAO = "IMPLANTACAO"
    CADASTRO = "CADASTRO"
    CONCLUIDO = "CONCLUIDO"
    CONGELADO = "CONGELADO"
    OPERACAO = "OPERAÇÃO"
    REGIONAL = "REGIONAL"

class StatusProjeto:
    PROJETO_ENVIADO = "PROJETO_ENVIADO"
    OBRA_CONGELADA = "OBRA_CONGELADA"
    PEND_AMPLIAR_HL4 = "PEND_AMPLIAR_HL4"
    PEND_ATIVAR_HL4 = "PEND_ATIVAR_HL4"
    PEND_BAYFACE = "PEND_BAYFACE"
    PEND_PROJETO_ENG = "PEND_PROJETO_ENG"
    PORTAL = "PORTAL"

class VendorOlt:
    HUAWEI = "HUAWEI"
    NOKIA = "NOKIA"
    RADISYS = "RADISYS"

class ModeloOlt:
    HUAWEI_X2 = "X2"
    HUAWEI_X7 = "X7"
    HUAWEI_X17 = "X17"
    HUAWEI_MA5600T = "MA5600T"
    HUAWEI_FL16 = "FL16"
    HUAWEI_FL4 = "FL4"
    NOKIA_FX8 = "FX8"
    NOKIA_FX16 = "FX16"
    RADISYS = "RADISYS"

class VendorHL4:
    HUAWEI = "HUAWEI"
    CISCO = "CISCO"
    NOKIA = "NOKIA"
    JUNIPER = "JUNIPER"

class Transmissao:
    REMOTA = "REMOTA"
    LOCAL = "LOCAL"

class Facilidades(Document):
    user_id = StringField(default="")
    uf = StringField(default="")
    bc = StringField(required=True)
    fase_atual_ri = StringField(default="")
    plano_mensal = StringField(default="")
    mes = StringField(default="")
    fac_a_construir = IntField(default=0)
    placas = FloatField(default=0)
    placas_prevista = IntField(default=0)
    site_id = StringField(default="")
    origem = StringField(default="")
    fac_construida = IntField(default=0)
    placas_instalada = IntField(default=0)
    fibra = StringField(default="")
    switch_site_vivo_bbtx_hl4_olt_sp = StringField(default="")
    obs = StringField(default="")
    plan_fup = StringField(default="")
    etp = StringField(default="")
    acao = StringField(default=Acao.NOVA_OLT)
    localidade = StringField(default="")
    hostname_olt = StringField(default="")
    vendor_olt = StringField(default="")
    modelo_olt = StringField(default="")
    tecnologia = StringField(default=Tecnologia.GPON)
    transmissao = StringField(default="")
    hostname_hl4 = StringField(default="")
    porta_hl4 = StringField(default="")
    vendor_hl4 = StringField(default="")
    data_envio = DateTimeField()
    san = StringField(default="")
    status_projeto = StringField(default="")
    analista = StringField(default="")
    ped_dhcp = StringField(default="")
    hl4_x_rsd = StringField(default="")
    proc_hl4_olt = StringField(default="")
    rede_externa = StringField(default="")
    projeto = StringField(default="")
    etapa_atual = StringField(default=Etapa.ENGENHARIA)
    responsavel_atual = StringField(default="")

    updated_at = StringField(default=datetime.now().strftime("%d-%m-%Y %H:%M:%S"))


    @staticmethod
    def get_by_id(id):
        return Facilidades.objects(id=id).first()

    @staticmethod
    def get_by_bc(bc):
        return Facilidades.objects(bc=bc)

    @staticmethod
    def exists_by_bc(bc):
        ocorrencia = Facilidades.objects(bc=bc)
        if ocorrencia:
            return True
        return False
    
    @staticmethod
    def get_by_hostname_olt(hostname):
        regex = re.compile(hostname, re.IGNORECASE)
        return Facilidades.objects(hostname_olt=regex)

    @staticmethod
    def get_by_hostname_hl4(hostname):
        regex = re.compile(hostname, re.IGNORECASE)
        return Facilidades.objects(hostname_hl4=regex)
    
    @staticmethod
    def get_all():
        return Facilidades.objects().order_by("-id")

    @staticmethod
    def create(info):

        try:

            info_localidade = None
            if info.get("site_id"):
                info_localidade = Localidades.get_by_site_id(info.get("site_id"))

            new_Facilidades = Facilidades(
                bc = info.get("bc"),
                uf = info.get("uf", "") if info.get("uf", "") != "" else (info_localidade['uf'] if info_localidade else ""),
                fase_atual_ri = info.get("fase_atual_ri", ""),
                plano_mensal = info.get("plano_mensal", ""),
                mes = info.get("mes", ""),
                fac_a_construir = info.get("fac_a_construir", 0),
                placas = info.get("placas", 0),
                placas_prevista = info.get("placas_prevista", 0),
                site_id = info.get("site_id", ""),
                origem = info.get("origem", ""),
                fac_construida = info.get("fac_construida", 0),
                placas_instalada = info.get("placas_instalada", 0),
                fibra = info.get("fibra", ""),
                switch_site_vivo_bbtx_hl4_olt_sp = info.get("switch_site_vivo_bbtx_hl4_olt_sp", ""),
                obs = info.get("obs", ""),
                plan_fup = info.get("plan_fup", ""),
                etp = info.get("etp", ""),
                acao = info.get("acao", Acao.NOVA_OLT) if info.get("acao", "") != "" else Acao.PENDENTE,
                localidade = info_localidade['sigla'] if info_localidade else info.get("localidade", ""),
                hostname_olt = info.get("hostname_olt", ""),
                vendor_olt = info.get("vendor_olt", ""),
                modelo_olt = info.get("modelo_olt", ""),
                tecnologia = info_localidade['tecnologia'] if info_localidade else info.get("tecnologia", Tecnologia.GPON),
                transmissao = info.get("transmissao", ""),
                hostname_hl4 = info.get("hostname_hl4", ""),
                porta_hl4 = info.get("porta_hl4", ""),
                vendor_hl4 = info.get("vendor_hl4", ""),
                data_envio = info.get("data_envio", None),
                san = info.get("san", ""),
                status_projeto = info.get("status_projeto", "PENDENTE ENGENHARIA") if info.get("status_projeto", "") != "" else 'PENDENTE ENGENHARIA',
                analista = info.get("analista", ""),
                ped_dhcp = info.get("ped_dhcp", ""),
                hl4_x_rsd = info.get("hl4_x_rsd", ""),
                proc_hl4_olt = info.get("proc_hl4_olt", ""),
                rede_externa = info.get("rede_externa", ""),
                projeto = info.get("projeto", ""),
                etapa_atual = info.get("etapa_atual", Etapa.ENGENHARIA) if info.get("status_projeto", "") != "" else Etapa.ENGENHARIA,
                responsavel_atual = info.get("responsavel_atual", ""),
                updated_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                )
            
            new_Facilidades.save()

            return new_Facilidades

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def update_by_id(id, dados):

        try:

            facilidade = Facilidades.objects(id=id).first()

            if not facilidade:
                return False

            updated_fibras = False
            fibras_value = 0

            for campo, valor in dados.items():

                if campo in ['site_id', 'localidade']:
                    valor = str(valor).strip().upper()

                
                if campo == "fibra":

                    try:
                        fibras_value = int(float(valor))
                        setattr(facilidade, "fibra", str(fibras_value))
                        updated_fibras = True
                    except Exception:
                        continue
                else:

                    if hasattr(facilidade, campo):
                        setattr(facilidade, campo, valor)

            if updated_fibras:
                # regra facilidade construída = fibras * 64
                facilidade.fac_construida = int(fibras_value * 64)
                # regra placas instaladas = ceil(fibras / 16)
                facilidade.placas_instalada = int(math.ceil(fibras_value / 16))

            facilidade.updated_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            facilidade.save()
            facilidade.reload()

            return facilidade

        except Exception as e:
            print(e)
            return facilidade

    @staticmethod
    def update_by_bc(bc, dados):
        try:
            facilidades = Facilidades.objects(bc=bc)

            if not facilidades:
                return False

            for facilidade in facilidades:
                for campo, valor in dados.items():
                    if hasattr(facilidade, campo):
                        setattr(facilidade, campo, valor)

                facilidade.updated_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                facilidade.save()

            return facilidade

        except Exception as e:
            print(e)
            return False
    

    @staticmethod
    def delete_by_id(id):

        try:

            facilidade = Facilidades.objects(id=id).first()

            if not facilidade:
                return False

            facilidade.delete()

            return True

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_cards_facilidades(planos_mensais=None):

        meses = ['jan-26', 'fev-26', 'mar-26', 'abr-26',
                'mai-26', 'jun-26', 'jul-26', 'ago-26',
                'set-26', 'out-26', 'nov-26', 'dez-26'
                ]

        if not planos_mensais:
            mes_atual = datetime.now().month - 1
            planos_mensais = [meses[mes_atual]]

        facilidades = Facilidades.objects()

        if planos_mensais:
            facilidades = facilidades.filter(plano_mensal__in=planos_mensais)

        return {
            "meses_selecionados": planos_mensais,
            "total_bcs": facilidades.count(),
            "facilidades_mes": sum(item.fac_a_construir or 0 for item in facilidades),
            "novas_olts": facilidades.filter(acao=Acao.NOVA_OLT).count(),
            "ampliacoes": facilidades.filter(acao=Acao.AMPLIACAO).count(),
            "concluidos": facilidades.filter(etapa_atual=Etapa.CONCLUIDO).count(),
            "pendencias": facilidades.filter(etapa_atual__ne=Etapa.CONCLUIDO).count()
        }

    @staticmethod
    def get_dashboard(plano_mensal=None):

        facilidades = Facilidades.objects()

        if plano_mensal:
            facilidades = facilidades.filter(plano_mensal=plano_mensal)

        total_bcs = facilidades.count()

        resumo = {
            "bcs": total_bcs,
            "novas_olts": facilidades.filter(acao=Acao.NOVA_OLT).count(),
            "ampliacoes": facilidades.filter(acao=Acao.AMPLIACAO).count(),
            "facilidades_entregues": sum(f.fac_construida or 0 for f in facilidades),
            "facilidades_planejadas": sum(f.fac_a_construir or 0 for f in facilidades),
            "placas_previstas": sum(f.placas_prevista or 0 for f in facilidades),
            "placas_instaladas": sum(f.placas_instalada or 0 for f in facilidades),
            "fibras_instaladas": sum(int(f.fibra or 0)for f in facilidades if str(f.fibra).isdigit())
        }

        analytics = {
            "vendor": {},
            "modelo": {},
            "tecnologia": {},
            "acoes": {},
            "uf": {}
        }

        for item in facilidades:

            vendor = item.vendor_olt or "NÃO INFORMADO"
            modelo = item.modelo_olt or "NÃO INFORMADO"
            tecnologia = item.tecnologia or "NÃO INFORMADO"
            acao = item.acao or "NÃO INFORMADO"
            uf = item.uf or "N/I"


            if vendor not in analytics["vendor"]:

                analytics["vendor"][vendor] = {
                    "total": 0,
                    "nova_olt": 0,
                    "ampliacao": 0
                }
            if modelo not in analytics["modelo"]:

                analytics["modelo"][modelo] = {
                    "total": 0,
                    "nova_olt": 0,
                    "ampliacao": 0
                }

            analytics["modelo"][modelo]["total"] += 1
            analytics["vendor"][vendor]["total"] += 1

            if acao == Acao.NOVA_OLT:
                analytics["vendor"][vendor]["nova_olt"] += 1
                analytics["modelo"][modelo]["nova_olt"] += 1

            if acao == Acao.AMPLIACAO:
                analytics["vendor"][vendor]["ampliacao"] += 1
                analytics["modelo"][modelo]["ampliacao"] += 1

            analytics["tecnologia"][tecnologia] = analytics["tecnologia"].get(tecnologia, 0) + 1
            analytics["acoes"][acao] = \
                analytics["acoes"].get(acao, 0) + 1


            if uf not in analytics["uf"]:

                analytics["uf"][uf] = {
                    "total_bcs": 0,
                    "nova_olt": 0,
                    "ampliacao": 0,
                    "facilidades_entregues": 0,
                    "placas_instaladas": 0
                }

            analytics["uf"][uf]["total_bcs"] += 1
            analytics["uf"][uf]["facilidades_entregues"] += (item.fac_construida or 0)
            analytics["uf"][uf]["placas_instaladas"] += (item.placas_instalada or 0)

            if acao == Acao.NOVA_OLT:
                analytics["uf"][uf]["nova_olt"] += 1

            if acao == Acao.AMPLIACAO:
                analytics["uf"][uf]["ampliacao"] += 1

        capacidade_instalada = {
            "fibras_instaladas":resumo["fibras_instaladas"],
            "capacidade_teorica":resumo["fibras_instaladas"] * 64,
            "facilidades_entregues":resumo["facilidades_entregues"]
        }

        return {"resumo": resumo, "analytics": analytics, "capacidade_instalada": capacidade_instalada}

    @staticmethod
    def get_dados_relatorio(plano_mensal=None):

        facilidades = Facilidades.objects()

        if plano_mensal:
            facilidades = facilidades.filter(
                plano_mensal=plano_mensal
            )

        dashboard = Facilidades.get_dashboard(plano_mensal)

        conclusoes = facilidades.filter(
            etapa_atual=Etapa.CONCLUIDO
        )

        pendencias = facilidades.filter(
            etapa_atual__ne=Etapa.CONCLUIDO
        )

        etapas = {}

        for etapa in [
            Etapa.ENGENHARIA,
            Etapa.IMPLANTACAO,
            Etapa.CADASTRO,
            Etapa.CONCLUIDO,
            Etapa.CONGELADO,
            Etapa.OPERACAO,
            Etapa.REGIONAL
        ]:

            registros = facilidades.filter(
                etapa_atual=etapa
            )

            etapas[etapa] = {
                "quantidade": registros.count()
            }

        status_projeto = {}

        for status in [
            StatusProjeto.PROJETO_ENVIADO,
            StatusProjeto.OBRA_CONGELADA,
            StatusProjeto.PEND_AMPLIAR_HL4,
            StatusProjeto.PEND_ATIVAR_HL4,
            StatusProjeto.PEND_BAYFACE,
            StatusProjeto.PEND_PROJETO_ENG,
            StatusProjeto.PORTAL
        ]:

            status_projeto[status] = facilidades.filter(
                status_projeto=status
            ).count()

        acoes = {}

        for acao in [
            Acao.NOVA_OLT,
            Acao.AMPLIACAO,
            Acao.AMP_NOVA
        ]:

            registros = facilidades.filter(
                acao=acao
            )

            acoes[acao] = {
                "total": registros.count(),
                "concluidos": registros.filter(
                    etapa_atual=Etapa.CONCLUIDO
                ).count(),
                "pendentes": registros.filter(
                    etapa_atual__ne=Etapa.CONCLUIDO
                ).count()
            }

        lista_pendencias = []

        for item in pendencias:

            lista_pendencias.append({
                "bc": item.bc,
                "site_id": item.site_id,
                "uf": item.uf,
                "localidade": item.localidade,
                "acao": item.acao,
                "etapa_atual": item.etapa_atual,
                "status_projeto": item.status_projeto,
                "hostname_olt": item.hostname_olt,
                "hostname_hl4": item.hostname_hl4,
                "responsavel": item.responsavel_atual,
                "analista": item.analista,
                "updated_at": item.updated_at,
                "obs": item.obs
            })

        lista_concluidos = []

        for item in conclusoes:

            lista_concluidos.append({
                "bc": item.bc,
                "site_id": item.site_id,
                "uf": item.uf,
                "localidade": item.localidade,
                "acao": item.acao,
                "etapa_atual": item.etapa_atual,
                "status_projeto": item.status_projeto,
                "hostname_olt": item.hostname_olt,
                "hostname_hl4": item.hostname_hl4,
                "responsavel": item.responsavel_atual,
                "analista": item.analista,
                "updated_at": item.updated_at,
                "obs": item.obs
            })

        return {
            "dashboard": dashboard,
            "etapas": etapas,
            "status_projeto": status_projeto,
            "acoes": acoes,
            "pendencias": lista_pendencias,
            "concluidos": lista_concluidos
        }
