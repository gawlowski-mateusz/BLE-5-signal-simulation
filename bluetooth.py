import random
import copy


#######################################
# XOR function
#######################################

def xor(a, b):
    if a == b:
        return '0'
    else:
        return '1'


###############################################
# CRC function
###############################################

def crc(message, switch):
    crc_code = ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '1', '1', '0', '1', '1']
    message_copy = copy.copy(message)
    code_length = len(crc_code)

    if switch:
        for p in range(0, 24):
            message_copy += '0'
    else:
        message_copy = message_copy[0:len(message_copy) - 24]
        for p in range(0, 24):
            message_copy += '0'

    data_length = len(message_copy)

    for k in range(0, data_length - code_length):
        if message_copy[k] == '1':
            for n in range(0, code_length):
                message_copy[k + n] = xor(message_copy[k + n], crc_code[n])

    if switch:
        return message_copy[-24:]
    else:
        return message[-24:] == message_copy[-24:]


######################################
# Whitening / Dewhitening function
######################################

def whitening(input_message, register_before, register_after):
    output_message_p4 = []
    iterations_number = len(input_message)
    register_length = len(register_before)

    for i in range(0, iterations_number):
        output_message_p4 += xor(input_message[i], register_before[6])

        for j in range(1, register_length):
            register_after[j] = register_before[j - 1]

        register_after[4] = xor(register_before[3], register_before[6])
        register_after[0] = register_before[6]

        register_before = register_after
        register_after = ['', '', '', '', '', '', '']

    return output_message_p4


######################################
# Viterbi encoder function - FEC encode
######################################

def viterbi_encoder(input):
    register = ['0', '0', '0']
    output_message_p4 = []

    for i in range(0, len(input)):
        output_message_p4.append(xor(xor(xor(input[i], register[0]), register[1]), register[2]))
        output_message_p4.append(xor(xor(input[i], register[1]), register[2]))
        register[2] = register[1]
        register[1] = register[0]
        register[0] = input[i]

    return output_message_p4


##############################
# Pattern Mapper function
##############################

def pattern_mapper(input_message, pattern_schema):
    global output_p4

    if pattern_schema == 1:
        return input_message

    if pattern_schema == 4:
        output_length = len(input_message)
        output_p4 = []

        for i in range(0, output_length):
            if input_message[i] == '0':
                output_p4 += '0011'
            else:
                output_p4 += '1100'

    return output_p4


##############################
# Distort sequence function
##############################

def distort_sequence(message, distortion_percent, distortion_location):

    # distortion_location
    # 0 - beginning
    # 1 - middle
    # 2 - end
    # 3 - the whole range
    
    changed = []
    bits_to_distort = int((len(message)) * distortion_percent)

    distortion_begin = 0
    distortion_end = len(message) - 1

    if distortion_location == 0:
        distortion_end = bits_to_distort - 1
    elif distortion_location == 1:
        middle = int(len(message) / 2)
        middle_distortion = int(bits_to_distort / 2)
        distortion_end = middle + middle_distortion
        distortion_begin = middle - middle_distortion
    elif distortion_location == 2:
        distortion_begin = len(message) - bits_to_distort - 1

    for i in range(0, bits_to_distort - 1):
        position = random.randint(distortion_begin, distortion_end)

        if position not in changed:
            if message[position] == '0':
                message[position] = '1'
            else:
                message[position] = '0'
        else:
            i -= 1

    return message


##############################
# Pattern de-Mapper function
##############################

def pattern_de_mapper(input_message, pattern_schema):
    global output_p4
    
    if pattern_schema == 1:
        output_message_p1 = []

        for i in range(0, len(input_message), 2):
            bit_pair = input_message[i] + input_message[i + 1]
            output_message_p1.append(bit_pair)

        return output_message_p1

    if pattern_schema == 4:
        input_length = len(input_message)
        output_p4 = []

        for i in range(0, input_length, 4):

            hamming_distance_0011 = 4
            hamming_distance_1100 = 4

            # 1 of 4 bytes
            if input_message[i] == '0':
                hamming_distance_0011 -= 1
            else:
                hamming_distance_1100 -= 1

            # 2 of 4 bytes
            if input_message[i + 1] == '0':
                hamming_distance_0011 -= 1
            else:
                hamming_distance_1100 -= 1

            # 3 of 4 bytes
            if input_message[i + 2] == '0':
                hamming_distance_0011 -= 1
            else:
                hamming_distance_1100 -= 1

                # 4 of 4 bytes
                if input_message[i + 3] == '0':
                    hamming_distance_0011 -= 1
                else:
                    hamming_distance_1100 -= 1

            if hamming_distance_1100 < hamming_distance_0011:
                output_p4 += '1'
            else:
                output_p4 += '0'

    output_message_p4 = []

    for j in range(0, len(output_p4), 2):
        bit_pair = output_p4[j] + output_p4[j + 1]
        output_message_p4.append(bit_pair)

    return output_message_p4


