import argparse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pathlib
import json


def parse_arguments():
    desc = 'An OSINT tool for gathering information about phone numbers.'

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-n', '--number', type=str, action='store',
                        required=True,
                        help='Enter Phone Number')

    parser.add_argument('-o', '--output', type=str, action='store',
                        required=True,
                        help='Output file')

    args = parser.parse_args()
    return args


def loop(phone_number):
    """
    Validate Number.
    If valid:
    Get basic Info + Get The Internet Service Provider(ISP)
    Save to .json file (list of dictionaries)
    """
    result = []

    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number

    try:
        parse = phonenumbers.parse(phone_number)

    except phonenumbers.NumberParseException as e:
        print(f"Invalid code number: {e}")

        result.append({"is_valid": False})
        return result

    is_valid_number = phonenumbers.is_valid_number(parse)

    if is_valid_number is True:
        print(f"Number {phone_number} is valid! Collecting Info ...")
        is_valid = True

        region = geocoder.description_for_number(parse, 'en', None)
        if not region:
            region = ""

        number_timezone = timezone.time_zones_for_number(parse)
        if number_timezone:
            number_timezone = number_timezone[0]
        else:
            number_timezone = ""

        isp = carrier.name_for_number(parse, 'en')
        if not isp:
            isp = ""

        result.append(
            {"is_valid": is_valid,
             "region": region,
             "timezone": number_timezone,
             "internet_service_provider": isp
             })

        print(f"Info collected! Result: {result}")
        return result

    else:
        print(f"Number {phone_number} is NOT valid! Exiting ...")
        result.append({"is_valid": False})
        return result


def main():
    args = parse_arguments()
    outputFile = args.output
    phone_number = args.number

    result_output = loop(phone_number)

    root_path = pathlib.Path(__file__).parent
    file_path = root_path.joinpath(outputFile)
    file_path.write_text(json.dumps(result_output))


if __name__ == "__main__":
    main()
