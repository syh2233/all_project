#!/usr/bin/env python3
"""
对比生成的X-s-common与真实值的差异
"""

import json
import time
import base64
from xiaohongshu_xs_common_generator import XiaohongshuXSCommonGenerator


def compare_xs_common():
    """对比X-s-common生成结果"""
    
    # 真实的X-s-common值
    real_xs_common = "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0qEN0ZjNsQh+aHCH0rEweDIwBP9G0rFPA41PoD98/Q7qeSfy9QVyn+Tyn4I8BkfG9rlJ7qh+/ZIPeZ9+ecF+ADjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfRSL98lnLYl49IUqgcMc0mrJFShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrLharQl4LShyBEl20YdanTQ8fRl49TQcMkgwBuAq9zV/9pnLoqAag8m8/mf89pDzBY7aLpOqAbgtF8EqgzGanWA8/bDcnLAzDRApSm7/9pf/7+8qgcAagYLq94p+d+/4gqM/e4Nq98n494QPMQCa/PFP7Qn4FEY4gqUJ7+kG7SI87+D8/4Apdb7tFS3a9prPrbApDlacDS9+nphPBzS8rD3cDSe87+fLo4Hag8QzSbc4FYcpdzmagWM8/8M4o8Qy9RS+dp7+LSiP7+x4gqM/db7z9Rn47pQc7kLag8a4bbSpDboJsRAygbFzDSiLozQynpSngp7J9pgG9+IpLRAzo+34LSiLdSFLo472db7cLS38g+gqgzMqLSmqM8B+dPlanQPaLLIqA8S8o+kLoz0GMm7qDSeafpfpd4fanTdqAGIp9RQcFTS8Bu68p4n4e+QPA4Spdb7PAYsngQQyrW3aLP9q7YQJ9L9wg8S8oQOqMSc4FzQc9T7aLpkwobM4F+Qy7p7a/+O8n8S+ozdzrkSP7p7+LDA/eZUqg4Scfc68nSx8o+xqgzkz7bFJrSkqDlQcM+DJM8F+F4n4FTQcFbS8Si9q9Sc4URt4g4PanYBt9bM498Qc9M6cDDROaHVHdWEH0iT+APhP0LF+AGMNsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR"
    
    print("🔍 X-s-common对比分析")
    print("=" * 60)
    
    print(f"真实X-s-common长度: {len(real_xs_common)}")
    print(f"真实X-s-common前50字符: {real_xs_common[:50]}")
    print(f"真实X-s-common后50字符: {real_xs_common[-50:]}")
    
    # 尝试解码真实的X-s-common
    print(f"\n📋 尝试解码真实X-s-common:")
    
    # 1. 标准Base64解码
    try:
        decoded = base64.b64decode(real_xs_common).decode('utf-8')
        print(f"✅ 标准Base64解码成功: {decoded}")
    except Exception as e:
        print(f"❌ 标准Base64解码失败: {e}")
    
    # 2. URL Safe Base64解码
    try:
        url_safe = real_xs_common.replace('-', '+').replace('_', '/')
        decoded = base64.b64decode(url_safe).decode('utf-8')
        print(f"✅ URL Safe Base64解码成功: {decoded}")
    except Exception as e:
        print(f"❌ URL Safe Base64解码失败: {e}")
    
    # 3. 检查是否包含特殊前缀
    if real_xs_common.startswith('XYS_'):
        try:
            without_prefix = real_xs_common[4:]
            decoded = base64.b64decode(without_prefix).decode('utf-8')
            print(f"✅ 去除XYS_前缀解码成功: {decoded}")
        except Exception as e:
            print(f"❌ 去除XYS_前缀解码失败: {e}")
    
    # 4. 分析字符频率
    print(f"\n🔍 真实X-s-common字符频率分析:")
    char_count = {}
    for char in real_xs_common:
        char_count[char] = char_count.get(char, 0) + 1
    
    sorted_chars = sorted(char_count.items(), key=lambda x: x[1], reverse=True)[:10]
    for char, count in sorted_chars:
        print(f"   '{char}': {count}次")
    
    # 5. 使用我们的生成器生成X-s-common
    print(f"\n🤖 使用我们的生成器:")
    generator = XiaohongshuXSCommonGenerator()
    
    # 设置测试数据
    generator.set_sign_random("test_random_123")
    generator.set_device_fingerprint("test_device_fp", "test_suffix")
    
    test_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?note_id=68a35fc0000000001c009cd9&root_comment_id=68a83b5900000000260052c3&num=10&cursor=68a83ccd000000002700255f&image_formats=jpg,webp,avif&top_comment_id=&xsec_token=ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI%3D"
    
    generated_xs_common = generator.generate_xs_common(test_url)
    
    print(f"生成的X-s-common: {generated_xs_common}")
    print(f"生成的X-s-common长度: {len(generated_xs_common)}")
    
    # 对比
    print(f"\n📊 对比结果:")
    print(f"真实值长度: {len(real_xs_common)}")
    print(f"生成值长度: {len(generated_xs_common)}")
    print(f"长度差异: {len(real_xs_common) - len(generated_xs_common)}")
    
    if generated_xs_common == real_xs_common:
        print("✅ 完全匹配！")
    else:
        print("❌ 不匹配")
        
        # 尝试找到可能的模式
        print(f"\n🔍 模式分析:")
        
        # 检查是否我们的生成结果是真实值的一部分
        if generated_xs_common in real_xs_common:
            print(f"✅ 生成值是真实值的一部分")
            pos = real_xs_common.find(generated_xs_common)
            print(f"   位置: {pos}-{pos + len(generated_xs_common)}")
        elif real_xs_common in generated_xs_common:
            print(f"✅ 真实值是生成值的一部分")
            pos = generated_xs_common.find(real_xs_common)
            print(f"   位置: {pos}-{pos + len(real_xs_common)}")
        else:
            print(f"❌ 没有包含关系")
            
        # 检查字符集
        real_chars = set(real_xs_common)
        gen_chars = set(generated_xs_common)
        common_chars = real_chars & gen_chars
        
        print(f"真实值字符集: {len(real_chars)}个独特字符")
        print(f"生成值字符集: {len(gen_chars)}个独特字符")
        print(f"共同字符: {len(common_chars)}个")
        print(f"真实值独有字符: {real_chars - gen_chars}")
        print(f"生成值独有字符: {gen_chars - real_chars}")


if __name__ == "__main__":
    compare_xs_common()