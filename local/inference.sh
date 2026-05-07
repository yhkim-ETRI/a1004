#!/bin/bash -eu

# Configuraiton
data=data/sample_data
#model=models/ma17k2401a/final.mdl
model=../exp/asr_train/valid.acc.ave_10best.pth
odir=results
conf=../conf/decode_asr.yaml
# End of Configuraiton

#[ -f ./utils/parse_options.sh ] && . ./utils/parse_options.sh

mkdir -p $odir/log

trnconfig=$(dirname $model)/config.yaml
python3 -m espnet2.bin.asr_inference --batch_size 1 --ngpu 0 \
    --data_path_and_name_and_type $data/wav.scp,speech,sound \
    --asr_train_config $trnconfig \
    --asr_model_file $model \
    --output_dir $odir \
    --config $conf
