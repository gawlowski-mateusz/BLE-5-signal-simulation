# Bluetooth 5 Simulation Project

This project aims to simulate Bluetooth Low Energy (BLE) 5 transmission, considering various parameters such as bit sequence length, mapping patterns, and error detection and correction mechanisms including CRC (Cyclic Redundancy Check), Whitening, Forward Error Correction (FEC), and Pattern Mapping. The simulation is implemented in Python and provides insights into transmission reliability across different channel parameters, aiding in finding optimal settings for effective data transfer in a BLE 5 network.

## Table of Contents

- [Project Components](#project-components)
  - [bluetooth.py](#bluetoothpy)
  - [demo.py](#demopy)
  - [tests.py](#testspy)
- [Usage](#usage)
- [Requirements](#requirements)
- [Authors](#authors)
- [License](#license)

## Project Components

### bluetooth.py

This module contains Python functions for various components of the simulation:

- **XOR function**: Computes the XOR operation between two binary inputs.
- **CRC function**: Implements CRC generation and verification for error detection.
- **Whitening / Dewhitening function**: Performs whitening and dewhitening operations to enhance data randomness.
- **Viterbi encoder and decoder functions**: Implements Forward Error Correction (FEC) using Viterbi encoding and decoding.
- **Pattern Mapper and de-Mapper functions**: Maps binary sequences to desired patterns and vice versa.
- **Distort sequence function**: Introduces distortion into the transmitted sequence for simulation purposes.

### demo.py

This script demonstrates the entire transmission process, from message generation to error detection and correction:

- Generates a message of specified size.
- Computes CRC checksum and appends it to the message.
- Performs whitening, FEC encoding, and pattern mapping.
- Introduces distortion to simulate transmission errors.
- Decodes the received message, performs FEC decoding, dewhitening, and verifies CRC to check for message integrity.

### tests.py

This script conducts systematic tests to evaluate the performance of the simulation under various conditions:

- Tests are conducted with different message sizes, distortion percentages, and distortion locations.
- Each test iteration involves generating a message, introducing distortion, decoding the received message, and verifying CRC.
- Results are logged to a file for further analysis.

## Usage

To run the demonstration script:

```bash
python demo.py
```

To conduct systematic tests:

```bash
python tests.py
```

## Requirements

- Python 3.x
- NumPy (for numerical computations)

## Authors

- [Mateusz Gawłowski](https://github.com/gawlowski-mateusz) - Student at Wroclaw University of Science and Technology

## License

This project is under open-source license that allows users to freely use, modify, and distribute the software for any purpose, including commercial purposes, without requiring payment or attribution. The license also includes a disclaimer of liability, stating that the software is provided "as is" without warranties. 