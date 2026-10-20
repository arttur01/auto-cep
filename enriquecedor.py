#bibliotecas necessarias
import json
from urllib.error import HTTPError
from urllib.request import urlopen, Request


class Enriquecedor:
    '''Classe que vai trazer os dados do endereço com base no CEP informado.'''
    def request(self, cep: str) -> dict:
        # Limpeza e formatação do CEP
        cep_limpo = str(cep).split(".")[0]
        cep_limpo = cep_limpo.replace("-", "").replace(" ", "").strip()
        cep_limpo = cep_limpo.zfill(8)

        url = f"https://brasilapi.com.br/api/cep/v1/{cep_limpo}"     
        
        # oculta o agente do navegador para evitar bloqueios da API
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Montando a requisição com os cabeçalhos
        requis = Request(url, headers=headers)
        
        try:
            with urlopen(requis) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            return {
                "error": "Falha na busca",
                "motivo": f"A API rejeitou o CEP '{cep_limpo}'. Erro HTTP: {e.code}"
            }
        except Exception as e:
            return {
                "error": "Falha na conexão",
                "motivo": str(e)
            }

def processar_cep_uipath(cep: str) -> str:
    app = Enriquecedor()
    resultado = app.request(cep)
    return json.dumps(resultado)