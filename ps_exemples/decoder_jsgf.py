#!/usr/bin/python

from os import environ, path
from sys import stdout

from pocketsphinx import *
from sphinxbase import *


def decode(decoder, filepath):
    decoder.start_utt()
    stream = open(filepath, 'rb')
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
    decoder.end_utt()


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm',  'ps_data/model/en-us')
config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
config.set_string('-dict', 'ps_data/lex/turtle.dic')
decoder = Decoder(config)

# Decode with lm
# filepath = "ps_data/example/goforward.raw"
filepath = "/home/devmood/private/uni/SEM3/speech/td_corpus_digits/SNR25dB/man/seq1digit_200_files/SNR25dB_man_seq1digit_001.raw"

decode(decoder, filepath)
print('Decoding with "turtle" language:', decoder.hyp().hypstr)

# print('')
# print('--------------')
# print('')
# 
# # Switch to JSGF grammar
# jsgf = Jsgf('ps_data/jsgf/goforward.gram')
# rule = jsgf.get_rule('goforward.move2')
# fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
# fsg.writefile('goforward.fsg')
# 
# decoder.set_fsg("goforward", fsg)
# decoder.set_search("goforward")
# 
# decode(decoder, filepath)
# print('Decoding with "goforward" grammar:', decoder.hyp().hypstr)
