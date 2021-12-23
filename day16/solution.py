import math

hex_string = "E054831006016008CF01CED7CDB2D495A473336CF7B8C8318021C00FACFD3125B9FA624BD3DBB7968C0179DFDBD196FAE5400974A974B55C24DC580085925D5007E2D49C6579E49252E28600B580272379054AF57A54D65E1586A951D860400434E36080410926624D25458890A006CA251006573D2DFCBF4016919CC0A467302100565CF24B7A9C36B0402840002150CA3E46000042621C108F0200CC5C8551EA47F79FC28401C20042E0EC288D4600F42585F1F88010C8C709235180272B3DCAD95DC005F6671379988A1380372D8FF1127BDC0D834600BC9334EA5880333E7F3C6B2FBE1B98025600A8803F04E2E45700043E34C5F8A72DDC6B7E8E400C01797D02D002052637263CE016CE5E5C8CC9E4B369E7051304F3509627A907C97BCF66008500521395A62553A9CAD312A9CCCEAF63A500A2631CCD8065681D2479371E4A90E024AD69AAEBE20002A84ACA51EE0365B74A6BF4B2CC178153399F3BACC68CF3F50840095A33CBD7EF1393459E2C3004340109596AB6DEBF9A95CACB55B6F5FCD4A24580400A8586009C70C00D44401D8AB11A210002190DE1BC43872C006C45299463005EC0169AFFF6F9273269B89F4F80100507C00A84EB34B5F2772CB122D26016CA88C9BCC8BD4A05CA2CCABF90030534D3226B32D040147F802537B888CD59265C3CC01498A6B7BA7A1A08F005C401C86B10A358803D1FE24419300524F32AD2C6DA009080330DE2941B1006618450822A009C68998C1E0C017C0041A450A554A582D8034797FD73D4396C1848FC0A6F14503004340169D96BE1B11674A4804CD9DC26D006E20008747585D0AC001088550560F9019B0E004080160058798012804E4801232C0437B00F70A005100CFEE007A8010C02553007FC801A5100530C00F4B0027EE004CA64A480287C005E27EEE13DD83447D3009E754E29CDB5CD3C"

binary_value = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}
binary_string = "".join([binary_value[x] for x in hex_string])

i = 0


def read(amount: int) -> int:
    global i
    result = binary_string[i:i + amount]
    i += amount
    return int(result, 2)


total_packet_versions = 0


def parse_packet() -> int:
    global total_packet_versions, i

    packet_version = read(3)
    total_packet_versions += packet_version
    type_id = read(3)

    if type_id == 4:
        return parse_number()
    else:
        sub_packets = []
        type_length_id = read(1)
        if type_length_id == 0:
            sub_packets_length = read(15)
            start_i = i
            while i < start_i + sub_packets_length:
                sub_packets.append(parse_packet())
        else:
            n_sub_packets = read(11)
            for _ in range(n_sub_packets):
                sub_packets.append(parse_packet())

        if type_id == 0:
            return sum(sub_packets)
        elif type_id == 1:
            return math.prod(sub_packets)
        elif type_id == 2:
            return min(sub_packets)
        elif type_id == 3:
            return max(sub_packets)
        elif type_id == 5:
            return sub_packets[0] > sub_packets[1]
        elif type_id == 6:
            return sub_packets[0] < sub_packets[1]
        elif type_id == 7:
            return sub_packets[0] == sub_packets[1]
        else:
            assert False


def parse_number():
    result = 0
    while read(1) == 1:
        result = 16 * result + read(4)

    result = 16 * result + read(4)
    return result


result = parse_packet()
print(f"Part 1: {total_packet_versions}")
print(f"Part 2: {result}")
