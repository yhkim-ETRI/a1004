#!/usr/bin/env python
# coding: utf-8

import editdistance

ref_text = "오늘 서울의 날씨가 어때"
hyp_text = "음 오늘의 날씨 가 어때"

ref = ref_text.split()
hyp = hyp_text.split()
print(ref, hyp, sep='\n')

E = editdistance.eval(ref, hyp)
N = len(ref)
WER = E/N*100
print(f"N={N}, E={E}, WER={WER}")

ref = list(ref_text)
hyp = list(hyp_text)
print(ref, hyp, sep='\n')

E = editdistance.eval(ref, hyp)
N = len(ref)
CER = E/N*100
print(f"N={N}, E={E}, CER={CER}")

ref = list(''.join(ref_text.split()))
hyp = list(''.join(hyp_text.split()))
print(ref, hyp, sep='\n')

E = editdistance.eval(ref, hyp)
N = len(ref)
CER = E/N*100
print(f"N={N}, E={E}, CER={CER}")
