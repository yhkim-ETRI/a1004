## python venv 환경 사용 (conda, miniforge 사용 X)

* Python version check (python 3.10 이상 권장)
    ```          
    python3 --version
    ```
    
* Install python-venv, python-dev
    ```
    # Daemons 관련 메세지 표출 시 Tab 키로 OK 이동 후 엔터
    sudo apt install python3.10-venv
    sudo apt install python3.10-dev
    # 설치 오류 발생 시
    sudo add-apt-repository --remove ppa:deadsnakes/ppa
    ```

## Install ESPnet
See [ESPnet Installation] page.

* clone source
    ```
    cd
    git clone -b v.202604 https://github.com/espnet/espnet
    ```

* setup python venv
    ```
    ./setup_venv.sh $(command -v python3)
    source activate_python.sh
    ```

* install torch, torchaudio
    ```
    pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
    ```

* install espnet asr
    ```
    (중요) pyproject.toml 파일에서 torch, torchaudio 부분 주석 처리
    pip install -e ".[asr]"
    pip install resampy
    ```

* check installation
    ```
    cd tools
    bash -c ". ./activate_python.sh; python3 check_install.py"
    ```

[ESPnet Installation]: https://espnet.github.io/espnet/installation.html

## Now download a1004

* clone source
    ```
    cd
    git clone https://github.com/yhkim-ETRI/a1004.git
    ```

* make soft link
    ```
    cd ~/a1004
    ln -sf ~/espnet/egs2/TEMPLATE/asr1/{steps,utils,pyscripts,scripts} .
    ```
    
* Edit `path.sh`, then

        $ source path.sh
        (venv)$ ls

