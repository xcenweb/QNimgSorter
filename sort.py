# 最初版本的分类程序，留作纪念

import tool
import sys

# 存储原始待分类图片文件夹
init_source_path = sys.path[0] + '\\images\\*'

# 存储分类后图片的文件夹
init_sorted_path = sys.path[0] + '\\sortImages\\'

# 从标准图片获取RGB值
# 期望的第一组RGB值（个人主页）
future_rgbs_a = tool.read_image_RGB('init\\sort_a.jpg', max_colors=5)

# 期望的第二组RGB值（看完后的截图）
future_rgbs_b = tool.read_image_RGB('init\\sort_b.jpg', max_colors=5)

# =========================================================

rgbs = tool.read_image_RGBS(init_source_path, max_colors=5)


for name,item in rgbs.items():
    print('-'*20, "\n正在处理文件：", name, '.' * 6)

    # 第一组比对值
    group_a = tool.rgb_similarity(future_rgbs_a, item['rgbs'])

    # 第二组比对值
    group_b = tool.rgb_similarity(future_rgbs_b, item['rgbs'])

    # 蹦跶一下，看看回调QuQ
    print('A:', group_a, 'B:', group_b)

    # 开始比对
    if group_a > group_b:
        print('对比结果：个人主页\n移动结果：', tool.move_file(item['filepath'],init_sorted_path + '2'))
    elif group_a < group_b:
        print('对比结果：看完后截图\n移动结果：', tool.move_file(item['filepath'],init_sorted_path + '1'))
    else:
        # print('对比结果：其他\n移动结果：', tool.move_file(item['filepath'],init_sorted_path + '其他'))
        continue