import boto3
import json
import requests

from botocore.exceptions import ClientError

aws_firehose = boto3.client('firehose', region_name='us-west-1')


def get_bearer():
    secret_name = "twit_bearer_token"
    region_name = "us-west-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    bearer_token = get_secret_value_response['SecretString']

    return bearer_token


def bearer_oauth(r):
    # Sets headers for HTTP requests
    r.headers['Authorization'] = f"Bearer {get_bearer()}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(" Cannot get rules (HTTP {})".format(
            response.status_code, response.text))
    print("Rules currently in place: ")
    print(json.dumps(response.json()))
    return response.json()


def set_rules():
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "#FTX"}
        # {"value": "#doge"}
        # {"value: "meme has:images"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(
                response.status_code, response.text)
        )
    rules = (json.dumps(response.json()))
    print(rules)
    return rules


def get_stream():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print("Tweet stream starting...")
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    seqID = 1
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            aws_firehose.put_record(DeliveryStreamName="TWEETS-S3", Record={'Data': json.dumps(
                json_response, indent=4, sort_keys=True)})
            print(json.dumps(json_response, indent=4, sort_keys=True))
            seqID += 1


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def main():
    rules = get_rules()
    # rules in this case refers to thE rules you seek to delete and returns current rules left?
    delete = delete_all_rules(rules)
    rule_set = set_rules()
    get_stream()
    return 0


if __name__ == "__main__":
    main()
