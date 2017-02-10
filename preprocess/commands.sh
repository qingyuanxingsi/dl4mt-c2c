python ~/workspace/subword-nmt/learn_bpe.py -s 3000 < all_pi-pw.pi.tok > ../pi.bpe
python ~/workspace/subword-nmt/learn_bpe.py -s 3000 < all_pi-pw.pw.tok > ../pw.bpe
python ~/workspace/subword-nmt/apply_bpe.py -c ../pw.bpe < all_pi-pw.pw.tok > all_pi-pw.pw.tok.bpe
python ~/workspace/subword-nmt/apply_bpe.py -c ../pi.bpe < all_pi-pw.pi.tok > all_pi-pw.pi.tok.bpe
python ~/workspace/dl4mt-c2c/preprocess/shuffle.py all_pi-pw.pi.tok.bpe all_pi-pw.pw.tok.bpe all_pi-pw.pi.tok all_pi-pw.pw.tok
python /home/lanlin/workspace/dl4mt-c2c/preprocess/build_dictionary_word.py all_pi-pw.pi.tok.bpe
python /home/lanlin/workspace/dl4mt-c2c/preprocess/build_dictionary_word.py all_pi-pw.pw.tok.bpe
python ~/workspace/dl4mt-c2c/preprocess/build_dictionary_char.py all_pi-pw.pi.tok
python ~/workspace/dl4mt-c2c/preprocess/build_dictionary_char.py all_pi-pw.pw.tok