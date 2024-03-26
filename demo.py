import random
import bluetooth

def transmission(message_size, distortion_percent, distortion_location):
    # Generate message
    message = []
    result = []

    for i in range(0, message_size):
        if random.randint(0, 1) % 2 == 0:
            message += '1'
        else:
            message += '0'

    print("\n\n######################################")
    print("# Generated message")
    print("######################################\n")
    print(message)


    # CRC
    crc_checksum = bluetooth.crc(message, True)
    message += crc_checksum

    print("\n\n######################################")
    print("# CRC checksum")
    print("######################################\n")
    print(crc_checksum)

    print("\n\n######################################")
    print("# Message + CRC checksum")
    print("######################################\n")
    print(message)


    # Whitening
    initial_whitening_register = ['1', '0', '1', '0', '1', '1', '1']
    register_to_work_on = ['0', '0', '0', '0', '0', '0', '0']
    whitening_message = bluetooth.whitening(message, initial_whitening_register, register_to_work_on)

    print("\n\n######################################")
    print("# Whitening message")
    print("######################################\n")
    print(whitening_message)


    # FEC encode
    whitening_message += ['0', '0', '0', '0']
    fec_message = bluetooth.viterbi_encoder(whitening_message)

    print("\n\n######################################")
    print("# FEC message")
    print("######################################\n")
    print(fec_message)


    # Pattern Mapper
    pm_message_p1 = bluetooth.pattern_mapper(fec_message, 1)
    pm_message_p4 = bluetooth.pattern_mapper(fec_message, 4)
    
    print("\n\n######################################")
    print("# Patterm Mapper ->> P=1")
    print("######################################\n")
    print(pm_message_p1)
    
    print("\n\n######################################")
    print("# Pattern Mapper ->> P=4")
    print("######################################\n")
    print(pm_message_p4)


    # Distort message
    distort_message_pm1 = bluetooth.distort_sequence(pm_message_p1, distortion_percent, distortion_location)
    distort_message_pm4 = bluetooth.distort_sequence(pm_message_p4, distortion_percent, distortion_location)
    
    print("\n\n######################################")
    print("# Distorted message ->> P=1")
    print("######################################\n")
    print(distort_message_pm1)
    
    print("\n\n######################################")
    print("# Distorted message ->> P=4")
    print("######################################\n")
    print(distort_message_pm4)


    # ------------------------------
    # ------------DECODE------------
    # ------------------------------
    print("\n\n\n############################################################################")
    print("# DECODE")
    print("############################################################################\n")


    # Pattern de-Mapper
    de_mapper_message_p1 = bluetooth.pattern_de_mapper(distort_message_pm1, 1)
    de_mapper_message_p4 = bluetooth.pattern_de_mapper(distort_message_pm4, 4)

    print("\n\n######################################")
    print("# De-Pattern Mapper ->> P=1")
    print("######################################\n")
    print(de_mapper_message_p1)
    print(de_mapper_message_p1 == pm_message_p1)
    
    print("\n\n######################################")
    print("# De-Pattern Mapper ->> P=4")
    print("######################################\n")
    print(de_mapper_message_p4)
    print(de_mapper_message_p4 == pm_message_p4)


    # FEC encode
    de_fec_message_p1 = bluetooth.viterbi_decoder(de_mapper_message_p1)
    de_fec_message_p1 = list(map(str, de_fec_message_p1[0:len(de_fec_message_p1) - 4]))
    de_fec_message_p4 = bluetooth.viterbi_decoder(de_mapper_message_p4)
    de_fec_message_p4 = list(map(str, de_fec_message_p4[0:len(de_fec_message_p4) - 4]))

    print("\n\n######################################")
    print("# De-FEC ->> P=1")
    print("######################################\n")
    print(de_fec_message_p1)
    
    print("\n\n######################################")
    print("# De-FEC ->> P=4")
    print("######################################\n")
    print(de_fec_message_p4)


    # Dewhitening
    de_whitening_message_p1 = bluetooth.whitening(de_fec_message_p1, initial_whitening_register, register_to_work_on)
    de_whitening_message_p4 = bluetooth.whitening(de_fec_message_p4, initial_whitening_register, register_to_work_on)

    print("\n\n######################################")
    print("# De-Whitening ->> P=1")
    print("######################################\n")
    print(de_whitening_message_p1)
    
    print("\n\n######################################")
    print("# De-Whitening ->> P=4")
    print("######################################\n")
    print(de_whitening_message_p4)


    # CRC check
    print("\n\n######################################")
    print("# CRC check ->> P=1")
    print("######################################\n")
    print("Is final message similar to original? ", bluetooth.crc(de_whitening_message_p1, False))

    print("\n\n######################################")
    print("# CRC check ->> P=4")
    print("######################################\n")
    print("Is final message similar to original? ", bluetooth.crc(de_whitening_message_p4, False))

    print()


def run_demo():

    # distortion location
    # 0 - beginning
    # 1 - mid
    # 2 - end
    # 3 - the whole range

    message_size = 20
    distortion_percent = 0.02
    distortion_location = 1

    transmission(message_size, distortion_percent, distortion_location)

run_demo()