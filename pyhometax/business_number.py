import requests
import xmltodict
import time


def check_business_number_status(business_number: str):
    _validate_format(business_number)
    response_xml = _request_to_hometax(business_number)
    response_message = _get_response_message(response_xml)

    return response_message


def _validate_format(business_number: str) -> None:
    if not business_number.isdecimal():
        raise ValueError('사업자번호는 숫자로만 이루어져야 합니다.')

    if len(business_number) != 10:
        raise ValueError('사업자번호는 10글자여야 합니다.')

    return


def _request_to_hometax(business_number: str) -> str:
    url = "https://teht.hometax.go.kr/wqAction.do"
    params = {
        "actionId": "ATTABZAA001R08",
    }
    payload = """
        <map id="ATTABZAA001R08">
            <inqrTrgtClCd>1</inqrTrgtClCd>
            <txprDscmNo>{}</txprDscmNo>
        </map>
    """.format(business_number)

    while True:
        response = requests.post(url, params=params, data=payload, timeout=5)
        response.raise_for_status()

        if '5초 후 부터 조회 가능합니다.' not in response.text:
            break
        time.sleep(5)

    return response.text


def _get_response_message(response_xml: str) -> str:
    response_dict = xmltodict.parse(response_xml)

    return response_dict['map']['trtCntn']
