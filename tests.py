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


    # CRC generate
    crc_checksum = bluetooth.crc(message, True)
    message += crc_checksum


    # Whitening
    initial_whitening_register = ['1', '0', '1', '0', '1', '1', '1']
    register_to_work_on = ['0', '0', '0', '0', '0', '0', '0']
    whitening_message = bluetooth.whitening(message, initial_whitening_register, register_to_work_on)


    # FEC encode
    whitening_message += ['0', '0', '0', '0']
    fec_message = bluetooth.viterbi_encoder(whitening_message)


    # Pattern Mapper
    pm_message_p1 = bluetooth.pattern_mapper(fec_message, 1)
    pm_message_p4 = bluetooth.pattern_mapper(fec_message, 4)


    # Message distort
    distort_message_pm1 = bluetooth.distort_sequence(pm_message_p1, distortion_percent, distortion_location)
    distort_message_pm4 = bluetooth.distort_sequence(pm_message_p4, distortion_percent, distortion_location)

    # ------------------------------
    # ------------DECODE------------
    # ------------------------------

    # Pattern de-Mapper
    de_mapper_message_p1 = bluetooth.pattern_de_mapper(distort_message_pm1, 1)
    de_mapper_message_p4 = bluetooth.pattern_de_mapper(distort_message_pm4, 4)


    # FEC decode
    de_fec_message_p1 = bluetooth.viterbi_decoder(de_mapper_message_p1)
    de_fec_message_p1 = list(map(str, de_fec_message_p1[0:len(de_fec_message_p1) - 4]))

    de_fec_message_p4 = bluetooth.viterbi_decoder(de_mapper_message_p4)
    de_fec_message_p4 = list(map(str, de_fec_message_p4[0:len(de_fec_message_p4) - 4]))


    # dewhitening
    de_whitening_message_p1 = bluetooth.whitening(de_fec_message_p1, initial_whitening_register, register_to_work_on)
    de_whitening_message_p4 = bluetooth.whitening(de_fec_message_p4, initial_whitening_register, register_to_work_on)


    # CRC check
    result.append(bluetooth.crc(de_whitening_message_p1, False))
    result.append(bluetooth.crc(de_whitening_message_p4, False))

    return result


def run_tests():
    message_size = [10, 20, 40, 80, 160, 240, 480, 960, 1200, 2400]
    distortion_percent = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.15, 0.18, 0.20]
    distortion_location = [0, 1, 2, 3]

    # distortion location
    # 0 - beginning
    # 1 - mid
    # 2 - end
    # 3 - the whole range

    file = open('results.txt', 'w')

    for i in range(0, len(message_size)):
        for j in range(0, len(distortion_percent)):
            for k in range(0, len(distortion_location)):

                print("\n\nCurrent simulation state...")
                print("    message size: ", message_size[i])
                print(" distort_percent: ", distortion_percent[j])
                print("distort location: ", distortion_location[k])

                for l in range(0, 100):
                    results = transmission(message_size[i],  distortion_percent[j], distortion_location[k])
                    file.write(str(message_size[i]) + ";" + str(distortion_percent[j]) + ';' + str(distortion_location[k]) + ';' + str(results[0]) + ';' + str(results[1]) + '\n')

run_tests()