###############################################
# Viterbi decoder function - FEC decode
###############################################

def bits_differences_number(bit_1, bit_2):
    count = 0

    for i in range(0, len(bit_1), 1):
        if bit_1[i] != bit_2[i]:
            count += 1

    return count


def viterbi_decoder(input_message):
    start_metric = {'zero': 0, 'one': 0, 'two': 0, 'three': 0, 'four': 0, 'five': 0, 'six': 0, 'seven': 0}
    machine_state = {
        # current state, possible branches, branch information
        'zero':  {'b1': {'out_b': "11", 'prev_st': 'one',   'input_b': 0},
                  'b2': {'out_b': "00", 'prev_st': 'zero',  'input_b': 0}},
        'one':   {'b1': {'out_b': "00", 'prev_st': 'three', 'input_b': 0},
                  'b2': {'out_b': "11", 'prev_st': 'two',   'input_b': 0}},
        'two':   {'b1': {'out_b': "10", 'prev_st': 'four',  'input_b': 0},
                  'b2': {'out_b': "01", 'prev_st': 'five',  'input_b': 0}},
        'three': {'b1': {'out_b': "01", 'prev_st': 'six',   'input_b': 0},
                  'b2': {'out_b': "10", 'prev_st': 'seven', 'input_b': 0}},
        'four':  {'b1': {'out_b': "11", 'prev_st': 'zero',  'input_b': 1},
                  'b2': {'out_b': "00", 'prev_st': 'one',   'input_b': 1}},
        'five':  {'b1': {'out_b': "00", 'prev_st': 'two',   'input_b': 1},
                  'b2': {'out_b': "11", 'prev_st': 'three', 'input_b': 1}},
        'six':   {'b1': {'out_b': "01", 'prev_st': 'four',  'input_b': 1},
                  'b2': {'out_b': "10", 'prev_st': 'five',  'input_b': 1}},
        'seven': {'b1': {'out_b': "10", 'prev_st': 'six',   'input_b': 1},
                  'b2': {'out_b': "01", 'prev_st': 'seven', 'input_b': 1}},
    }

    # global t
    viterbi = [{}]

    for state in machine_state:
        viterbi[0][state] = {"metric": start_metric[state]}

    for t in range(1, len(input_message) + 1):
        viterbi.append({})

        for state in machine_state:
            prev_st = machine_state[state]['b1']['prev_st']
            first_b_metric = viterbi[(t - 1)][prev_st]["metric"] + bits_differences_number(machine_state[state]['b1']['out_b'], input_message[t - 1])
            prev_st = machine_state[state]['b2']['prev_st']
            second_b_metric = viterbi[(t - 1)][prev_st]["metric"] + bits_differences_number(machine_state[state]['b2']['out_b'], input_message[t - 1])

            if first_b_metric > second_b_metric:
                viterbi[t][state] = {"metric": second_b_metric, "branch": 'b2'}
            else:
                viterbi[t][state] = {"metric": first_b_metric, "branch": 'b1'}

    smaller = min(viterbi[t][state]["metric"] for state in machine_state)
    output_message_p4 = []

    for state in machine_state:
        if viterbi[len(input_message) - 1][state]["metric"] == smaller:
            source_state = state

            for t in range(len(input_message), 0, -1):
                branch = viterbi[t][source_state]["branch"]
                output_message_p4.append(machine_state[source_state][branch]['input_b'])
                source_state = machine_state[source_state][branch]['prev_st']

    return output_message_p4[::-1]
