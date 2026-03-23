from f_google.services.gemini import Gemini, ResponseGemini


def test_ask() -> None:
    """
    ========================================================================
     Test ask() returns a valid ResponseGemini.
    ========================================================================
    """
    gemini = Gemini.Factory.rami()
    response = gemini.ask(prompt='Reply with only the number: 2+2=')
    assert isinstance(response, ResponseGemini)
    assert response.text.strip() == '4'
    assert response.finish_reason == 'STOP'
