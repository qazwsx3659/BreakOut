"""
File: complement.py
Name: Yu wen
----------------------------
This program uses string manipulation to tackle a real world problem -
finding the complement strand of a DNA sequence.
"""


def main():
    """
    This program finds the complement stand of a given DNA sequence.
    """
    print(build_complement('ATC'))
    print(build_complement(''))
    print(build_complement('ATGCAT'))
    print(build_complement('GCTATAC'))


def build_complement(dna: str) -> str:

    result = ''
    dna_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    for ch in dna:
        result += dna_dict[ch]

    if result:
        return result
    else:
        return 'DNA strand is missing'


if __name__ == '__main__':
    main()
