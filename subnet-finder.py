import re
from ipaddress import IPv4Address
from math import floor, log2
from socket import IPPROTO_IPV4
from telnetlib import IP


class CustomIPManager(IPv4Address):
    @classmethod
    def from_binary_repr(cls, binary_repr: str):
        """Construct IPv4 from binary representation.

        args:
            binary_repr: str
                Binary representation of IPv4 address
        returns:
            IPv4Address
        """
        # Remove anything that's not a 0 or 1
        i = int(re.sub(r"[^01]", "", binary_repr), 2)
        return cls(i)

    @classmethod
    def find_first_different_bit(cls, first_ip, second_ip) -> int:
        """Finds the first different bit position of two IPv4 addresses
        args:
            first_ip: str
                First IPv4 address
            second_ip: str
                Second IPv4 address
        returns:
            int
                Position of the first different bit
        """

        if first_ip == second_ip:
            return 0

        first_ip = int(first_ip)
        second_ip = int(second_ip)

        first_ip_bit_count = floor(log2(first_ip)) + 1
        second_ip_bit_count = floor(log2(second_ip)) + 1

        bit_diff = abs(first_ip_bit_count - second_ip_bit_count)
        max_bit_count = max(first_ip_bit_count, second_ip_bit_count)

        if first_ip_bit_count > second_ip_bit_count:
            second_ip *= pow(2, bit_diff)
        else:
            first_ip *= pow(2, bit_diff)

        xor_val = first_ip ^ second_ip
        bit_count_xor_val = floor(log2(xor_val)) + 1
        different_bit_position = max_bit_count - bit_count_xor_val + 1

        return different_bit_position

    @classmethod
    def first_different_pos_to_binary_ipv4(cls, int_pos):
        """Create a binary representation according to first similar bits position

        For example:
        if first_different_bit_pos is 3,
        then the binary representation is 11100000000000000000000000000000
        """
        binary = ""
        for i in range(32):
            if i < int_pos:
                binary += "1"
            else:
                binary += "0"
        return binary

    @classmethod
    def find_smallest(cls, ip_list):
        """Find the smallest IPv4 address in a list of IPv4 addresses"""
        smallest_ip = ip_list[0]
        for ip in ip_list:
            if ip < smallest_ip:
                smallest_ip = ip
        return smallest_ip

    @classmethod
    def find_largest(cls, ip_list):
        """Find the largest IPv4 address in a list of IPv4 addresses"""
        largest_ip = ip_list[0]
        for ip in ip_list:
            if ip > largest_ip:
                largest_ip = ip
        return largest_ip


class MinimalSubnetFinder:
    def __init__(self, ip_list):
        self.ip_list = list(map(lambda ip: IPv4Address(ip), ip_list))
        print(self.ip_list)

    def find(self):
        first_different_bit_pos = CustomIPManager.find_first_different_bit(
            self.ip_list[0], self.ip_list[1]
        )

        print(first_different_bit_pos)
        binary_result = CustomIPManager.first_different_pos_to_binary_ipv4(
            first_different_bit_pos
        )
        print(binary_result)

        print(CustomIPManager.from_binary_repr(binary_result))


if __name__ == "__main__":
    ip_list = ["128.42.5.17", "128.42.5.67", "192.160.2.0"]
    subnet_finder = MinimalSubnetFinder(ip_list)
    subnet_finder.find()
