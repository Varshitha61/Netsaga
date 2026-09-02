import pytest
from checker.rule_checker import check_ip_gateway_mismatch

def test_ip_gateway_mismatch_detected():
    output = """
    PC1> ipconfig
    IPv4 Address....................: 192.168.10.10
    Default Gateway.................: 0.0.0.0
    """
    assert check_ip_gateway_mismatch(output) is True

def test_ip_gateway_mismatch_not_detected():
    output = """
    PC1> ipconfig
    IPv4 Address....................: 192.168.10.10
    Default Gateway.................: 192.168.10.1
    """
    assert check_ip_gateway_mismatch(output) is False

def test_ip_gateway_mismatch_empty():
    output = """
    PC1> ping 8.8.8.8
    Timeout.
    """
    assert check_ip_gateway_mismatch(output) is False
