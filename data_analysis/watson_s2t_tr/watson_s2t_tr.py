#!/usr/bin/env python3
#
# Before to call this script be sure to define
# the following environment variables
#   S2T_APIKEY:  Watson Speech to text service API key
#   S2T_URL   :  Watson Speech to text service URL
#   LT_APIKEY : IBM Watson language translation service API key
#   LT_URL    : IBM Watson language translation service URL
#
# References:
#   https://cloud.ibm.com/apidocs/speech-to-text?code=python
#   https://cloud.ibm.com/apidocs/language-translator?code=python
#
import os
import sys
import json

from pandas import json_normalize
from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# ---------------------------------------------------
def main():
    if 'S2T_APIKEY' in os.environ:
        _s2t_apikey = os.environ.get('S2T_APIKEY')
    else:
        print("fatal: S2T_APIKEY not found in environment, cannot proceed")
        sys.exit(1)

    if 'S2T_URL' in os.environ:
        _s2t_url = os.environ.get('S2T_URL')
    else:
        print("fatal: S2T_URL not found in environment, cannot proceed")
        sys.exit(1)

    if 'LT_APIKEY' in os.environ:
        _lt_apikey = os.environ.get('LT_APIKEY')
    else:
        print("fatal: LT_APIKEY not found in environment, cannot proceed")
        sys.exit(1)

    if 'LT_URL' in os.environ:
        _lt_url = os.environ.get('LT_URL')
    else:
        print("fatal: LT_URL not found in environment, cannot proceed")
        sys.exit(1)



    # ---------------------------------------------------------------------
    # 1. Create a Speech To Text Adapter object.
    #    Parameters: the endpoint and API key
#    s2t_auth = IAMAuthenticator(_s2t_apikey)
#    s2t = SpeechToTextV1(authenticator=s2t_auth)
#    s2t.set_service_url(_s2t_url)
    #print(s2t)
    # <ibm_watson.speech_to_text_v1_adapter.SpeechToTextV1Adapter object at 0x7fc9c2354130>

    # 2. require the T2S service for the sample audio file
#    audiofile = 'PolynomialRegressionAndPipelines.mp3'
#    with open(audiofile, "rb") as afile:
#        response = s2t.recognize(audio=afile, content_type="audio/mp3")
#    json_normalize(response.result['results'], "alternatives")
#    print(response.result)
#    recognized_text = response.result['results'][0]['alternatives'][0]['transcript']
#    print(type(recognized_text))
#    print(recognized_text)

    # 3. Create the Language Translator object
    lt_version = '2018-05-01'
    lt_auth = IAMAuthenticator(_lt_apikey)
    lt = LanguageTranslatorV3(version=lt_version, authenticator=lt_auth)
    lt.set_service_url(_lt_url)
    langs = json_normalize(lt.list_identifiable_languages().get_result(), "languages")
    ##print(langs)
    #    language                 name
    # 0        af            Afrikaans
    # 1        ar               Arabic
    # 2        az          Azerbaijani
    # 3        ba              Bashkir
    # 4        be           Belarusian
    # ..      ...                  ...
    # 63       uk            Ukrainian
    # 64       ur                 Urdu
    # 65       vi           Vietnamese
    # 66       zh   Simplified Chinese
    # 67    zh-TW  Traditional Chinese

    #italian = langs[langs['language'] == 'it']
    #print(italian)
    #    language     name
    # 30       it  Italian

    text1 = "There is no universal best way to visualize data. Different questions are " \
        "best answered by different kinds of visualizations. Seaborn tries to make it easy " \
        "to switch between different visual representations that can be parameterized with " \
        "the same dataset-oriented API."

    tr = lt.translate(text=text1, model_id='en-it')
    tr_result = tr.get_result()
    #print(tr_result)
    # {
    #   'translations':
    #     [
    #       {
    #         'translation': "...<translated text>..."
    #       }
    #     ],
    #   'word_count': 40,
    #   'character_count': 268
    # }
    text_it = tr_result['translations'][0]['translation']
    print(text_it)

if __name__ == '__main__':
    main()

