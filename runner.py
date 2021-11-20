import os

from jiwer import wer

from pocketsphinx import *
from sphinxbase import *


def loop(decoder):
    base_path = "./td_corpus_digits"
    dirs = os.listdir(base_path)

    for dir in dirs:
        dir_tmp = os.path.join(base_path, dir)
        for speaker in os.listdir(dir_tmp):
            files = os.path.join(dir_tmp, speaker)
            for filedir in os.listdir(files):
                wer_sum, correct_cnt = 0, 0

                tmp_split = filedir.split("_")
                total_cnt = int(tmp_split[1])
                digits = int(
                    "".join([x for x in tmp_split[0] if x.isnumeric()]))

                files_tmp = os.path.join(files, filedir)
                for file in filter(lambda l: ".raw" in l, os.listdir(files_tmp)):
                    fullpath = os.path.join(files_tmp, file)

                    correct, wer = decode(fullpath)
                    correct_cnt += correct
                    wer_sum += wer

                log(correct_cnt, wer_sum, total_cnt, speaker, digits, dir)


def decode(fullpath):
    decoder.start_utt()

    raw = open(fullpath, "rb").read()
    reference = open(
        f".{''.join(fullpath.split('.')[:-1])}.ref").readline().strip()
    decoder.process_raw(raw, False, True)

    wer_sum, correct_cnt = 0, 0
    if decoder.hyp():
        hypothesis = decoder.hyp().hypstr.strip()
        correct_cnt = hypothesis == reference
        wer_sum = wer(reference, hypothesis)

    decoder.end_utt()

    return correct_cnt, wer_sum


def log(correct_cnt, wer_sum, total_cnt, speaker, digits, dir):
    # print(correct_cnt)
    # print(total_cnt)
    # print(wer_sum)

    error = round(1 - (correct_cnt / total_cnt), 4)
    wer = round(wer_sum, 4)
    print(f"{speaker} {digits} digits {dir}; error: {error}; wer: {wer}")


def init_decoder():
    # Create a decoder with certain model
    config = Decoder.default_config()
    config.set_string('-logfn', 'nul')
    config.set_string('-hmm',  'ps_data/model/en-us')
    config.set_string('-lm',   'ps_data/lm/turtle.lm.bin')
    config.set_string('-dict', 'ps_data/numbers.dic')
    decoder = Decoder(config)

    # Switch to JSGF grammar
    jsgf = Jsgf('ps_data/numbers.gram')
    rule = jsgf.get_rule('numbers.move')
    fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
    fsg.writefile('ps_data/numbers.fsg')

    # TODO: check if this one can be set on the fly dynamically to improve performance
    decoder.set_fsg("numbers", fsg)
    decoder.set_search("numbers")

    return decoder


if __name__ == "__main__":
    decoder = init_decoder()
    loop(decoder)
    os.remove("./nul")
