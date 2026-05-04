### Training ASR Model with ESPnet

## Prepare data: train/valid/test

### Select train data
* We will use data from AIHub [[KsponSpeech]]. List of files are mode for convenience.
* 회원가입 및 로그인 -> 파일 목록(API 다운로드) 이동
* Download KsponSpeech_eval.zip and KsponSpeech_01.zip (optionally, download KsponSpeech_03.zip)
* 다운로드 완료 후
    ```
    cd ~/Downloads
    tar -xvf download.tar  # 압축 해제 후 여러개의 파일 생성됨
    mv 10.한국어음성 NIA2019_KSPONSPEECH
    cd NIA2019_KSPONSPEECH
    find ./ -name "KsponSpeech_01.zip.part*" -print0 | sort -zt'.' -k2V | xargs -0 cat > "01.zip"
    find ./ -name "KsponSpeech_eval.zip.part*" -print0 | sort -zt'.' -k2V | xargs -0 cat > "eval.zip"
    unzip 01.zip
    unzip eval.zip
    ```
* 데이터셋 정보가 담긴 파일 압축 해제
    ```
    cd ~/a1004/data/
    tar xvzf ks.tgz
    ```

* Change path in `~a1004/data/ks/wav.scp` and corrent it 
    ```
    sed -i 's,/path/to/db/,/some/correct/path,' ~/a1004/data/ks/wav.scp
    ```  

* Choose **one** of following 3 options:
    ```
    cd ~/a1004/data/ks
    cat uttid.01 > uttid.train
    ```
* or
    ```
    cd ~/a1004/data/ks
    cat uttid.01 uttid.03 > uttid.train
    ```
* or
    ```
    cd ~/a1004/data/ks
    cat uttid.01 uttid.03 uttid.05 > uttid.train
    ```
    
[KsponSpeech]: https://aihub.or.kr/aihubdata/data/view.do?currMenu=&topMenu=&aihubDataSe=realm&dataSetSn=123

## Prepare data directory
Prepare data director in Kaldi format. We need 4 files.

* `wav.scp`: mapping of utterence id to wav file path
* `text`: mapping of utterence id to transcription
* `utt2spk`: mapping of utterence id to speaker id
* `spk2utt`: mapping of speaker id to utterence id
    ```
    cd ~/a1004
    source path.sh
    ```
* generate train dir
    ```     
    mkdir -p data/train
    filter_scp.pl data/ks/uttid.train data/ks/wav.scp > data/train/wav.scp
    filter_scp.pl data/ks/uttid.train data/ks/text > data/train/text
    awk '{print $1 " " $1}' data/train/wav.scp > data/train/spk2utt
    cp data/train/spk2utt data/train/utt2spk
    ```

* generate dev dir
    ```
    mkdir -p data/dev
    filter_scp.pl data/ks/uttid.dev data/ks/wav.scp > data/dev/wav.scp
    filter_scp.pl data/ks/uttid.dev data/ks/text > data/dev/text
    awk '{print $1 " " $1}' data/dev/wav.scp > data/dev/spk2utt
    cp data/dev/spk2utt data/dev/utt2spk
    ```

* generate test dir
    ```
    mkdir -p data/test
    filter_scp.pl data/ks/uttid.test data/ks/wav.scp > data/test/wav.scp
    filter_scp.pl data/ks/uttid.test data/ks/text > data/test/text
    awk '{print $1 " " $1}' data/test/wav.scp > data/test/spk2utt
    cp data/test/spk2utt data/test/utt2spk
    ```

## Run training with asr.sh
Do it step by step (for convenience of explanation)

### run asr.sh: stage3-5

* Stage 3: `Format wav.scp: data/ -> dump/raw`
  - elapsed=1126s,93s,6s
* Stage 4: `Remove long/short data: dump/raw/org -> dump/raw`
* Stage 5:
  - `Generate character level token_list from dump/raw/org/train/text`
  - `Generate token_list from dump/raw/org/train/text using BPE`

* Edit `--stage 3` and `--stop_stage 5` in `train.sh`, then run:

        (venv)$ bash train.sh

Open `data/ko_token_list/char/tokens.txt` or `data/ko_token_list/bpe_unigram5000/tokens.txt`

### run asr.sh: stage10

* Stage 10: `ASR collect stats: train_set=dump/raw/train, valid_set=dump/raw/dev`
* Edit `--stage 10` and `--stop_stage 10` in `train.sh`, then run:

        (venv)$ bash train.sh

* `Successfully finished. [elapsed=1153s,240s]`
* See `asr_stats_`...

### run asr.sh: stage11

* Stage 11: `ASR Training: train_set=dump/raw/train, valid_set=dump/raw/dev`
* Edit `--stage 11` and `--stop_stage 11` in `train.sh`, then run:

        (venv)$ bash train.sh

### Monitoring training

* Run `nvidia-smi`

* See `exp/myasr/train.log`

        (venv)$ tail -f ~/a1004/exp/train.log

Output looks like:

        [hostname] 2026-04-23 04:59:09,396 (trainer:318) INFO: 1/30epoch started
        [hostname] 2026-04-23 04:59:25,764 (trainer:793) INFO: 1epoch:train:1-90batch: iter_time=0.003, forward_time=0.095, loss_ctc=557.480, loss_att=223.114, acc=4.043e-04, loss=80.856, backward_time=0.041, grad_norm=530.879, clip=100.000, loss_scale=1.000, optim_step_time=0.010, optim0_lr0=6.250e-07, train_time=0.734
        [hostname] 2026-04-23 04:59:37,331 (trainer:793) INFO: 1epoch:train:91-180batch: iter_time=4.780e-04, forward_time=0.055, loss_ctc=515.555, loss_att=220.957, acc=4.963e-04, loss=77.334, backward_time=0.032, grad_norm=616.627, clip=100.000, loss_scale=1.000, optim_step_time=0.003, optim0_lr0=1.750e-06, train_time=0.512
        [hostname] 2026-04-23 04:59:48,778 (trainer:793) INFO: 1epoch:train:181-270batch: iter_time=1.797e-04, forward_time=0.055, loss_ctc=413.005, loss_att=214.631, acc=4.955e-04, loss=68.536, backward_time=0.032, grad_norm=557.550, clip=100.000, loss_scale=1.000, optim_step_time=0.003, optim0_lr0=2.875e-06, train_time=0.508

## Testing

### Prepare Data

* Prepare files `wav.scp`,`text`,`spk2utt`,`utt2spk` in `data/mydata`

### Run
Edit `inference.sh` and run it.


# Pretrained models

* Training data

| model | training data | hours  | elapsed |
| ---   | ---           | ---    | ---     |
| 01    | 01            | 173.9h | 8h 8m   |
| 03    | 03            | 192.3h | 8h 55m  |
| 2x    | 01 + 03       | 366.3h | 16h 4m  |
| 3x    | 01 + 03 + 05  | 563.7h | 40h 50m (1080ti x1) |

* Path to models (obsolete)

        /path/to/a1004/models/ref01/valid.acc.ave_10best.pth
        /path/to/a1004/models/ref03/valid.acc.ave_10best.pth
        /path/to/a1004/models/ref2x/valid.acc.ave_10best.pth
        /path/to/a1004/models/ref3x/valid.acc.ave_10best.pth

