import urllib.parse

import mitmproxy.flow
import yaml

DOMAIN_CONFIG = 'domains.yml'

with open(DOMAIN_CONFIG, 'rb') as fp:
    domains = yaml.load(fp.read())


def urlparse_default_port(url):
    print(url)
    result = urllib.parse.urlparse(url)
    if result.port is None:
        url = url.rstrip('/')
        if result.scheme == 'http':
            return urllib.parse.urlparse(url + ':80')
        elif result.scheme == 'https':
            return urllib.parse.urlparse(url + ':443')
    return result


proxies = [[
    urlparse_default_port(proxy), [urlparse_default_port(origin) for origin in origins]
] for proxy, origins in domains['proxy'].items()]

# parse_results = map(urllib.parse.urlparse, domains['proxy'])


def is_match_flow_parse_result(flow: mitmproxy.flow.Flow,
                               parse_result: urllib.parse.ParseResult) -> bool:
    return bool(flow.request.scheme == parse_result.scheme
                and flow.request.host == parse_result.hostname
                and flow.request.port == parse_result.port)


def merge_flow_parse_result(flow: mitmproxy.flow.Flow,
                            parse_result: urllib.parse.ParseResult) -> bool:
    flow.request.scheme = parse_result.scheme
    flow.request.host = parse_result.hostname
    flow.request.port = parse_result.port
    flow.request.headers["Host"] = parse_result.hostname
    return flow


def set_flow_params(flow):
    for proxy, origins in proxies:
        for origin in origins:
            if is_match_flow_parse_result(flow, origin):
                return merge_flow_parse_result(flow, proxy)
    return flow


def http_connect(flow):
    set_flow_params(flow)


def request(flow):
    set_flow_params(flow)
