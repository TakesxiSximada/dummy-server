import urllib.parse

import mitmproxy.flow
import yaml

DOMAIN_CONFIG = 'domains.yml'

with open(DOMAIN_CONFIG, 'rb') as fp:
    domains = yaml.load(fp.read())

parse_results = map(urllib.parse.urlparse, domains['proxy'])


def is_match_flow_parse_result(flow: mitmproxy.flow.Flow,
                               parse_result: urllib.parse.ParseResult) -> bool:
    return bool(flow.request.scheme == parse_result.scheme
                and flow.request.host == parse_result.netloc
                and flow.request.port == parse_result.port)


def merge_flow_parse_result(flow: mitmproxy.flow.Flow,
                            parse_result: urllib.parse.ParseResult) -> bool:
    flow.request.scheme = parse_result.scheme
    flow.request.host = parse_result.netloc
    flow.request.port = parse_result.port
    flow.request.headers["Host"] = [flow.request.host]
    return flow


def set_flow_params(flow):
    for parse_result in parse_results:
        if is_match_flow_parse_result(flow, parse_result):
            merge_flow_parse_result(flow, parse_result)
            return flow
    return flow


def http_connect(flow):
    set_flow_params(flow)


def request(flow):
    set_flow_params(flow)
