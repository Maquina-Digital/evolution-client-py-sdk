
from evolution_client.client import EvolutionApiClient

def test_init_client():
    c = EvolutionApiClient(base_url="https://evo", instance="Inst", api_key="k")
    assert c is not None
