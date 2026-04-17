#!/usr/bin/env python3
"""反向解码 x-s-common：自定义 Base64 → 标准 Base64 → UTF-8 → JSON"""
import base64
import json
import os
import sys

CUSTOM = "ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5"
STANDARD = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# 构建映射表
char_map = {}
for i, c in enumerate(CUSTOM):
    char_map[c] = STANDARD[i]


def decode_xs_common(encoded):
    """自定义 Base64 → 标准 Base64 → bytes → UTF-8"""
    standard_b64 = ""
    for ch in encoded:
        if ch == "=":
            standard_b64 += "="
        elif ch in char_map:
            standard_b64 += char_map[ch]
        else:
            standard_b64 += ch  # 未知字符保留
    raw_bytes = base64.b64decode(standard_b64)
    return raw_bytes.decode("utf-8", errors="replace")


# 浏览器真实的子评论请求 x-s-common (reqid=3866, 返回200) — 完整值
browser_sub = "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1PUhlHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHMN0rlN0ZjNsQh+aHCH0rEGAqAGAqAGfpfy9YC2opT2oSTyfMEy7iEJ9E3qezIPoYxynhl+nk1+/ZIPeZUweZlP0rjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafpDwLMra7pFLDDAa7+8J7QgabmFz7Qjy/mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfRSL98lnLYl49IUqgcMc0mrJFShtMmozBD6qM8FyFShPo+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrLhaB8l4LShyBEl20YdanTQ8fRl49TQcMkgzAqAq9zV/9pnLoqAag8m8/mf89pDPBTtanDMqA+QqDGU4gzmanSNq9SD4fp3nDESpbmF+BEm/9pgLo4bag88Gn+m8Bp/4g4bqrQ6q98c47QQPMQUagYb+LlM474Yqgq3qfp3ybkm/fLl/LESPbm7wLSe/d+n/BRSL9QQzDS3J7+/q04ApfEByLS387+npdz+anSM8obl4UTFqgzga/PI8/+c49kQzLESpb8FyrSiN7+8qgz/z7b72nMc4FzQ4DS3a/+Q4ezYzMPFnaRSygpFyDSkJgQQzLRALM8F2DQ6zDF6wg8Sy0Sy4DSkzLEo4gzCqdpFJrS94fLALozp/7mN8p8gcgPAqBY7anY6qAPE/7PA4gzAGMm7GLSead+gLoqManSd8nTSqLlQcFTSyfc6q98c4epQ2e4A2op7zezTzBEQynHFagYw8/P6Po+LGg8A8rSS8nTc4FQQyb+haL+B+aRc47+QPMmBanSO8/+8wrMCqFkSp7pF8LSbtUTI4g4QJpkS8nz+cnpgpd4TJgpFPDSk//SQyBYz/bm7a0Yl4omQPApAzrbd8Lzc49z1pdzxaLp82pbM4eQQy7QCJAml4LS38g+nJA8APe4N8/8n4F8HpdzwanScLLS3J7P9pdzaaLp98pSfwo+QybSALLSVnrSbz0YQ2o8SPop72BRM4BROqgzha/+ryFSi+d+/cLESpS87yomUzDMQcFcFa7pFyBpn4BRQ2ob3a/PF/rS3L9SQz/8SygHMqM8I20bjpd4taL+Pzn+M4FlUpd4+aLp98p8+asRQ2r4tqgmN8gYn4bi34gcELBb0pMmByLpQy/Wl2S87tFS3+7P920zSanS8LnMn4e4QygrRHjIj2eDjw0rMPeGUPec9w/ZVHdWlPsHCPsIj2erlH0ijJfRUJnbVHjIj2erUH0ijP/q7P0ZI+ADIPArFP/Vl+AGEPeqFP/DAP/cMHdF="

# 我们生成的 x-s-common
our_xs_common = "2UQAPsHCHd4kJ0PUHjIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQccUHVHdWAH0ij2BYANgm0Ng4SGjHVHdWFH0ij+sh7wahIHjIj2eLjwjHlwnP7P9P7P9QS8fTi2dYMJgYEJnkT2nTCwnR1y7ZFqemhyfS1P/pxJ0LIPeZIP0WIP/HlHjIj2eGjwjHjNsQh+UHCHjHVHdWhH0ijHjIj2eDjwjHAw/WhP0DUPAWFHjIj2erIH0ilNsQhP/rjwjQ1J7QTGnIjKc=="

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decode_output.txt")

with open(out_path, "w", encoding="utf-8") as f:
    for label, data in [
        ("浏览器子评论 x-s-common (reqid=3866)", browser_sub),
        ("我们生成的 x-s-common", our_xs_common),
    ]:
        f.write(f"\n{'='*60}\n")
        f.write(f"{label}\n")
        f.write(f"{'='*60}\n")
        f.write(f"编码长度: {len(data)} 字符\n\n")

        try:
            text = decode_xs_common(data)
            f.write(f"解码文本:\n{text}\n\n")
            try:
                parsed = json.loads(text)
                f.write(f"JSON 字段数: {len(parsed)}\n\n")
                f.write("字段详情:\n")
                for k, v in parsed.items():
                    val_str = str(v)
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    f.write(f"  {k}: {val_str}\n")
                f.write(f"\n格式化 JSON:\n")
                f.write(json.dumps(parsed, indent=2, ensure_ascii=False) + "\n")
            except json.JSONDecodeError as e:
                f.write(f"JSON 解析失败: {e}\n")
        except Exception as e:
            f.write(f"解码失败: {e}\n")

print(f"结果已写入: {out_path}")
sys.exit(0)
