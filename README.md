# dex-ExfilImageStego
Embeds data within a PNG image using LSB steganography. Takes data and an image as input, outputs a new PNG image containing the hidden data. - Focused on Simulates data exfiltration techniques by generating realistic fake data (e.g., usernames, passwords, financial records), staging it in various formats, and then simulating its transmission over different protocols (e.g., HTTP, DNS tunneling). Used for testing data loss prevention (DLP) systems and incident response playbooks.

## Install
`git clone https://github.com/ShadowStrikeHQ/dex-exfilimagestego`

## Usage
`./dex-exfilimagestego [params]`

## Parameters
- `-h`: Show help message and exit
- `-o`: Path to save the steganographically encoded PNG image.
- `-d`: Path to a file containing data to embed. If not provided, fake data is generated.
- `-g`: Generate fake data for embedding. Overrides --data_file.
- `-s`: No description provided
- `-e`: No description provided

## License
Copyright (c) ShadowStrikeHQ
