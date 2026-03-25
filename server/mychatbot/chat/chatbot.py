from .slm import slm_response

def get_response(sentence: str) -> str:
    return slm_response(sentence)